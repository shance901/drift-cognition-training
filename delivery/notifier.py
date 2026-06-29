"""
Notification hub — Stage 4 of the pipeline.

Sends curated parcel alerts via Slack, Twilio SMS, and/or a generic webhook.
Only fires when a parcel's composite_score meets the minimum threshold.
"""

import json
import logging
import textwrap
from typing import Optional

import requests

from config import NOTIFY

logger = logging.getLogger(__name__)


def _slack_send(text: str) -> bool:
    if not NOTIFY.slack_bot_token:
        logger.debug("Slack not configured; skipping")
        return False
    try:
        from slack_sdk import WebClient
        client = WebClient(token=NOTIFY.slack_bot_token)
        resp = client.chat_postMessage(channel=NOTIFY.slack_channel, text=text)
        return resp["ok"]
    except Exception:
        logger.exception("Slack notification failed")
        return False


def _twilio_send(body: str) -> bool:
    if not (NOTIFY.twilio_account_sid and NOTIFY.twilio_auth_token):
        logger.debug("Twilio not configured; skipping")
        return False
    try:
        from twilio.rest import Client
        client = Client(NOTIFY.twilio_account_sid, NOTIFY.twilio_auth_token)
        msg = client.messages.create(
            body=body[:1600],
            from_=NOTIFY.twilio_from_number,
            to=NOTIFY.twilio_to_number,
        )
        logger.info("Twilio SMS sent: %s", msg.sid)
        return True
    except Exception:
        logger.exception("Twilio notification failed")
        return False


def _webhook_send(payload: dict) -> bool:
    if not NOTIFY.webhook_url:
        logger.debug("Webhook not configured; skipping")
        return False
    try:
        resp = requests.post(
            NOTIFY.webhook_url,
            json=payload,
            timeout=10,
            headers={"Content-Type": "application/json"},
        )
        resp.raise_for_status()
        return True
    except Exception:
        logger.exception("Webhook notification failed")
        return False


def format_alert(enriched: dict) -> str:
    """Build the human-readable alert string sent across all channels."""
    parcel_id = enriched.get("parcel_id", "N/A")
    headline = enriched.get("alert_headline", "New surplus parcel detected")
    body = enriched.get("alert_body", "")
    score = enriched.get("composite_score", 0)
    tier = enriched.get("investment_tier", "")
    address = enriched.get("address") or "Address not on file"
    lot_sqft = enriched.get("lot_sqft")
    zoning = enriched.get("zoning_code", "Unknown")
    flood = enriched.get("flood_zone") or "X (minimal)"
    just_val = enriched.get("just_value")

    sqft_str = f"{lot_sqft:,} sqft" if lot_sqft else "size unknown"
    val_str = f"${int(float(just_val)):,}" if just_val else "not assessed"

    alert = textwrap.dedent(f"""
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    SURPLUS LAND ALERT — Escambia County
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Parcel: {parcel_id}
    Address: {address}
    Score: {score}/100  |  {tier}

    {headline}

    Lot Size: {sqft_str}
    Zoning: {zoning}
    Flood Zone: {flood}
    Just Value: {val_str}

    {body}
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """).strip()
    return alert


def send_alert(enriched: dict) -> bool:
    """
    Dispatch a parcel alert through all configured channels.
    Returns True if at least one channel delivered successfully.
    """
    score = enriched.get("composite_score", 0)
    if score < NOTIFY.min_alert_score:
        logger.debug(
            "Parcel %s score %d below threshold %d; no alert sent",
            enriched.get("parcel_id"),
            score,
            NOTIFY.min_alert_score,
        )
        return False

    alert_text = format_alert(enriched)
    webhook_payload = {
        "parcel_id": enriched.get("parcel_id"),
        "composite_score": score,
        "investment_tier": enriched.get("investment_tier"),
        "alert_headline": enriched.get("alert_headline"),
        "alert_body": enriched.get("alert_body"),
        "address": enriched.get("address"),
        "zoning_code": enriched.get("zoning_code"),
        "lot_sqft": enriched.get("lot_sqft"),
        "flood_zone": enriched.get("flood_zone"),
        "url": enriched.get("url"),
    }

    slack_ok = _slack_send(alert_text)
    twilio_ok = _twilio_send(alert_text)
    webhook_ok = _webhook_send(webhook_payload)

    delivered = slack_ok or twilio_ok or webhook_ok
    if delivered:
        logger.info("Alert delivered for parcel %s", enriched.get("parcel_id"))
    else:
        logger.warning(
            "No delivery channel active for parcel %s; configure Slack/Twilio/Webhook",
            enriched.get("parcel_id"),
        )
    return delivered


def send_daily_digest(enriched_list: list[dict]) -> None:
    """
    Send a digest of all Tier 1 and Tier 2 parcels processed today.
    Useful for morning email / Slack report.
    """
    top = [
        e for e in enriched_list
        if e.get("composite_score", 0) >= NOTIFY.min_alert_score
    ]
    if not top:
        logger.info("No parcels met digest threshold today")
        return

    lines = [f"Daily Surplus Digest — {len(top)} actionable parcel(s)\n"]
    for e in sorted(top, key=lambda x: x.get("composite_score", 0), reverse=True):
        lines.append(
            f"• [{e.get('composite_score')}/100] {e.get('parcel_id')} — "
            f"{e.get('address', 'no address')} | {e.get('zoning_code')} | "
            f"{e.get('investment_tier')}"
        )

    digest = "\n".join(lines)
    _slack_send(digest)
    logger.info("Daily digest sent: %d parcels", len(top))

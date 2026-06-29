"""Unit tests for alert formatting and threshold logic."""

from unittest.mock import patch

from delivery.notifier import format_alert, send_alert


def _enriched(**kwargs) -> dict:
    base = {
        "parcel_id": "12-3456-789-012",
        "source": "BidEscambia",
        "title": "Tax Deed Clearing — RM-2 Infill",
        "url": "https://www.bidescambia.com/lot/123",
        "address": "1401 Cervantes St, Pensacola FL 32501",
        "lot_sqft": 8200,
        "zoning_code": "RM-2",
        "flood_zone": "X",
        "just_value": "47500",
        "composite_score": 82,
        "investment_tier": "Tier 1 — Immediate Action",
        "alert_headline": "Parcel 12-3456-789-012 entered Tax Deed Clearing list",
        "alert_body": (
            "Urban Pensacola boundary. RM-2 zoning. "
            "By-right quadplex eligible. Estimated pervious margin 38%."
        ),
    }
    base.update(kwargs)
    return base


class TestFormatAlert:
    def test_contains_parcel_id(self):
        alert = format_alert(_enriched())
        assert "12-3456-789-012" in alert

    def test_contains_score(self):
        alert = format_alert(_enriched())
        assert "82" in alert

    def test_contains_zoning(self):
        alert = format_alert(_enriched())
        assert "RM-2" in alert

    def test_formats_value(self):
        alert = format_alert(_enriched())
        assert "$47,500" in alert

    def test_unknown_value(self):
        alert = format_alert(_enriched(just_value=None))
        assert "not assessed" in alert


class TestSendAlert:
    def test_below_threshold_no_send(self):
        enriched = _enriched(composite_score=30)
        # No channels configured; just verify it returns False without crashing
        result = send_alert(enriched)
        assert result is False

    def test_above_threshold_attempts_channels(self):
        enriched = _enriched(composite_score=80)
        with (
            patch("delivery.notifier._slack_send", return_value=True) as mock_slack,
            patch("delivery.notifier._twilio_send", return_value=False),
            patch("delivery.notifier._webhook_send", return_value=False),
        ):
            result = send_alert(enriched)
            assert result is True
            mock_slack.assert_called_once()

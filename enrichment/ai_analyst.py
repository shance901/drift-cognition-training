"""
AI Enrichment Layer — Stage 3 of the pipeline.

Sends structured parcel data through a four-step prompt matrix using
the Anthropic API and returns a fully enriched ParcelAnalysis object.
"""

import json
import logging
from typing import Any

import anthropic

from config import AI
from .prompt_matrix import (
    SYSTEM_PROMPT,
    zoning_analysis_prompt,
    environmental_analysis_prompt,
    compliance_filter_prompt,
    composite_summary_prompt,
)

logger = logging.getLogger(__name__)


class AIAnalyst:
    def __init__(self):
        if not AI.api_key:
            raise EnvironmentError(
                "ANTHROPIC_API_KEY is not set. Add it to your .env file."
            )
        self._client = anthropic.Anthropic(api_key=AI.api_key)

    def analyze(self, parcel: dict) -> dict:
        """
        Run the full four-stage AI enrichment pipeline on a single parcel.
        Returns a merged result dict including all sub-analyses.
        """
        logger.info("AI enrichment: %s", parcel.get("parcel_id", "unknown"))

        zoning = self._run_prompt(zoning_analysis_prompt(parcel))
        environmental = self._run_prompt(environmental_analysis_prompt(parcel))
        compliance = self._run_prompt(compliance_filter_prompt(parcel))
        summary = self._run_prompt(
            composite_summary_prompt(parcel, zoning, environmental, compliance)
        )

        return {
            "parcel_id": parcel.get("parcel_id"),
            "source": parcel.get("source"),
            "title": parcel.get("title"),
            "url": parcel.get("url"),
            "address": parcel.get("situs_address") or parcel.get("address"),
            "lot_sqft": parcel.get("lot_sqft_gis") or parcel.get("lot_sqft"),
            "zoning_code": parcel.get("zoning_code"),
            "flood_zone": parcel.get("flood_zone"),
            "just_value": parcel.get("just_value"),
            "zoning_analysis": zoning,
            "environmental_analysis": environmental,
            "compliance_analysis": compliance,
            "summary": summary,
            "composite_score": summary.get("composite_score", 0),
            "investment_tier": summary.get("investment_tier", "Tier 4 — Pass"),
            "alert_headline": summary.get("alert_headline", ""),
            "alert_body": summary.get("alert_body", ""),
        }

    def _run_prompt(self, messages: list[dict]) -> dict:
        """Call the API and parse the JSON response. Returns {} on error."""
        try:
            response = self._client.messages.create(
                model=AI.model,
                max_tokens=AI.max_tokens,
                system=SYSTEM_PROMPT,
                messages=messages,
            )
            text = response.content[0].text.strip()
            return json.loads(text)
        except json.JSONDecodeError:
            logger.warning("AI returned non-JSON; attempting extraction")
            return self._extract_json_from_text(text)
        except anthropic.APIError:
            logger.exception("Anthropic API error during enrichment")
            return {}

    @staticmethod
    def _extract_json_from_text(text: str) -> dict:
        """Last-resort extraction: find first { ... } block in the response."""
        start = text.find("{")
        end = text.rfind("}") + 1
        if start >= 0 and end > start:
            try:
                return json.loads(text[start:end])
            except json.JSONDecodeError:
                pass
        return {}


def enrich_parcels(parcels: list[dict]) -> list[dict]:
    """
    Batch-enrich a list of parsed parcel dicts.
    Parcels without a valid parcel_id receive a minimal stub result.
    """
    analyst = AIAnalyst()
    results = []
    for parcel in parcels:
        if not parcel.get("parcel_id"):
            logger.debug("Skipping parcel with no ID: %s", parcel.get("title"))
            continue
        result = analyst.analyze(parcel)
        results.append(result)
    return results

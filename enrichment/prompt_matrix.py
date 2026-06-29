"""
Prompt templates for the AI enrichment pipeline.
Each template receives a formatted parcel context dict and returns a
complete messages list ready to send to the Anthropic API.
"""

from config import AI

_SYSTEM = f"""You are a licensed real estate analysis assistant specializing in
municipal surplus land acquisition in {AI.jurisdiction}.
You have deep familiarity with the {AI.land_dev_code_version} and the
Escambia County Land Development Code, FEMA flood map conventions, and
Florida Statute Chapter 197 (tax deed proceedings).

Your role is to evaluate government surplus and tax deed parcels for
by-right development potential. Be concise, accurate, and flag risks
prominently. Never speculate beyond the data provided.
Return your analysis ONLY as valid JSON — no markdown fences, no prose."""


def zoning_analysis_prompt(parcel: dict) -> list[dict]:
    context = _format_parcel(parcel)
    user_content = f"""Analyze this parcel for by-right development potential under the
Escambia County / Pensacola UDO.

PARCEL DATA:
{context}

Return a JSON object with these exact keys:
{{
  "zoning_summary": "<1-2 sentence description of zone>",
  "by_right_uses": ["<use1>", "<use2>"],
  "max_density_units": <int or null>,
  "quadplex_eligible": <true/false>,
  "setbacks": {{"front": <ft>, "rear": <ft>, "side": <ft>}},
  "max_lot_coverage_pct": <float or null>,
  "parking_required_per_unit": <float or null>,
  "priority_rating": "<High|Medium|Low|Bypass>",
  "priority_reason": "<one sentence>",
  "action_flags": ["<flag1>"]
}}"""
    return [
        {"role": "user", "content": user_content},
    ]


def environmental_analysis_prompt(parcel: dict) -> list[dict]:
    context = _format_parcel(parcel)
    user_content = f"""Evaluate environmental and regulatory constraints for this parcel.

PARCEL DATA:
{context}

Return a JSON object with these exact keys:
{{
  "flood_risk": "<None|Low|Medium|High|Severe>",
  "flood_zone_explanation": "<one sentence>",
  "wetland_risk": "<None|Low|Medium|High>",
  "wetland_buffer_encroachment": <true/false>,
  "estimated_pervious_space_pct": <float or null>,
  "watershed_proximity_flag": <true/false>,
  "environmental_notes": "<brief notes or null>",
  "buildable_area_sqft": <int or null>,
  "environmental_score": <0-100, higher is cleaner>
}}"""
    return [
        {"role": "user", "content": user_content},
    ]


def compliance_filter_prompt(parcel: dict) -> list[dict]:
    context = _format_parcel(parcel)
    user_content = f"""Run FR 4.0 regulatory integrity checks on this parcel.
Identify any hidden liabilities that would impair acquisition or development.

PARCEL DATA:
{context}

Return a JSON object with these exact keys:
{{
  "code_enforcement_risk": "<None|Low|Medium|High>",
  "title_concerns": ["<concern1>"],
  "easement_flags": ["<flag1>"],
  "unpermitted_structure_risk": "<None|Low|Medium|High>",
  "access_issue": <true/false>,
  "municipal_lien_risk": "<None|Low|Medium|High>",
  "acquisition_recommendation": "<Proceed|Proceed with Caution|Due Diligence Required|Avoid>",
  "hidden_liability_notes": "<brief notes or null>",
  "compliance_score": <0-100, higher is cleaner>
}}"""
    return [
        {"role": "user", "content": user_content},
    ]


def composite_summary_prompt(
    parcel: dict,
    zoning_result: dict,
    env_result: dict,
    compliance_result: dict,
) -> list[dict]:
    context = _format_parcel(parcel)
    user_content = f"""Produce a final investment readiness summary for this parcel.

PARCEL DATA:
{context}

ZONING ANALYSIS:
{_format_dict(zoning_result)}

ENVIRONMENTAL ANALYSIS:
{_format_dict(env_result)}

COMPLIANCE ANALYSIS:
{_format_dict(compliance_result)}

Return a JSON object with these exact keys:
{{
  "alert_headline": "<≤120 char alert headline>",
  "composite_score": <0-100>,
  "investment_tier": "<Tier 1 — Immediate Action|Tier 2 — Monitor|Tier 3 — Watch List|Tier 4 — Pass>",
  "key_strengths": ["<strength1>", "<strength2>"],
  "key_risks": ["<risk1>", "<risk2>"],
  "estimated_development_capacity": "<brief capacity statement>",
  "recommended_next_step": "<actionable one-liner>",
  "alert_body": "<3-4 sentence investor alert suitable for SMS/Slack>"
}}"""
    return [
        {"role": "user", "content": user_content},
    ]


def _format_parcel(parcel: dict) -> str:
    lines = []
    for k, v in parcel.items():
        if v is not None and k not in ("raw_data",):
            lines.append(f"  {k}: {v}")
    return "\n".join(lines)


def _format_dict(d: dict) -> str:
    lines = []
    for k, v in d.items():
        lines.append(f"  {k}: {v}")
    return "\n".join(lines)


SYSTEM_PROMPT = _SYSTEM

"""
FR 4.0 Compliance Filter — pre-AI sanity checks.

Applies deterministic rule-based filters before sending a parcel to the
AI enrichment layer. This catches obvious bypasses cheaply without an API call
and hard-codes Escambia County regulatory parameters.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field

from config import ZONING, ENV

logger = logging.getLogger(__name__)


@dataclass
class FilterResult:
    parcel_id: str
    passed: bool
    flags: list[str] = field(default_factory=list)
    score_penalty: int = 0


# ---------------------------------------------------------------------------
# Individual rule functions — each returns (flag_message | None, penalty)
# ---------------------------------------------------------------------------

def check_lot_size(parcel: dict) -> tuple[str | None, int]:
    sqft = parcel.get("lot_sqft_gis") or parcel.get("lot_sqft")
    if sqft is None:
        return "Lot size unknown — verify before acquisition", 5
    if sqft < ZONING.min_lot_sqft:
        return f"Undersized lot ({sqft} sqft < {ZONING.min_lot_sqft} min)", 30
    return None, 0


def check_zoning_bypass(parcel: dict) -> tuple[str | None, int]:
    code = (parcel.get("zoning_code") or "").upper()
    if any(code.startswith(bypass) for bypass in ZONING.bypass_codes):
        return f"Bypass zoning code: {code} — rezoning required", 50
    return None, 0


def check_flood_zone(parcel: dict) -> tuple[str | None, int]:
    zone = (parcel.get("flood_zone") or "").upper().strip()
    if any(zone.startswith(hz) for hz in ENV.high_risk_flood_zones):
        return f"High-risk FEMA flood zone: {zone}", 35
    if any(zone.startswith(mz) for mz in ENV.medium_risk_flood_zones):
        return f"Medium-risk FEMA flood zone: {zone} — obtain elevation certificate", 15
    return None, 0


def check_wetland_proximity(parcel: dict) -> tuple[str | None, int]:
    if parcel.get("wetland_type"):
        return f"Wetland designation detected: {parcel['wetland_type']}", 20
    return None, 0


def check_owner_municipality(parcel: dict) -> tuple[str | None, int]:
    owner = (parcel.get("owner_name") or "").upper()
    municipal_keywords = ["COUNTY", "CITY OF", "STATE OF", "FL DEP", "FDOT", "USA ", "UNITED STATES"]
    if any(kw in owner for kw in municipal_keywords):
        return f"Current owner may be government entity: {owner} — confirm transfer status", 10
    return None, 0


def check_access(parcel: dict) -> tuple[str | None, int]:
    desc = (parcel.get("legal_description") or "").upper()
    # Landlocked indicators in legal description
    if any(kw in desc for kw in ["EASEMENT ONLY", "NO INGRESS", "LANDLOCKED"]):
        return "Legal description suggests access easement or landlocked parcel", 50
    return None, 0


# ---------------------------------------------------------------------------
# Public interface
# ---------------------------------------------------------------------------

_RULES = [
    check_lot_size,
    check_zoning_bypass,
    check_flood_zone,
    check_wetland_proximity,
    check_owner_municipality,
    check_access,
]


def apply_compliance_filter(parcel: dict) -> FilterResult:
    """
    Run all FR 4.0 rule checks against a parcel dict.
    Returns a FilterResult with accumulated flags and score penalty.
    A parcel fails (passed=False) if total penalty >= 50.
    """
    pid = parcel.get("parcel_id", "unknown")
    flags: list[str] = []
    total_penalty = 0

    for rule in _RULES:
        flag, penalty = rule(parcel)
        if flag:
            flags.append(flag)
            total_penalty += penalty
            logger.debug("[%s] Flag: %s (penalty %d)", pid, flag, penalty)

    passed = total_penalty < 50
    return FilterResult(
        parcel_id=pid,
        passed=passed,
        flags=flags,
        score_penalty=total_penalty,
    )


def pre_filter_parcels(parcels: list[dict]) -> tuple[list[dict], list[FilterResult]]:
    """
    Split parcels into (ai_queue, rejected).
    Returns the queue for AI enrichment and all filter results.
    """
    ai_queue: list[dict] = []
    filter_results: list[FilterResult] = []

    for parcel in parcels:
        result = apply_compliance_filter(parcel)
        filter_results.append(result)
        if result.passed:
            # Attach flags to parcel for later AI context
            parcel["pre_filter_flags"] = result.flags
            parcel["pre_filter_penalty"] = result.score_penalty
            ai_queue.append(parcel)
        else:
            logger.info(
                "Parcel %s rejected by compliance filter (penalty=%d)",
                result.parcel_id,
                result.score_penalty,
            )

    logger.info(
        "Compliance filter: %d/%d parcels passed",
        len(ai_queue),
        len(parcels),
    )
    return ai_queue, filter_results

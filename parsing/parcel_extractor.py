"""
Normalises raw parcel IDs and extracts structured property fields
from the mixed text produced by the ingestion scrapers.
"""

import re
from typing import Optional

# Escambia County parcel format: XX-XXXX-XXX-XXX  (hyphen-separated digits)
_PARCEL_PATTERN = re.compile(
    r"(\d{2})[- ]?(\d{4})[- ]?(\d{3})[- ]?(\d{3})"
)
_SQFT_PATTERN = re.compile(
    r"(\d[\d,]*)\s*(?:sq(?:uare)?\s*f(?:ee)?t|sf\b)", re.I
)
_ACRES_PATTERN = re.compile(r"(\d+\.?\d*)\s*acres?", re.I)
_ADDR_PATTERN = re.compile(
    r"\d{1,5}\s+[A-Z][a-zA-Z\s]+(?:St|Ave|Blvd|Dr|Rd|Ln|Ct|Way|Pl|Ter)\b",
    re.I,
)
_ASSESSED_PATTERN = re.compile(
    r"assessed\s+value[:\s]+\$?([\d,]+)", re.I
)
_LIEN_PATTERN = re.compile(
    r"(?:lien|cer(?:tificate)?)[:\s#]+([\w-]+)", re.I
)


def normalize_parcel_id(raw: Optional[str]) -> Optional[str]:
    """Return XX-XXXX-XXX-XXX canonical form or None if unparseable."""
    if not raw:
        return None
    m = _PARCEL_PATTERN.search(raw)
    if not m:
        return None
    return f"{m.group(1)}-{m.group(2)}-{m.group(3)}-{m.group(4)}"


def extract_fields(raw_text: str) -> dict:
    """
    Pull structured fields out of free-form property description text.
    Returns a dict; any field not found is None.
    """
    text = raw_text.replace("\n", " ")

    sqft: Optional[int] = None
    sqft_m = _SQFT_PATTERN.search(text)
    if sqft_m:
        sqft = int(sqft_m.group(1).replace(",", ""))

    acres: Optional[float] = None
    acres_m = _ACRES_PATTERN.search(text)
    if acres_m:
        acres = float(acres_m.group(1))
        if sqft is None:
            sqft = int(acres * 43_560)

    address_m = _ADDR_PATTERN.search(text)
    address = address_m.group(0).strip() if address_m else None

    assessed_m = _ASSESSED_PATTERN.search(text)
    assessed_value = (
        int(assessed_m.group(1).replace(",", "")) if assessed_m else None
    )

    lien_m = _LIEN_PATTERN.search(text)
    lien_number = lien_m.group(1) if lien_m else None

    return {
        "address": address,
        "lot_sqft": sqft,
        "lot_acres": acres,
        "assessed_value": assessed_value,
        "lien_certificate_number": lien_number,
    }


def enrich_raw_listing(listing: dict) -> dict:
    """
    Accepts a raw listing dict from ingestion layer and returns an
    enriched copy with normalised parcel ID and extracted fields.
    """
    enriched = dict(listing)
    enriched["parcel_id"] = normalize_parcel_id(listing.get("raw_parcel_id"))

    raw_text = listing.get("raw_data", {}).get("text_snippet", "")
    extracted = extract_fields(raw_text)
    enriched.update(extracted)

    return enriched

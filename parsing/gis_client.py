"""
Escambia County GIS / Property Appraiser API client.

Queries the ESRI ArcGIS REST endpoint at the Escambia Clerk GIS server
and the Property Appraiser's public search to fetch lot geometry,
ownership, zoning, flood zone, and land-use codes for a given parcel ID.
"""

import logging
from typing import Optional

import requests

from config import SOURCES, SCRAPER

logger = logging.getLogger(__name__)

# Public ArcGIS REST endpoints (no auth required)
_GIS_BASE = "https://gis.escambiaclerk.com/arcgis/rest/services"
_PA_PARCEL_LAYER = f"{_GIS_BASE}/Property/MapServer/0/query"
_FLOOD_ZONE_LAYER = f"{_GIS_BASE}/Hazards/FloodZones/MapServer/0/query"
_ZONING_LAYER = f"{_GIS_BASE}/Planning/Zoning/MapServer/0/query"
_WETLANDS_LAYER = f"{_GIS_BASE}/Environmental/Wetlands/MapServer/0/query"

_ARCGIS_PARAMS = {
    "f": "json",
    "outFields": "*",
    "returnGeometry": "false",
}

_SESSION = requests.Session()
_SESSION.headers["User-Agent"] = SCRAPER.user_agent


def _arcgis_query(url: str, where: str) -> list[dict]:
    """Execute an ArcGIS feature query and return the attributes of matching features."""
    params = dict(_ARCGIS_PARAMS)
    params["where"] = where
    try:
        resp = _SESSION.get(url, params=params, timeout=SCRAPER.timeout_seconds)
        resp.raise_for_status()
        data = resp.json()
        return [f.get("attributes", {}) for f in data.get("features", [])]
    except Exception:
        logger.warning("ArcGIS query failed: %s | where=%s", url, where)
        return []


def fetch_parcel_data(parcel_id: str) -> dict:
    """
    Pull all available GIS data for parcel_id.
    Returns a merged attribute dict; missing fields are None.
    """
    safe_id = parcel_id.replace("-", "").replace(" ", "")
    where = f"UPPER(REPLACE(PARCELID, '-', '')) = '{safe_id}'"

    parcel_attrs = {}
    results = _arcgis_query(_PA_PARCEL_LAYER, where)
    if results:
        parcel_attrs = results[0]

    # If we have geometry info (centroid/polygon), query derived layers
    flood_attrs: dict = {}
    zoning_attrs: dict = {}
    wetland_attrs: dict = {}

    # Use parcel ID to cross-query spatial layers
    flood_results = _arcgis_query(_FLOOD_ZONE_LAYER, where)
    if flood_results:
        flood_attrs = flood_results[0]

    zoning_results = _arcgis_query(_ZONING_LAYER, where)
    if zoning_results:
        zoning_attrs = zoning_results[0]

    wetland_results = _arcgis_query(_WETLANDS_LAYER, where)
    if wetland_results:
        wetland_attrs = wetland_results[0]

    return _normalize_gis_response(
        parcel_id, parcel_attrs, flood_attrs, zoning_attrs, wetland_attrs
    )


def _normalize_gis_response(
    parcel_id: str,
    parcel: dict,
    flood: dict,
    zoning: dict,
    wetlands: dict,
) -> dict:
    """Map raw GIS attribute names to a clean, consistent schema."""

    def pick(d: dict, *keys) -> Optional[str]:
        for k in keys:
            v = d.get(k) or d.get(k.upper()) or d.get(k.lower())
            if v is not None:
                return str(v)
        return None

    lot_sqft_raw = pick(parcel, "TOTLNDAREA", "LandArea", "SqFt", "SQFT")
    lot_sqft = int(float(lot_sqft_raw)) if lot_sqft_raw else None

    return {
        "parcel_id": parcel_id,
        # Ownership & location
        "owner_name": pick(parcel, "OWN1", "OwnerName", "OWNERNAME"),
        "situs_address": pick(parcel, "SITUSADDR", "SitusAddress", "ADDRESS"),
        "legal_description": pick(parcel, "LEGALDESC", "LegalDescription"),
        # Lot dimensions
        "lot_sqft_gis": lot_sqft,
        "lot_frontage_ft": pick(parcel, "FRONTAGE", "Frontage"),
        "lot_depth_ft": pick(parcel, "DEPTH", "Depth"),
        # Valuation
        "just_value": pick(parcel, "JUSTVALUE", "JustValue", "MKTVAL"),
        "assessed_value_gis": pick(parcel, "ASSESSEDVALUE", "ASSDVAL"),
        "taxable_value": pick(parcel, "TAXABLEVALUE", "TAXVAL"),
        # Zoning / land use
        "zoning_code": pick(zoning, "ZONINGCODE", "ZONE_CODE", "ZONING", "ZONDESC"),
        "land_use_code": pick(parcel, "DORCUC", "DorUseCode", "LANDUSE"),
        "future_land_use": pick(zoning, "FLU", "FUTUREUSE", "FUTURELU"),
        # Environmental
        "flood_zone": pick(flood, "FLDZONE", "FloodZone", "ZONE"),
        "firm_panel": pick(flood, "FIRM_PANEL", "PANEL"),
        "wetland_type": pick(wetlands, "ATTRIBUTE", "WetType", "TYPE"),
        "wetland_acres": pick(wetlands, "SHAPE_AREA", "WetAcres"),
        # Metadata
        "gis_data_fetched": True,
    }


def fetch_parcel_data_safe(parcel_id: Optional[str]) -> dict:
    """Wrapper that returns an empty GIS dict when parcel_id is None."""
    if not parcel_id:
        return {"parcel_id": None, "gis_data_fetched": False}
    try:
        return fetch_parcel_data(parcel_id)
    except Exception:
        logger.exception("GIS fetch failed for %s", parcel_id)
        return {"parcel_id": parcel_id, "gis_data_fetched": False}

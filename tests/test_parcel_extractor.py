"""Unit tests for parcel extraction and normalisation logic."""

import pytest
from parsing.parcel_extractor import normalize_parcel_id, extract_fields, enrich_raw_listing


class TestNormalizeParcelId:
    def test_hyphen_format(self):
        assert normalize_parcel_id("00-1234-567-890") == "00-1234-567-890"

    def test_space_format(self):
        assert normalize_parcel_id("00 1234 567 890") == "00-1234-567-890"

    def test_no_separator(self):
        assert normalize_parcel_id("00123456789O") is None  # letter in input

    def test_none_input(self):
        assert normalize_parcel_id(None) is None

    def test_parcel_embedded_in_text(self):
        result = normalize_parcel_id("Parcel ID: 12-3456-789-012 located in Pensacola")
        assert result == "12-3456-789-012"


class TestExtractFields:
    def test_sqft_extraction(self):
        fields = extract_fields("Lot size: 8,200 square feet, zoning RM-2")
        assert fields["lot_sqft"] == 8200

    def test_acres_to_sqft_conversion(self):
        fields = extract_fields("0.25 acres vacant land")
        assert fields["lot_acres"] == 0.25
        assert fields["lot_sqft"] == pytest.approx(10890, abs=1)

    def test_address_extraction(self):
        fields = extract_fields("Property at 1401 Cervantes St in Pensacola")
        assert fields["address"] is not None
        assert "1401" in fields["address"]

    def test_assessed_value(self):
        fields = extract_fields("Assessed Value: $47,500 as of 2024")
        assert fields["assessed_value"] == 47500

    def test_missing_fields_return_none(self):
        fields = extract_fields("No useful data here")
        assert fields["lot_sqft"] is None
        assert fields["address"] is None


class TestEnrichRawListing:
    def test_parcel_id_normalised(self):
        listing = {
            "source": "BidEscambia",
            "raw_parcel_id": "12 3456 789 012",
            "title": "Test lot",
            "url": "https://example.com",
            "raw_data": {"text_snippet": "8,200 square feet RM-2 zoning"},
        }
        result = enrich_raw_listing(listing)
        assert result["parcel_id"] == "12-3456-789-012"
        assert result["lot_sqft"] == 8200

    def test_missing_parcel_id(self):
        listing = {
            "source": "GovDeals",
            "raw_parcel_id": None,
            "title": "Unknown",
            "url": "https://example.com",
            "raw_data": {"text_snippet": "no parcel data"},
        }
        result = enrich_raw_listing(listing)
        assert result["parcel_id"] is None

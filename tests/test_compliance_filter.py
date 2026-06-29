"""Unit tests for the FR 4.0 compliance pre-filter."""

from enrichment.compliance_filter import apply_compliance_filter, pre_filter_parcels


def _base_parcel(**kwargs) -> dict:
    base = {
        "parcel_id": "12-3456-789-012",
        "lot_sqft_gis": 8200,
        "zoning_code": "RM-2",
        "flood_zone": "X",
        "wetland_type": None,
        "owner_name": "John Doe",
        "legal_description": "Lot 5 Block 3 Pensacola Heights",
    }
    base.update(kwargs)
    return base


class TestApplyComplianceFilter:
    def test_clean_parcel_passes(self):
        result = apply_compliance_filter(_base_parcel())
        assert result.passed is True
        assert result.score_penalty == 0

    def test_undersized_lot_flagged(self):
        result = apply_compliance_filter(_base_parcel(lot_sqft_gis=2000))
        assert any("Undersized" in f for f in result.flags)
        assert result.score_penalty >= 30

    def test_bypass_zoning_fails(self):
        result = apply_compliance_filter(_base_parcel(zoning_code="CON"))
        assert result.passed is False
        assert any("Bypass" in f or "rezoning" in f for f in result.flags)

    def test_high_risk_flood_zone_flagged(self):
        result = apply_compliance_filter(_base_parcel(flood_zone="AE"))
        assert any("flood zone" in f.lower() for f in result.flags)
        assert result.score_penalty >= 35

    def test_wetland_detected(self):
        result = apply_compliance_filter(_base_parcel(wetland_type="Freshwater Forested"))
        assert any("Wetland" in f for f in result.flags)

    def test_landlocked_parcel_fails(self):
        result = apply_compliance_filter(
            _base_parcel(legal_description="EASEMENT ONLY access from the north")
        )
        assert result.passed is False

    def test_municipal_owner_flagged(self):
        result = apply_compliance_filter(_base_parcel(owner_name="ESCAMBIA COUNTY"))
        assert any("government" in f.lower() or "entity" in f.lower() for f in result.flags)


class TestPreFilterParcels:
    def test_splits_correctly(self):
        parcels = [
            _base_parcel(parcel_id="AA-0001-001-001"),          # should pass
            _base_parcel(parcel_id="AA-0002-001-001", zoning_code="CON"),  # should fail
        ]
        queue, results = pre_filter_parcels(parcels)
        assert len(queue) == 1
        assert queue[0]["parcel_id"] == "AA-0001-001-001"
        assert len(results) == 2

    def test_flags_attached_to_passing_parcels(self):
        parcels = [_base_parcel(flood_zone="A")]  # medium risk, still passes
        queue, _ = pre_filter_parcels(parcels)
        assert len(queue) == 1
        assert "pre_filter_flags" in queue[0]

"""
Central configuration for the Municipal Surplus Land Platform.
Load secrets from environment variables; never hardcode credentials here.
"""

import os
from dataclasses import dataclass, field
from dotenv import load_dotenv

load_dotenv()


@dataclass
class ScraperConfig:
    request_delay_seconds: float = 2.0
    max_retries: int = 4
    backoff_factor: float = 2.0
    timeout_seconds: int = 30
    user_agent: str = (
        "MunicipalSurplusMonitor/1.0 (research; contact@yourorg.com)"
    )


@dataclass
class SourceURLs:
    bidescambia: str = "https://www.bidescambia.com"
    lienhub: str = "https://lienhub.com"
    govdeals: str = "https://www.govdeals.com"
    escambia_surplus: str = (
        "https://www.myescambia.com/our-county/finance/purchasing/surplus-property"
    )
    fl_dep_state_lands: str = (
        "https://floridadep.gov/lands/land-bureau-mapping-support-services"
    )
    escambia_gis_api: str = (
        "https://gis.escambiaclerk.com/arcgis/rest/services"
    )
    escambia_pa_api: str = (
        "https://www.escpa.org/PropertySearch/Search"
    )


@dataclass
class ZoningPriority:
    """
    Escambia County / City of Pensacola zoning codes flagged as
    high-value by-right development opportunities.
    """
    high_priority_codes: list = field(default_factory=lambda: [
        "RM-1",   # Residential Medium-Low: by-right duplex / triplex
        "RM-2",   # Residential Medium: by-right quadplex
        "RM-3",   # Residential Medium-High
        "MU-U",   # Mixed-Use Urban infill
        "MU-S",   # Mixed-Use Suburban
        "HC",     # Highway Commercial with residential overlay
    ])
    medium_priority_codes: list = field(default_factory=lambda: [
        "RS-1",
        "RS-2",
        "RS-3",
        "C-1",
        "C-2",
    ])
    bypass_codes: list = field(default_factory=lambda: [
        "AG",     # Agricultural — requires rezoning
        "CON",    # Conservation — typically unbuildable
        "P",      # Public / Institutional
    ])
    # Minimum lot size in sq ft to be actionable
    min_lot_sqft: int = 4_000
    # By-right quadplex threshold
    quadplex_threshold_sqft: int = 7_200


@dataclass
class EnvironmentalThresholds:
    # FEMA flood zones that trigger automatic caution flag
    high_risk_flood_zones: list = field(default_factory=lambda: ["AE", "AH", "AO", "VE", "V"])
    medium_risk_flood_zones: list = field(default_factory=lambda: ["A", "X500"])
    # Watershed buffer distance in feet
    watershed_buffer_ft: int = 100
    # Max imperviousness for RM zones (percent)
    max_impervious_rm: float = 0.60
    # Critical habitat / wetland proximity flag distance (feet)
    wetland_buffer_ft: int = 75


@dataclass
class NotificationConfig:
    slack_bot_token: str = field(default_factory=lambda: os.getenv("SLACK_BOT_TOKEN", ""))
    slack_channel: str = field(default_factory=lambda: os.getenv("SLACK_CHANNEL", "#surplus-land-alerts"))
    twilio_account_sid: str = field(default_factory=lambda: os.getenv("TWILIO_ACCOUNT_SID", ""))
    twilio_auth_token: str = field(default_factory=lambda: os.getenv("TWILIO_AUTH_TOKEN", ""))
    twilio_from_number: str = field(default_factory=lambda: os.getenv("TWILIO_FROM_NUMBER", ""))
    twilio_to_number: str = field(default_factory=lambda: os.getenv("TWILIO_TO_NUMBER", ""))
    webhook_url: str = field(default_factory=lambda: os.getenv("ALERT_WEBHOOK_URL", ""))
    # Only alert when composite score >= this threshold (0-100)
    min_alert_score: int = 60


@dataclass
class DatabaseConfig:
    url: str = field(
        default_factory=lambda: os.getenv("DATABASE_URL", "sqlite:///surplus_land.db")
    )


@dataclass
class AIConfig:
    api_key: str = field(default_factory=lambda: os.getenv("ANTHROPIC_API_KEY", ""))
    model: str = "claude-sonnet-4-6"
    max_tokens: int = 2048
    # County / jurisdiction context injected into every prompt
    jurisdiction: str = "Escambia County, Florida (City of Pensacola)"
    land_dev_code_version: str = "2024 UDO"


# ---------------------------------------------------------------------------
# Singleton instances imported by other modules
# ---------------------------------------------------------------------------

SCRAPER = ScraperConfig()
SOURCES = SourceURLs()
ZONING = ZoningPriority()
ENV = EnvironmentalThresholds()
NOTIFY = NotificationConfig()
DB = DatabaseConfig()
AI = AIConfig()

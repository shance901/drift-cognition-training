"""
Scraper for the Florida DEP Division of State Lands surplus registry.
Captures state-owned parcels released in the Escambia County / NW Florida region.
"""

import logging
import re
from typing import Any

from bs4 import BeautifulSoup

from config import SOURCES
from .base_scraper import BaseScraper

logger = logging.getLogger(__name__)

_ESCAMBIA_KEYWORDS = re.compile(
    r"\b(escambia|pensacola|cantonment|molino|century|bellview|pace|gulf\s*breeze)\b",
    re.I,
)
_PARCEL_RE = re.compile(r"\b\d{2}[- ]\d{4}[- ]\d{3}[- ]\d{3}\b")


class FlDepScraper(BaseScraper):
    source_name = "FlDepStateLands"

    def fetch_listings(self) -> list[dict[str, Any]]:
        response = self.get(SOURCES.fl_dep_state_lands)
        soup = BeautifulSoup(response.text, "lxml")
        return self._parse_surplus_section(soup)

    def _parse_surplus_section(self, soup: BeautifulSoup) -> list[dict[str, Any]]:
        listings = []

        # DEP posts surplus land notices as content blocks or downloadable lists
        candidate_blocks = soup.select(
            ".surplus-item, .land-notice, article, .field--type-text-long, .views-row"
        )
        if not candidate_blocks:
            # Fallback: all paragraphs and list items on the page
            candidate_blocks = soup.find_all(["p", "li", "tr"])

        for block in candidate_blocks:
            text = block.get_text(" ", strip=True)

            # Only process blocks that mention our region
            if not _ESCAMBIA_KEYWORDS.search(text):
                continue

            parcel_match = _PARCEL_RE.search(text)
            raw_parcel_id = (
                parcel_match.group(0).replace(" ", "-") if parcel_match else None
            )

            link = block.find("a", href=True)
            href = ""
            if link:
                href = link["href"]
                if not href.startswith("http"):
                    href = "https://floridadep.gov" + href

            listings.append(
                {
                    "source": self.source_name,
                    "raw_parcel_id": raw_parcel_id,
                    "title": text[:120],
                    "url": href or SOURCES.fl_dep_state_lands,
                    "raw_data": {"text_snippet": text[:600]},
                }
            )

        logger.debug("FL DEP parsed %d regional surplus notices", len(listings))
        return listings

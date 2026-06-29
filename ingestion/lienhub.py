"""
Scraper for LienHub — aggregator for Florida tax lien certificates
and tax deed applications, filtered to Escambia County.
"""

import re
import logging
from typing import Any

from bs4 import BeautifulSoup

from config import SOURCES
from .base_scraper import BaseScraper

logger = logging.getLogger(__name__)

_COUNTY_FILTER = "escambia"
_SEARCH_PATH = "/search"
_PARCEL_RE = re.compile(r"\b\d{2}[- ]\d{4}[- ]\d{3}[- ]\d{3}\b")


class LienHubScraper(BaseScraper):
    source_name = "LienHub"

    def fetch_listings(self) -> list[dict[str, Any]]:
        url = f"{SOURCES.lienhub}{_SEARCH_PATH}"
        params = {
            "state": "FL",
            "county": "Escambia",
            "type": "tax_deed",
            "status": "active",
        }
        response = self.get(url, params=params)
        soup = BeautifulSoup(response.text, "lxml")
        return self._parse_results(soup)

    def _parse_results(self, soup: BeautifulSoup) -> list[dict[str, Any]]:
        listings = []
        rows = soup.select("table.results-table tbody tr, .lien-card, .result-row")

        for row in rows:
            text = row.get_text(" ", strip=True)
            cells = row.select("td")

            parcel_match = _PARCEL_RE.search(text)
            raw_parcel_id = parcel_match.group(0).replace(" ", "-") if parcel_match else None

            # Try to pull structured fields from table cells
            raw_data: dict[str, Any] = {"text_snippet": text[:500]}
            if len(cells) >= 4:
                raw_data.update(
                    {
                        "certificate_number": cells[0].get_text(strip=True),
                        "owner": cells[1].get_text(strip=True),
                        "assessed_value": cells[2].get_text(strip=True),
                        "lien_amount": cells[3].get_text(strip=True),
                    }
                )

            link = row.select_one("a[href]")
            href = link["href"] if link else ""
            if href and not href.startswith("http"):
                href = SOURCES.lienhub + href

            listings.append(
                {
                    "source": self.source_name,
                    "raw_parcel_id": raw_parcel_id,
                    "title": f"Tax Deed – {raw_parcel_id or 'Unknown Parcel'}",
                    "url": href or SOURCES.lienhub,
                    "raw_data": raw_data,
                }
            )

        logger.debug("LienHub parsed %d results", len(listings))
        return listings

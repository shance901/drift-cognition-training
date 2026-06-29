"""
Scraper for BidEscambia — Escambia County's online auction/surplus portal.
Targets active tax deed and surplus property listings.
"""

import re
import logging
from typing import Any

from bs4 import BeautifulSoup

from config import SOURCES
from .base_scraper import BaseScraper

logger = logging.getLogger(__name__)

# BidEscambia uses iGovServices / OpenGov auction platform
_AUCTION_LIST_PATH = "/auction/list"
_PARCEL_RE = re.compile(
    r"\b(\d{2}-\d{4}-\d{3}-\d{3}|\d{2}\s+\d{4}\s+\d{3}\s+\d{3})\b"
)


class BidEscambiaScraper(BaseScraper):
    source_name = "BidEscambia"

    def fetch_listings(self) -> list[dict[str, Any]]:
        url = f"{SOURCES.bidescambia}{_AUCTION_LIST_PATH}"
        response = self.get(url)
        soup = BeautifulSoup(response.text, "lxml")
        return self._parse_auction_items(soup, url)

    def _parse_auction_items(
        self, soup: BeautifulSoup, base_url: str
    ) -> list[dict[str, Any]]:
        listings = []
        # BidEscambia renders items in .auction-item or table rows depending on version
        items = soup.select(".auction-item, tr.item-row, .listing-card")

        if not items:
            # Fallback: look for any anchor containing "parcel" or common real estate keywords
            items = soup.find_all(
                "a",
                href=re.compile(r"/(auction|item|lot)/\d+", re.I),
            )

        for item in items:
            text = item.get_text(" ", strip=True)
            title = self._extract_text(item, [".item-title", "h2", "h3", "strong"])
            href = item.get("href", "") if item.name == "a" else ""
            if href and not href.startswith("http"):
                href = SOURCES.bidescambia + href

            parcel_match = _PARCEL_RE.search(text)
            raw_parcel_id = parcel_match.group(0).replace(" ", "-") if parcel_match else None

            if not any(kw in text.lower() for kw in ("parcel", "real", "land", "property", "lot")):
                continue

            listings.append(
                {
                    "source": self.source_name,
                    "raw_parcel_id": raw_parcel_id,
                    "title": title or text[:120],
                    "url": href or base_url,
                    "raw_data": {"text_snippet": text[:500]},
                }
            )

        logger.debug("BidEscambia parsed %d candidate listings", len(listings))
        return listings

    @staticmethod
    def _extract_text(element: Any, selectors: list[str]) -> str:
        for sel in selectors:
            found = element.select_one(sel)
            if found:
                return found.get_text(strip=True)
        return ""

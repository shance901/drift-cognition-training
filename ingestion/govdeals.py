"""
Scraper for GovDeals — nationwide government surplus auction platform.
Filtered to Escambia County, FL real property listings.
GovDeals exposes a public search API alongside its HTML interface.
"""

import logging
from typing import Any

from bs4 import BeautifulSoup

from config import SOURCES
from .base_scraper import BaseScraper

logger = logging.getLogger(__name__)

# GovDeals category 4 = Real Estate
_SEARCH_URL = "https://www.govdeals.com/index.cfm"
_SEARCH_PARAMS = {
    "fa": "Main.AdvSearchResultsAction",
    "searchPg": "1",
    "category": "4",
    "state": "FL",
    "agency": "Escambia County",
    "kWord": "",
    "sortBy": "ad",
    "sortOrder": "A",
    "resultsPerPage": "50",
}


class GovDealsScraper(BaseScraper):
    source_name = "GovDeals"

    def fetch_listings(self) -> list[dict[str, Any]]:
        response = self.get(_SEARCH_URL, params=_SEARCH_PARAMS)
        soup = BeautifulSoup(response.text, "lxml")
        return self._parse_results(soup)

    def _parse_results(self, soup: BeautifulSoup) -> list[dict[str, Any]]:
        listings = []
        items = soup.select(".itemDiv, .result-item, table.itemTable tr[valign]")

        for item in items:
            text = item.get_text(" ", strip=True)
            if not text.strip():
                continue

            title_el = item.select_one(".itemTitle, .item-title, td.title a")
            title = title_el.get_text(strip=True) if title_el else text[:100]

            link = item.select_one("a[href]")
            href = ""
            if link:
                href = link.get("href", "")
                if href and not href.startswith("http"):
                    href = "https://www.govdeals.com" + href

            price_el = item.select_one(".currentBid, .current-bid, .price")
            current_bid = price_el.get_text(strip=True) if price_el else None

            end_el = item.select_one(".endDate, .auction-end, .closes")
            end_date = end_el.get_text(strip=True) if end_el else None

            raw_data: dict[str, Any] = {
                "text_snippet": text[:500],
                "current_bid": current_bid,
                "auction_end": end_date,
            }

            listings.append(
                {
                    "source": self.source_name,
                    "raw_parcel_id": None,  # GovDeals doesn't surface parcel IDs in list view
                    "title": title,
                    "url": href or _SEARCH_URL,
                    "raw_data": raw_data,
                }
            )

        logger.debug("GovDeals parsed %d results", len(listings))
        return listings

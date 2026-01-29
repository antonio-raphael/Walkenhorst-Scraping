#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 31 12:13:59 2025
"""

# This script serves as a commented example of the scraping script ran to collect walmart data
# there exist individual scripts for individual products, but this should serve as the commented
# reference to undertsand what was done, this one scrapes data on coffee from walmart search
# Core async and utility libraries
import asyncio
import json
import math
import httpx
import nest_asyncio
import os

# URL encoding utility
from urllib.parse import urlencode

# Type hints
from typing import List, Dict

# Logging utility
from loguru import logger as log

# HTML parsing / XPath selection
from parsel import Selector

# Filesystem path handling
from pathlib import Path


cookies = {
# to be copied with each converted curl
}

headers = {
# to be copied with each converted curl
}


# Allows nested event loops (useful in notebooks or interactive environments)
nest_asyncio.apply()


def parse_search(html_text: str) -> tuple[list[dict], int]:
    """
    Parse a Walmart search result page and extract product items and total count.

    Parameters
    ----------
    html_text : str
        Raw HTML response text from a Walmart search page

    Returns
    -------
    tuple[list[dict], int]
        - List of product item dictionaries
        - Total number of results reported by Walmart
    """
    # Initialize an XPath selector on the HTML
    sel = Selector(text=html_text)

    # Extract embedded JSON state from Next.js (__NEXT_DATA__)
    data = sel.xpath('//script[@id="__NEXT_DATA__"]/text()').get()

    # If the JSON blob is missing, return empty results
    if not data:
        return [], 0

    # Parse the JSON string into a Python dictionary
    data = json.loads(data)

    try:
        # Navigate Walmart's internal JSON structure to reach search results
        item_stacks = (
            data["props"]["pageProps"]["initialData"]
            ["searchResult"]["itemStacks"]
        )
    except KeyError:
        # If Walmart changes their internal structure
        return [], 0

    # If no item stacks exist, return empty results
    if not item_stacks:
        return [], 0

    # Walmart stores items in the first stack
    stack = item_stacks[0]

    # Extract product items and total result count
    results = stack.get("items", [])
    total_results = stack.get("count", 0)

    return results, total_results


async def scrape_walmart_page(session: httpx.AsyncClient, query: str = "coffee", page=1):
    """
    Scrape a single Walmart search results page.

    Parameters
    ----------
    session : httpx.AsyncClient
        Active HTTP session
    query : str
        Search keyword
    page : int
        Search results page number

    Returns
    -------
    httpx.Response
        HTTP response object
    """
    # Construct the Walmart search URL with query parameters
    url = "https://www.walmart.com/search?" + urlencode(
        {
            "q": query,
            "page": page,
            "facet": "fulfillment_method:Pickup",
            "affinityOverride": "default",
        },
    )

    # Retry logic with exponential backoff (anti-blocking strategy)
    for attempt in range(5):
        resp = await session.get(url)
        if resp.status_code == 200:
            return resp
        # Wait increasingly longer between retries
        await asyncio.sleep(2 ** attempt)

    # If all retries fail, assume blocking
    raise Exception(f"Blocked: {url}")

    # Redundant code (never reached, but left unchanged as requested)
    resp = await session.get(url)
    assert resp.status_code == 200, "request is blocked"
    return resp


async def scrape_search(
    search_query: str,
    session: httpx.AsyncClient,
    max_scrape_pages: int = None
) -> List[Dict]:
    """
    Scrape all Walmart search result pages for a given query.

    Parameters
    ----------
    search_query : str
        Search keyword
    session : httpx.AsyncClient
        Active HTTP session
    max_scrape_pages : int, optional
        User-defined limit on number of pages to scrape

    Returns
    -------
    List[Dict]
        List of scraped product records
    """
    # Log start of scraping
    log.info(f"scraping Walmart search for the keyword {search_query}")

    # Scrape the first search page
    _resp_page1 = await scrape_walmart_page(query=search_query, session=session)
    results, total_items = parse_search(_resp_page1.text)

    # Calculate total number of available pages (40 items per page)
    max_page = math.ceil(total_items / 40)

    # Walmart caps search pagination at 25 pages
    if max_page > 25:
        max_page = 25

    # Apply user-defined page limit if provided
    if max_scrape_pages and max_scrape_pages < max_page:
        max_page = max_scrape_pages

    # Log remaining pages to scrape
    log.info(f"scraped the first search, remaining ({max_page - 1}) more pages")

    # Scrape remaining pages concurrently
    for response in await asyncio.gather(
        *[
            scrape_walmart_page(query=search_query, page=i, session=session)
            for i in range(2, max_page + 1)
        ]
    ):
        # Extend results with items from each page
        results.extend(parse_search(response.text)[0])

    # Log final success message
    log.success(f"scraped {len(results)} products from walmart search")

    return results


async def main():
    """
    Main entry point:
    - Creates output directory
    - Initializes HTTP client
    - Scrapes Walmart search results
    - Saves data to JSON file
    """
    # Define export directory
    export_dir = Path("/Users/antonioraphael/Documents/PROJECT-CLONES/Data-Storage")
    export_dir.mkdir(parents=True, exist_ok=True)

    # Output file path
    output_file = export_dir / "walmart_coffee.json"

    # Create an async HTTP session with headers, cookies, and timeout
    async with httpx.AsyncClient(
        headers=headers,
        cookies=cookies,
        timeout=30
    ) as session:
        # Scrape Walmart search results
        results = await scrape_search(
            search_query="coffee",
            session=session,
            max_scrape_pages=25
        )

    # Write scraped data to JSON file
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    # Confirmation message
    print(f"Saved {len(results)} products to {output_file}")


# Run the async main function when executed as a script
if __name__ == "__main__":
    asyncio.run(main())

    
    
    
    
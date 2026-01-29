#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 14 16:32:37 2026

@author: antonioraphael
"""

import asyncio
import json
import math
import httpx
import nest_asyncio
import os
from urllib.parse import urlencode
from typing import List, Dict
from loguru import logger as log
from parsel import Selector
from pathlib import Path


nest_asyncio.apply()

def parse_search(html_text: str) -> tuple[list[dict], int]:
    sel = Selector(text=html_text)
    data = sel.xpath('//script[@id="__NEXT_DATA__"]/text()').get()

    if not data:
        return [], 0

    data = json.loads(data)

    try:
        item_stacks = (
            data["props"]["pageProps"]["initialData"]
            ["searchResult"]["itemStacks"]
        )
    except KeyError:
        return [], 0

    if not item_stacks:
        return [], 0

    stack = item_stacks[0]

    results = stack.get("items", [])
    total_results = stack.get("count", 0)

    return results, total_results

async def scrape_walmart_page(session:httpx.AsyncClient, query:str="sauce", page=1):
    """scrape a single walmart search page"""
    url = "https://www.walmart.com/search?" + urlencode(
        {
            "q": query,
            "page": page,
            "facet": "fulfillment_method:Pickup",
            "affinityOverride": "default",
          
        },
    )
    for attempt in range(5):
        resp = await session.get(url)
        if resp.status_code == 200:
            return resp
        await asyncio.sleep(2 ** attempt)  # exponential backoff
    raise Exception(f"Blocked: {url}")
    resp = await session.get(url)
    assert resp.status_code == 200, "request is blocked"
    return resp


async def scrape_search(search_query:str, session:httpx.AsyncClient, max_scrape_pages:int=None) -> List[Dict]:
    """scrape Walmart search pages"""
    # scrape the first search page first
    log.info(f"scraping Walmart search for the keyword {search_query}")
    _resp_page1 = await scrape_walmart_page(query=search_query, session=session)
    results, total_items = parse_search(_resp_page1.text)
    # get the total number of pages available
    max_page = math.ceil(total_items / 40)
    if max_page > 25: # the max number of pages is 25
        max_page = 25

    # get the number of total pages to scrape
    if max_scrape_pages and max_scrape_pages < max_page:
        max_page = max_scrape_pages
    
    # scrape the remaining search pages
    log.info(f"scraped the first search, remaining ({max_page-1}) more pages")
    for response in await asyncio.gather(
        *[scrape_walmart_page(query=search_query, page=i, session=session) for i in range(2, max_page+1)]
    ):
        results.extend(parse_search(response.text)[0])
    log.success(f"scraped {len(results)} products from walmart search")
    return results

async def main():
    export_dir = Path("/Users/antonioraphael/Documents/PROJECT-CLONES/Data-Storage")
    export_dir.mkdir(parents=True, exist_ok=True)

    output_file = export_dir / "walmart-sauce.json"

    async with httpx.AsyncClient(
        headers=headers,
        cookies=cookies,
        timeout=30
    ) as session:
        results = await scrape_search(
            search_query="sauce",
            session=session,
            max_scrape_pages=25
        )

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(results)} products to {output_file}")


if __name__ == "__main__":
    asyncio.run(main())
    
    
    
    
    
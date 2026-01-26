#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 15 17:02:53 2026

@author: antonioraphael
"""

import pandas as pd
from rapidfuzz.process import extractOne
import unicodedata
import re

Catalogue = pd.read_csv("/Users/antonioraphael/Documents/PROJECT-CLONES/Data-Storage/Walkenhorst/Scraped_Catalogue.csv")
Products = pd.read_csv("/Users/antonioraphael/Documents/PROJECT-CLONES/Walkenhorst-Scraping/01. Scraping/Scraped-JSON-Files/Full-Products-Data/Products_Categories.csv")


Catalogue = Catalogue[Catalogue["Category"] == "CRACKERS"]
Products =  Products[Products["source_file"] == "walmart_crackers.json"]

Products = Products.rename(columns = {'name':'item', 'price':'price_walmart', 'priceInfo.unitPrice':'walmart_price_ounce'})

Catalogue['item'] = Catalogue['item'].str.lower()
Products['item'] = Products['item'].str.lower()

def normalize_text(x: str) -> str:
    if x is None:
        return None

    # lowercase
    x = x.lower()

    # UTF-8 → ASCII transliteration
    x = (
        unicodedata
        .normalize("NFKD", x)
        .encode("ascii", "ignore")
        .decode("ascii")
    )

    # remove numbers (including decimals)
    x = re.sub(r"\d+(\.\d+)?", " ", x)

    # keep letters + spaces only
    x = re.sub(r"[^a-z ]", " ", x)

    # remove units / pack tokens
    x = re.sub(r"\b(kg|g|lb|oz|pack|pcs|pc|x)\b", " ", x)

    # collapse whitespace
    x = re.sub(r"\s+", " ", x).strip()

    return x

Catalogue["item_normalized"] = Catalogue["item"].astype(str).map(normalize_text)
Products["item_normalized"] = Products["item"].astype(str).map(normalize_text)

results = Catalogue['item_normalized'].apply(lambda x: extractOne(query = x,
                                                               choices =Products['item_normalized'],
                                                               score_cutoff=85))

Catalogue['match'] = results
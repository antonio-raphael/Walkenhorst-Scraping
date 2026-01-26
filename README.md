# Walkenhorst-Scraping

This repository is the code for a Telecom-Paris webscraping course project completed by the following authors:
Louise Gatty, Alice Petillon, Charles Pyle, Antonio Raphael, and Anne Thebaud.


# Project Overview

This project aims to measure the degree to which Walkenhorst is over charging for products resulting
from its monopoly status within the California Prison system. 

In the California Department of Corrections and Rehabilitation (CDCR), if friends or family wish to send
food, toiletries or other approved goods to an inmate, they must purchase these good through the one CDCR
approved vendor, Walkenhorst. Due to the fact that prison inmates are quite literally a captive population,
and that there is no other choice in vendor or option for purchasing goods, Walkenhorst has monopoly power
over this population.

This project uses price data PDF scraped from the Walkenhorst family visits catalogue, and webscraped from
Walmart to quantify the hypothesized monopoly power Walkenhorst exerts within the CDCR prison system.

# Directory Tree

```text
.
├── 01. Scraping
│   ├── PDF-Scraping
│   │   ├── Catalogue-PDF-Scraping.rmd
│   │   └── Catalogue_Recoded_Categories.csv
│   ├── Scraped-JSON-Files
│   │   ├── Full-Products-Data
│   │   │   ├── Products_Categories.csv
│   │   │   └── Products_Only.csv
│   │   ├── seafood.json
│   │   ├── walmart-honey.json
│   │   ├── walmart-hot-sauce.json
│   │   ├── walmart-sauce.json
│   │   ├── walmart-spreads.json
│   │   ├── walmart_CREAMERS.json
│   │   ├── walmart_Diet-Supplements.json
│   │   ├── walmart_Drink-Mixes.json
│   │   ├── walmart_Milk-drink-mix.json
│   │   ├── walmart_Nutrition-Supplements.json
│   │   ├── walmart_antacidtablets.json
│   │   ├── walmart_asian_food.json
│   │   ├── walmart_beans.json
│   │   ├── walmart_bottled-water.json
│   │   ├── walmart_bread.json
│   │   ├── walmart_candy.json
│   │   ├── walmart_candy_sugarfree.json
│   │   ├── walmart_cereal.json
│   │   ├── walmart_cheese.json
│   │   ├── walmart_chips.json
│   │   ├── walmart_coffee.json
│   │   ├── walmart_condiments.json
│   │   ├── walmart_cookies.json
│   │   ├── walmart_coughdrops.json
│   │   ├── walmart_crackers.json
│   │   ├── walmart_fruit-drink-mix.json
│   │   ├── walmart_fruit.json
│   │   ├── walmart_granolabars.json
│   │   ├── walmart_macncheese.json
│   │   ├── walmart_meals.json
│   │   ├── walmart_meats.json
│   │   ├── walmart_nuts.json
│   │   ├── walmart_oatmeal.json
│   │   ├── walmart_olives.json
│   │   ├── walmart_pasta.json
│   │   ├── walmart_pastries.json
│   │   ├── walmart_popcorn.json
│   │   ├── walmart_potatoesgravy.json
│   │   ├── walmart_ramen.json
│   │   ├── walmart_rice.json
│   │   ├── walmart_sauces.json
│   │   ├── walmart_seafood.json
│   │   ├── walmart_sides.json
│   │   ├── walmart_soda-drink-mix.json
│   │   ├── walmart_soft-drinks-177oz.json
│   │   ├── walmart_soft-drinks.json
│   │   ├── walmart_soups.json
│   │   ├── walmart_spicesseasonings.json
│   │   ├── walmart_sports-drink-mix.json
│   │   ├── walmart_spreads.json
│   │   ├── walmart_sweeteners.json
│   │   ├── walmart_taco&tortillas.json
│   │   ├── walmart_tea.json
│   │   └── walmart_vegetables.json
│   └── Web-Scraping
│       ├── Bottled-Water-Scraping.py
│       ├── Coffee-Scraping.py
│       ├── Condiments-Scraping.py
│       ├── Cookies-Scraping.py
│       ├── Creamers-Scraping.py
│       ├── Diet-Supplements-Scraping.py
│       ├── Drink-Mixes-Scraping.py
│       ├── Fruit-Drink-Mix-Scraping.py
│       ├── Honey-Scraping.py
│       ├── Hot-Sauce-Scraping.py
│       ├── Milk-Drink-Mix-Scraping.py
│       ├── Nutrition-Supplements-Scraping.py
│       ├── Sauce-Scraping.py
│       ├── Soda-Drink-Mix-Scraping.py
│       ├── Soft-Drinks-Scraping.py
│       ├── Spreads-Scraping.py
│       ├── Webscraping-Crackers-Attempt-1.py
│       ├── soft-drinks-17oz-scraping.py
│       └── sports-drink-mix-scraping.py
├── 02. Combining-Merging
│   ├── 01. Combining-Scraped-Data.rmd
│   ├── 02. Df-merging-all.ipynb
│   ├── 03. Creating-Analysis-File.rmd
│   └── Archived
│       ├── Fuzzy-Join-First-Attempt.rmd
│       └── Fuzzy-Join-Second-Attempt.py
├── 03. Analysis
│   ├── Analysis-Data
│   │   └── Analysis-Data.csv
│   └── T-Testing.rmd
├── README.md
├── Submissions
│   ├── Submission-Jan-06
│   │   ├── Code_assignment-Modified-Coffee.ipynb
│   │   └── Code_assignment2.ipynb
│   └── Submission-Jan-16
│       ├── Assigment-3.ipynb
│       └── Walmart_Walkenhorst_data.csv
└── Walkenhorst-Scraping.Rproj
```
# File Descriptions and Objectives

## 01. Scraping

In this sub-directory 01. scraping, there are two main tasks carried out as a part of the data collection
process.

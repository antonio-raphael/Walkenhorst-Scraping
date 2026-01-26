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
├── 01. Scraping
│   ├── PDF-Scraping
│   │   ├── Catalogue-PDF-Scraping.rmd
│   │   └── Catalogue_Recoded_Categories.csv
│   ├── Scraped-JSON-Files
│   │   ├── Full-Products-Data
│   │   │   ├── Products_Categories.csv
│   │   │   └── Products_Only.csv
│   │   └── Scraped-Data.zip
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
│   ├── 02. Products-Fuzzy-Merging.ipynb
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
│   ├── Initial Research and Data Plan.pdf
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

The first is PDF scraping the family visits catalogue. Walkenhorst has two different CDCR catalogues,
the main catalogue which proved to be too unstructured to PDF scrape effectively or accurately,
and the family visits catalogue. The difference between family visits catalogue is simply a list of
products that can be given to an inmate during a family visit. A phone call with a Walkenhorst 
representative informed the project that the prices were the same between the two catalogues, the difference
is when the products are given to the inmate.

The family visits catalogue is a highly structured, table format, PDF document largely consisting of
food items for purchase. Information for each item includes brand, item, price, weight, and kosher status,
as well as an overarching product category.

The PDF file is scraped in R and exported as a CSV.

The second is webscraping. This was done in python, and the team worked to scrape relevant walmart data
by querying relevant search terms at the walmart webpage, and extracting the JSON file that underlies
the results webpage.

## 02. Combining-Merging

Combining and Merging has three different parts. The first is combining all the JSON files and
performing initial data cleaning, the second is perform a fuzzy merge of the Walmart and Walkenhorst 
product files, and finally is additional data cleaning of the merged file to create the analysis file.


### 02-01 Walmart Data Cleaning
The Walmart data required substantial cleaning before being ready for the merge. The first and most
basic steps were to combine all of the individudal json files that came from scraping different queries
into one master products file, and selecting all the of the variables relevant to the product.

Once this was accomplished, the data required further cleaning and preparation for the fuzzy merge.
Fuzzy merging performs best when the text strings are short, free from special characters, and 
free from numbers. Extensive string cleaning was preformed to remove things such as counts, weights,
or numeric descriptors which would hinder the match process.

Next was to standardize the price-per-unit variable for all of the products. Some products were expressed in
cents per ounce, dollars per ounce, dollars per pound etc. and needed to be standardized to dollars
per ounce.

Once all strings were cleaned and price-per-units were standardized, the decision was made to aggregate
the price-per-units by products which were the same products of differing sizes. Fuzzy merging does
not match well on numbers, and given time and resource constraints it was not possible to match products
exactly on product and weight. So aggregate price-per-unit ratios were created by simply taking the mean
of the price-per-unit variable for otherwise identical products.

This data cleaning was done in R.

### 02-02 Fuzzy Joining


### 02-03 Analysis File

After fuzzy merging, a little more data cleaning remained. This was mostly to keep the relevant
variables in the data set for analysis, such as the price-per-unit variables for Walmart and Walkenhorst,
and the product categories. The decided that our main variable for analysis would be the percent markup
between Walkenhorst and Walmart. This uses the price per unit ratio for matched products, the price from
Walmart is subtracted from the price from Walkenhorst, divided by the price from Walmart, and multiplied
by 100:

$((P_{Walkenhorst} - P_{Walmart}) / P_{Walmart})*100$


Once the mark-up was calcuated, there were some outliers that needed to be addressed. First, there 
are some observations for ramen that Walmart has priced as a fraction of a cent per ounce. Whether
this is an error with how Walmart had calculated the price-per-unit or if it is a extreme example of
an scale economy is unclear. However since these generated mark ups in the 10,000% range these
observations were dropped from the data.

Second, there were some observations that had a markup greater than 400%, some of these observations
were the economy-of-scale ramen with mark ups, and some were due to poor/incorrect matching. These
observations were sorted manually, with acceptable matches kept in the data and the rest dropped.

This file was then exported and used for all statistical testing and data visuals.

## 03. Analysis

This performs various aspects of the data visualization and statistical testing. For the purposes
of this project we simply preform t tests and and visualize the data.

### 01. T-Testing

This tests for differences between the price per unit between walmart and walkenhorst, and if 
the percent mark up is greater than 0. There are a total of 16 different tests performed by category
for each variable for a total of 32 tests, and we apply a Benjamini–Hochberg correction to ensure 
validity of our results.

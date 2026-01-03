#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 31 12:13:59 2025

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


cookies = {
    'isoLoc': 'US_CA_t3',
    'ak_bmsc': '877AE438107B2DE94BADF22B0F0F9C8B~000000000000000000000000000000~YAAQSgw0F6PAMimbAQAAav6deh4M8XmIaON3JS3eoCcvBYjujUvR3OJupBw4FOq91zc4uKoUEA1wmPWr9BmB6ufHXTHy2pw+zvPGwL8QgPwrwyj1Gh1oA0P+jVuxjCPfVhgs7Gz8CSUHRziaeyF0Oyt5nIIgbX43BbiJ1+tFHhqiK2hrFJFic8O68LsJFtrQowb/5MnO3TPPFG5aqVtI98kQMbZYyuXRxsWYImkPa+ucNd/bF48pompnA3iwfnE14lOeL26LJ7slLCqQl1bhD6e+GMV3bYDxFopr7PsdF5NWXepTx/NsH6FMyCJEaFPKtx8kl02kcJTtFaSwTtRAyOGnUOsSsLWiu08x1Ius/XgtRgIBa8dbxsXH92qCcYH5hchZIOPoFe7Lz2SNZQ==',
    '_astc': 'a22480d45857f897e9fad5b101bbd4c9',
    'vtc': 'Ww797XfCXjPdCKSB1_NagE',
    'bstc': 'Ww797XfCXjPdCKSB1_NagE',
    'pxcts': 'cf5335bd-e737-11f0-9bc9-15382157f881',
    '_pxvid': 'cf532842-e737-11f0-9bc9-335a987b950d',
    'adblocked': 'true',
    'ACID': '3302e177-9fb8-4e24-aa37-b68b4a3d930e',
    '_m': '9',
    'hasACID': 'true',
    'abqme': 'false',
    'xpth': 'x-o-mart%2BB2C~x-o-mverified%2Bfalse',
    'xpa': '54G-6|M02Ld|Nhde5|O8qqV|OkuK4|TCS94|aVtuC|c4yNV|eqxfC|jM1ax|xByE7',
    'exp-ck': '54G-61Nhde51O8qqV1OkuK41TCS941aVtuC2eqxfC1',
    '_pxhd': '705b473cb5e9fddfc3e5f8618e3beb3050251f71554d43a7fb20e52e59911dee:cf746b56-e737-11f0-9dfc-c73d2b70bc72',
    '_px3': '1e2623c3ef53cf944cad96a69c84afbf1ca418b1b7345513010e24d1d47059a4:lOUfbLDTJSZsXV3O/A3HpPck+jg8MsDU8sL/XgKpHQ8cDOTRfvtzN30U6+euz4HkoMKzd2ahw718UANX/PGp3Q==:1000:Esc9XIQDUHI7yjgz/eVWXLvR3HuPpSi7sH16znieBA0f3xlAFAPTsdm7aGrs5G6rninhfDX0iAJm7qkOgJEuPaY2WHiPWsVG5jXHFujQm4Ew8o5+S6BMdOCTrRCfxF3ibComGlNf7epqr/veZzbbceIl3m0Cnc1RH5LLqYyOUQ6eDhTK/T2HQA2rwEiFmn90Yx4/usvEXRiECyW2ZXx0ASR2AKvcOfZPd4rmycHgAxOlu3WVrwnTqVfKsenqRKMQP9xYAHiqsYh/pUnPX7YJAuFBwZLjUma6mGDCyEHzFnGpTufWTt2DVLzs/YwYiXP2kUn96gHjOUz6oJb/HAq+EQ==',
    'io_id': '6f59a67e-9252-4071-b2e3-f27b12ea77a4',
    'bm_mi': 'E5238EAA2586D618B5DE2406C04BA1EF~YAAQSgw0F+vBMimbAQAAiw+eeh6WfhvAxsxzYj8azsF6DdEAz2ueanSllfFl5FUeW//bRTx0y0kEHYXDh5CaydbOQas+lA/vFCCriW5GwGH9mRw415zo+4yEOqNv8TznvaDd70+gQ4V8rgzBxEDZ6v4AjyYc83NRCVuq9D6OU58fc3TaMyrS77NRhdpsdZ5jaOYnviTRoZ9X3BGrnaSvzZPyXUoviau+WfotcfRe7m2UZ94nz3RXyCDPZeiJV0XgQkuRbUEap1itS0n8tt/9aOXDWhQBHRDQYE7A324f0ITSSAvP4HU0buPXidVKeog0fwUK~1',
    '_intlbu': 'false',
    '_shcc': 'US',
    'assortmentStoreId': '5766',
    'hasLocData': '1',
    'locDataV3': 'eyJpc0RlZmF1bHRlZCI6ZmFsc2UsImlzRXhwbGljaXQiOmZhbHNlLCJpbnRlbnQiOiJTSElQUElORyIsInBpY2t1cCI6W3sibm9kZUlkIjoiNTc2NiIsImRpc3BsYXlOYW1lIjoiTW9yZ2FuIEhpbGwgU3VwZXJjZW50ZXIiLCJhZGRyZXNzIjp7InBvc3RhbENvZGUiOiI5NTAzNyIsImFkZHJlc3NMaW5lMSI6IjE3MCBDT0NIUkFORSBQTFoiLCJjaXR5IjoiTW9yZ2FuIEhpbGwiLCJzdGF0ZSI6IkNBIiwiY291bnRyeSI6IlVTIn0sImdlb1BvaW50Ijp7ImxhdGl0dWRlIjozNy4xNDkyMTEsImxvbmdpdHVkZSI6LTEyMS42NTUxNzJ9LCJzY2hlZHVsZWRFbmFibGVkIjp0cnVlLCJ1blNjaGVkdWxlZEVuYWJsZWQiOnRydWUsInN0b3JlSHJzIjoiMDY6MDAtMjM6MDAiLCJhbGxvd2VkV0lDQWdlbmNpZXMiOlsiQ0EiXSwic3VwcG9ydGVkQWNjZXNzVHlwZXMiOlsiV0lSRUxFU1NfU0VSVklDRSIsIlBJQ0tVUF9DVVJCU0lERSIsIlBJQ0tVUF9JTlNUT1JFIiwiUElDS1VQX1NQRUNJQUxfRVZFTlQiXSwidGltZVpvbmUiOiJQU1QiLCJzZWxlY3Rpb25UeXBlIjoiTFNfU0VMRUNURUQifSx7Im5vZGVJZCI6IjU4ODQifSx7Im5vZGVJZCI6IjMwMjMifSx7Im5vZGVJZCI6IjQxNzQifSx7Im5vZGVJZCI6IjU0MzUifSx7Im5vZGVJZCI6IjI0ODYifSx7Im5vZGVJZCI6IjIwMDIifSx7Im5vZGVJZCI6IjMxMjMifSx7Im5vZGVJZCI6IjIxMTkifV0sInNoaXBwaW5nQWRkcmVzcyI6eyJsYXRpdHVkZSI6MzcuMTY3Njg1NywibG9uZ2l0dWRlIjotMTIxLjc3MDgzMzcsInBvc3RhbENvZGUiOiI5NTE0MSIsImNpdHkiOiJTYW4gSm9zZSIsInN0YXRlIjoiQ0EiLCJjb3VudHJ5Q29kZSI6IlVTQSIsImxvY2F0aW9uQWNjdXJhY3kiOiJsb3ciLCJnaWZ0QWRkcmVzcyI6ZmFsc2UsInRpbWVab25lIjoiQW1lcmljYS9Mb3NfQW5nZWxlcyIsImFsbG93ZWRXSUNBZ2VuY2llcyI6WyJDQSJdfSwiYXNzb3J0bWVudCI6eyJub2RlSWQiOiI1NzY2IiwiZGlzcGxheU5hbWUiOiJNb3JnYW4gSGlsbCBTdXBlcmNlbnRlciIsImludGVudCI6IlBJQ0tVUCJ9LCJpbnN0b3JlIjpmYWxzZSwiZGVsaXZlcnkiOnsibm9kZUlkIjoiNTg4NCIsImRpc3BsYXlOYW1lIjoiU2FuIEpvc2UgU3VwZXJjZW50ZXIiLCJhZGRyZXNzIjp7InBvc3RhbENvZGUiOiI5NTExOCIsImFkZHJlc3NMaW5lMSI6IjUwOTUgQUxNQURFTiBFWFBZIiwiY2l0eSI6IlNhbiBKb3NlIiwic3RhdGUiOiJDQSIsImNvdW50cnkiOiJVUyJ9LCJnZW9Qb2ludCI6eyJsYXRpdHVkZSI6MzcuMjU1NDgzLCJsb25naXR1ZGUiOi0xMjEuODgwMTM1fSwic2NoZWR1bGVkRW5hYmxlZCI6ZmFsc2UsInVuU2NoZWR1bGVkRW5hYmxlZCI6ZmFsc2UsImFjY2Vzc1BvaW50cyI6W3siYWNjZXNzVHlwZSI6IkRFTElWRVJZX0FERFJFU1MifV0sImlzRXhwcmVzc0RlbGl2ZXJ5T25seSI6ZmFsc2UsImFsbG93ZWRXSUNBZ2VuY2llcyI6WyJDQSJdLCJzdXBwb3J0ZWRBY2Nlc3NUeXBlcyI6WyJERUxJVkVSWV9BRERSRVNTIl0sInRpbWVab25lIjoiQW1lcmljYS9Mb3NfQW5nZWxlcyIsInN0b3JlQnJhbmRGb3JtYXQiOiJXYWxtYXJ0IFN1cGVyY2VudGVyIiwic2VsZWN0aW9uVHlwZSI6IkxTX1NFTEVDVEVEIn0sImlzZ2VvSW50bFVzZXIiOmZhbHNlLCJtcERlbFN0b3JlQ291bnQiOjAsInJlZnJlc2hBdCI6MTc2NzMxMDMzNzY4NSwidmFsaWRhdGVLZXkiOiJwcm9kOnYyOjMzMDJlMTc3LTlmYjgtNGUyNC1hYTM3LWI2OGI0YTNkOTMwZSJ9',
    'locGuestData': 'eyJpbnRlbnQiOiJTSElQUElORyIsImlzRXhwbGljaXQiOmZhbHNlLCJzdG9yZUludGVudCI6IlBJQ0tVUCIsIm1lcmdlRmxhZyI6ZmFsc2UsImlzRGVmYXVsdGVkIjpmYWxzZSwicGlja3VwIjp7Im5vZGVJZCI6IjU3NjYiLCJ0aW1lc3RhbXAiOjE3NjcyODg3Mzc2NzYsInNlbGVjdGlvblR5cGUiOiJMU19TRUxFQ1RFRCIsInNlbGVjdGlvblNvdXJjZSI6IklQX1NOSUZGRURfQllfTFMifSwic2hpcHBpbmdBZGRyZXNzIjp7InRpbWVzdGFtcCI6MTc2NzI4ODczNzY3NiwidHlwZSI6InBhcnRpYWwtbG9jYXRpb24iLCJnaWZ0QWRkcmVzcyI6ZmFsc2UsInBvc3RhbENvZGUiOiI5NTE0MSIsImRlbGl2ZXJ5U3RvcmVMaXN0IjpbeyJub2RlSWQiOiI1ODg0IiwidHlwZSI6IkRFTElWRVJZIiwidGltZXN0YW1wIjoxNzY3Mjg1MTAwNTY3LCJkZWxpdmVyeVRpZXIiOm51bGwsInNlbGVjdGlvblR5cGUiOiJMU19TRUxFQ1RFRCIsInNlbGVjdGlvblNvdXJjZSI6IklQX1NOSUZGRURfQllfTFMifV0sImNpdHkiOiJTYW4gSm9zZSIsInN0YXRlIjoiQ0EifSwicG9zdGFsQ29kZSI6eyJ0aW1lc3RhbXAiOjE3NjcyODg3Mzc2NzYsImJhc2UiOiI5NTE0MSJ9LCJtcCI6W10sIm1zcCI6eyJub2RlSWRzIjpbIjU4ODQiLCIzMDIzIiwiNDE3NCIsIjU0MzUiLCIyNDg2IiwiMjAwMiIsIjMxMjMiLCIyMTE5Il0sInRpbWVzdGFtcCI6MTc2NzI4ODczNzY3Nn0sIm1wRGVsU3RvcmVDb3VudCI6MCwic2hvd0xvY2FsRXhwZXJpZW5jZSI6ZmFsc2UsInNob3dMTVBFbnRyeVBvaW50IjpmYWxzZSwibXBVbmlxdWVTZWxsZXJDb3VudCI6MCwidmFsaWRhdGVLZXkiOiJwcm9kOnYyOjMzMDJlMTc3LTlmYjgtNGUyNC1hYTM3LWI2OGI0YTNkOTMwZSJ9',
    '_pxde': '7c48cbbab6301ed66497462084e823b726f6fea14ba2e18b419f37ef555eb8a2:eyJ0aW1lc3RhbXAiOjE3NjcyODg3NDE4OTQsImZfa2IiOjAsImlwY19pZCI6W10sImluY19pZCI6WyJiNDFlNmM1ZjM3ZDdjMTYyNmMxNTU2ZjI0MzMyY2EwYyIsIjFmOTAwY2YyNTM3ZDg1YmY3ZGRmMjZjMmZhMTdlMGQ3Il19',
    'xpm': '1%2B1767288739%2BWw797XfCXjPdCKSB1_NagE~%2B0',
    'xptwj': 'uz:f844fd5152c0c21aa6c1:8dGNQG80wcq6VJWvdyohVPI/DpxQCVPV7bOdKgIT7XcP5P9gblSUzPLRnBsb6hXjol/TjAaX2yvinbqWm5BqSspB0PmZlj9HHnaq3i41Zzxnt0raOarEd3OokC9V6lbUuBAmyFtysU3vulSrpFiygNQi5HzC+TyOMLu9zhlRLw==',
    'akavpau_p2': '1767289372~id=bbef33c5465483d0e5ecb8471b6605b5',
    'xptc': '_m%2B9~assortmentStoreId%2B5766',
    'xptwg': '1040479759:10688A01C4EB520:27E0649:4B32C195:EDF2A6E9:30B271E0:',
    'TS012768cf': '01a68f80b11e2bcf838bcf30ed6003297766eec1b94a1bd6cfc26fd07fe933a8d9ad6aae6dab78d1f4bd6ccf172ad2e3b1bd070247',
    'TS01a90220': '01a68f80b11e2bcf838bcf30ed6003297766eec1b94a1bd6cfc26fd07fe933a8d9ad6aae6dab78d1f4bd6ccf172ad2e3b1bd070247',
    'TS2a5e0c5c027': '0828b058d1ab20004fe765867e0e32186f65ccb517c2beacc55d0af0beedced8ec05fcfcb300f9740834779c5f1130006173088e63d094df52c9accfba655295b214a9365fdbcb226b14054a516333fe1e38a9d5e9d13133ef4982c99f522c18',
    'if_id': 'FMEZARSFG48mVRJgSSjEJAutNIpC7WntCdEVSR+hTxyzWU0KBLA60d5F0CQd3Q7ZCzLFNG+U9rGlsIusRVFPltfCpFr22KkVgR6rlLnZeROt0UhI5RVOef7taW0lXy+NFDjB/yufm68I44jsnFLYYqZD6HRtxf/DyH91PgA4dLquGxrDloz8Hnvw3FEIaQw6DmfS+cPbOSiUdgqtZ+V/C0GHYJaECNoUIzle60JEWW1UN1O+g28QaNbhu3Arul8puGbfHeY7mEkjYxahLgoEtnlJZX9PySVbHWlo4h9xrtZLHXtOQF60uQxg3PlSuWljwy2OYeJRwW3H/Oficg==',
    'TS016ef4c8': '01352185ccdb546da094d0729a4f2470a1265b72ef8beb59b21eee3d6d95a1a1f1dec1c598f91982bd42017af406b78a4bfe008c85',
    'TS01f89308': '01352185ccdb546da094d0729a4f2470a1265b72ef8beb59b21eee3d6d95a1a1f1dec1c598f91982bd42017af406b78a4bfe008c85',
    'TS8cb5a80e027': '089082aa26ab2000c9f5f37cdc35561478595762439a7297a2d950ffb5dd60dcdeff6da309aaf15a08562d65031130006dcdc6fab49502df3149a01409f331a31976f5a9279cd473dad044af1288a261b460c72b1de89004444b5dc0ed5c3fd3',
    'bm_sv': '3A5C706D73F13CA13BCB228A3E7FDB58~YAAQSgw0F57SMimbAQAAfO6eeh4XD1YGbW/g5CmhqJBrdiiD1aJNTZgqFdaOWLWgMGDbj/dVh43l8q89JHrgCXINOd9MEDSi4z0NZ4TD8iwfvySeQbMz7zD6ttVBN3x3Q9e59cxatde309sPLmcEuqSzKXqPijlw6r1tPbMDgV9QnjrSp3xuRReysi+7ZAykHODPnl3z9G+US4GPgeQr+6KAn7KWwz+kYp253L+81ax5JWaNDVje69BPPwlqRuQfVXU=~1',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'downlink': '10',
    'dpr': '2',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
    # 'cookie': 'isoLoc=US_CA_t3; ak_bmsc=877AE438107B2DE94BADF22B0F0F9C8B~000000000000000000000000000000~YAAQSgw0F6PAMimbAQAAav6deh4M8XmIaON3JS3eoCcvBYjujUvR3OJupBw4FOq91zc4uKoUEA1wmPWr9BmB6ufHXTHy2pw+zvPGwL8QgPwrwyj1Gh1oA0P+jVuxjCPfVhgs7Gz8CSUHRziaeyF0Oyt5nIIgbX43BbiJ1+tFHhqiK2hrFJFic8O68LsJFtrQowb/5MnO3TPPFG5aqVtI98kQMbZYyuXRxsWYImkPa+ucNd/bF48pompnA3iwfnE14lOeL26LJ7slLCqQl1bhD6e+GMV3bYDxFopr7PsdF5NWXepTx/NsH6FMyCJEaFPKtx8kl02kcJTtFaSwTtRAyOGnUOsSsLWiu08x1Ius/XgtRgIBa8dbxsXH92qCcYH5hchZIOPoFe7Lz2SNZQ==; _astc=a22480d45857f897e9fad5b101bbd4c9; vtc=Ww797XfCXjPdCKSB1_NagE; bstc=Ww797XfCXjPdCKSB1_NagE; pxcts=cf5335bd-e737-11f0-9bc9-15382157f881; _pxvid=cf532842-e737-11f0-9bc9-335a987b950d; adblocked=true; ACID=3302e177-9fb8-4e24-aa37-b68b4a3d930e; _m=9; hasACID=true; abqme=false; xpth=x-o-mart%2BB2C~x-o-mverified%2Bfalse; xpa=54G-6|M02Ld|Nhde5|O8qqV|OkuK4|TCS94|aVtuC|c4yNV|eqxfC|jM1ax|xByE7; exp-ck=54G-61Nhde51O8qqV1OkuK41TCS941aVtuC2eqxfC1; _pxhd=705b473cb5e9fddfc3e5f8618e3beb3050251f71554d43a7fb20e52e59911dee:cf746b56-e737-11f0-9dfc-c73d2b70bc72; _px3=1e2623c3ef53cf944cad96a69c84afbf1ca418b1b7345513010e24d1d47059a4:lOUfbLDTJSZsXV3O/A3HpPck+jg8MsDU8sL/XgKpHQ8cDOTRfvtzN30U6+euz4HkoMKzd2ahw718UANX/PGp3Q==:1000:Esc9XIQDUHI7yjgz/eVWXLvR3HuPpSi7sH16znieBA0f3xlAFAPTsdm7aGrs5G6rninhfDX0iAJm7qkOgJEuPaY2WHiPWsVG5jXHFujQm4Ew8o5+S6BMdOCTrRCfxF3ibComGlNf7epqr/veZzbbceIl3m0Cnc1RH5LLqYyOUQ6eDhTK/T2HQA2rwEiFmn90Yx4/usvEXRiECyW2ZXx0ASR2AKvcOfZPd4rmycHgAxOlu3WVrwnTqVfKsenqRKMQP9xYAHiqsYh/pUnPX7YJAuFBwZLjUma6mGDCyEHzFnGpTufWTt2DVLzs/YwYiXP2kUn96gHjOUz6oJb/HAq+EQ==; io_id=6f59a67e-9252-4071-b2e3-f27b12ea77a4; bm_mi=E5238EAA2586D618B5DE2406C04BA1EF~YAAQSgw0F+vBMimbAQAAiw+eeh6WfhvAxsxzYj8azsF6DdEAz2ueanSllfFl5FUeW//bRTx0y0kEHYXDh5CaydbOQas+lA/vFCCriW5GwGH9mRw415zo+4yEOqNv8TznvaDd70+gQ4V8rgzBxEDZ6v4AjyYc83NRCVuq9D6OU58fc3TaMyrS77NRhdpsdZ5jaOYnviTRoZ9X3BGrnaSvzZPyXUoviau+WfotcfRe7m2UZ94nz3RXyCDPZeiJV0XgQkuRbUEap1itS0n8tt/9aOXDWhQBHRDQYE7A324f0ITSSAvP4HU0buPXidVKeog0fwUK~1; _intlbu=false; _shcc=US; assortmentStoreId=5766; hasLocData=1; locDataV3=eyJpc0RlZmF1bHRlZCI6ZmFsc2UsImlzRXhwbGljaXQiOmZhbHNlLCJpbnRlbnQiOiJTSElQUElORyIsInBpY2t1cCI6W3sibm9kZUlkIjoiNTc2NiIsImRpc3BsYXlOYW1lIjoiTW9yZ2FuIEhpbGwgU3VwZXJjZW50ZXIiLCJhZGRyZXNzIjp7InBvc3RhbENvZGUiOiI5NTAzNyIsImFkZHJlc3NMaW5lMSI6IjE3MCBDT0NIUkFORSBQTFoiLCJjaXR5IjoiTW9yZ2FuIEhpbGwiLCJzdGF0ZSI6IkNBIiwiY291bnRyeSI6IlVTIn0sImdlb1BvaW50Ijp7ImxhdGl0dWRlIjozNy4xNDkyMTEsImxvbmdpdHVkZSI6LTEyMS42NTUxNzJ9LCJzY2hlZHVsZWRFbmFibGVkIjp0cnVlLCJ1blNjaGVkdWxlZEVuYWJsZWQiOnRydWUsInN0b3JlSHJzIjoiMDY6MDAtMjM6MDAiLCJhbGxvd2VkV0lDQWdlbmNpZXMiOlsiQ0EiXSwic3VwcG9ydGVkQWNjZXNzVHlwZXMiOlsiV0lSRUxFU1NfU0VSVklDRSIsIlBJQ0tVUF9DVVJCU0lERSIsIlBJQ0tVUF9JTlNUT1JFIiwiUElDS1VQX1NQRUNJQUxfRVZFTlQiXSwidGltZVpvbmUiOiJQU1QiLCJzZWxlY3Rpb25UeXBlIjoiTFNfU0VMRUNURUQifSx7Im5vZGVJZCI6IjU4ODQifSx7Im5vZGVJZCI6IjMwMjMifSx7Im5vZGVJZCI6IjQxNzQifSx7Im5vZGVJZCI6IjU0MzUifSx7Im5vZGVJZCI6IjI0ODYifSx7Im5vZGVJZCI6IjIwMDIifSx7Im5vZGVJZCI6IjMxMjMifSx7Im5vZGVJZCI6IjIxMTkifV0sInNoaXBwaW5nQWRkcmVzcyI6eyJsYXRpdHVkZSI6MzcuMTY3Njg1NywibG9uZ2l0dWRlIjotMTIxLjc3MDgzMzcsInBvc3RhbENvZGUiOiI5NTE0MSIsImNpdHkiOiJTYW4gSm9zZSIsInN0YXRlIjoiQ0EiLCJjb3VudHJ5Q29kZSI6IlVTQSIsImxvY2F0aW9uQWNjdXJhY3kiOiJsb3ciLCJnaWZ0QWRkcmVzcyI6ZmFsc2UsInRpbWVab25lIjoiQW1lcmljYS9Mb3NfQW5nZWxlcyIsImFsbG93ZWRXSUNBZ2VuY2llcyI6WyJDQSJdfSwiYXNzb3J0bWVudCI6eyJub2RlSWQiOiI1NzY2IiwiZGlzcGxheU5hbWUiOiJNb3JnYW4gSGlsbCBTdXBlcmNlbnRlciIsImludGVudCI6IlBJQ0tVUCJ9LCJpbnN0b3JlIjpmYWxzZSwiZGVsaXZlcnkiOnsibm9kZUlkIjoiNTg4NCIsImRpc3BsYXlOYW1lIjoiU2FuIEpvc2UgU3VwZXJjZW50ZXIiLCJhZGRyZXNzIjp7InBvc3RhbENvZGUiOiI5NTExOCIsImFkZHJlc3NMaW5lMSI6IjUwOTUgQUxNQURFTiBFWFBZIiwiY2l0eSI6IlNhbiBKb3NlIiwic3RhdGUiOiJDQSIsImNvdW50cnkiOiJVUyJ9LCJnZW9Qb2ludCI6eyJsYXRpdHVkZSI6MzcuMjU1NDgzLCJsb25naXR1ZGUiOi0xMjEuODgwMTM1fSwic2NoZWR1bGVkRW5hYmxlZCI6ZmFsc2UsInVuU2NoZWR1bGVkRW5hYmxlZCI6ZmFsc2UsImFjY2Vzc1BvaW50cyI6W3siYWNjZXNzVHlwZSI6IkRFTElWRVJZX0FERFJFU1MifV0sImlzRXhwcmVzc0RlbGl2ZXJ5T25seSI6ZmFsc2UsImFsbG93ZWRXSUNBZ2VuY2llcyI6WyJDQSJdLCJzdXBwb3J0ZWRBY2Nlc3NUeXBlcyI6WyJERUxJVkVSWV9BRERSRVNTIl0sInRpbWVab25lIjoiQW1lcmljYS9Mb3NfQW5nZWxlcyIsInN0b3JlQnJhbmRGb3JtYXQiOiJXYWxtYXJ0IFN1cGVyY2VudGVyIiwic2VsZWN0aW9uVHlwZSI6IkxTX1NFTEVDVEVEIn0sImlzZ2VvSW50bFVzZXIiOmZhbHNlLCJtcERlbFN0b3JlQ291bnQiOjAsInJlZnJlc2hBdCI6MTc2NzMxMDMzNzY4NSwidmFsaWRhdGVLZXkiOiJwcm9kOnYyOjMzMDJlMTc3LTlmYjgtNGUyNC1hYTM3LWI2OGI0YTNkOTMwZSJ9; locGuestData=eyJpbnRlbnQiOiJTSElQUElORyIsImlzRXhwbGljaXQiOmZhbHNlLCJzdG9yZUludGVudCI6IlBJQ0tVUCIsIm1lcmdlRmxhZyI6ZmFsc2UsImlzRGVmYXVsdGVkIjpmYWxzZSwicGlja3VwIjp7Im5vZGVJZCI6IjU3NjYiLCJ0aW1lc3RhbXAiOjE3NjcyODg3Mzc2NzYsInNlbGVjdGlvblR5cGUiOiJMU19TRUxFQ1RFRCIsInNlbGVjdGlvblNvdXJjZSI6IklQX1NOSUZGRURfQllfTFMifSwic2hpcHBpbmdBZGRyZXNzIjp7InRpbWVzdGFtcCI6MTc2NzI4ODczNzY3NiwidHlwZSI6InBhcnRpYWwtbG9jYXRpb24iLCJnaWZ0QWRkcmVzcyI6ZmFsc2UsInBvc3RhbENvZGUiOiI5NTE0MSIsImRlbGl2ZXJ5U3RvcmVMaXN0IjpbeyJub2RlSWQiOiI1ODg0IiwidHlwZSI6IkRFTElWRVJZIiwidGltZXN0YW1wIjoxNzY3Mjg1MTAwNTY3LCJkZWxpdmVyeVRpZXIiOm51bGwsInNlbGVjdGlvblR5cGUiOiJMU19TRUxFQ1RFRCIsInNlbGVjdGlvblNvdXJjZSI6IklQX1NOSUZGRURfQllfTFMifV0sImNpdHkiOiJTYW4gSm9zZSIsInN0YXRlIjoiQ0EifSwicG9zdGFsQ29kZSI6eyJ0aW1lc3RhbXAiOjE3NjcyODg3Mzc2NzYsImJhc2UiOiI5NTE0MSJ9LCJtcCI6W10sIm1zcCI6eyJub2RlSWRzIjpbIjU4ODQiLCIzMDIzIiwiNDE3NCIsIjU0MzUiLCIyNDg2IiwiMjAwMiIsIjMxMjMiLCIyMTE5Il0sInRpbWVzdGFtcCI6MTc2NzI4ODczNzY3Nn0sIm1wRGVsU3RvcmVDb3VudCI6MCwic2hvd0xvY2FsRXhwZXJpZW5jZSI6ZmFsc2UsInNob3dMTVBFbnRyeVBvaW50IjpmYWxzZSwibXBVbmlxdWVTZWxsZXJDb3VudCI6MCwidmFsaWRhdGVLZXkiOiJwcm9kOnYyOjMzMDJlMTc3LTlmYjgtNGUyNC1hYTM3LWI2OGI0YTNkOTMwZSJ9; _pxde=7c48cbbab6301ed66497462084e823b726f6fea14ba2e18b419f37ef555eb8a2:eyJ0aW1lc3RhbXAiOjE3NjcyODg3NDE4OTQsImZfa2IiOjAsImlwY19pZCI6W10sImluY19pZCI6WyJiNDFlNmM1ZjM3ZDdjMTYyNmMxNTU2ZjI0MzMyY2EwYyIsIjFmOTAwY2YyNTM3ZDg1YmY3ZGRmMjZjMmZhMTdlMGQ3Il19; xpm=1%2B1767288739%2BWw797XfCXjPdCKSB1_NagE~%2B0; xptwj=uz:f844fd5152c0c21aa6c1:8dGNQG80wcq6VJWvdyohVPI/DpxQCVPV7bOdKgIT7XcP5P9gblSUzPLRnBsb6hXjol/TjAaX2yvinbqWm5BqSspB0PmZlj9HHnaq3i41Zzxnt0raOarEd3OokC9V6lbUuBAmyFtysU3vulSrpFiygNQi5HzC+TyOMLu9zhlRLw==; akavpau_p2=1767289372~id=bbef33c5465483d0e5ecb8471b6605b5; xptc=_m%2B9~assortmentStoreId%2B5766; xptwg=1040479759:10688A01C4EB520:27E0649:4B32C195:EDF2A6E9:30B271E0:; TS012768cf=01a68f80b11e2bcf838bcf30ed6003297766eec1b94a1bd6cfc26fd07fe933a8d9ad6aae6dab78d1f4bd6ccf172ad2e3b1bd070247; TS01a90220=01a68f80b11e2bcf838bcf30ed6003297766eec1b94a1bd6cfc26fd07fe933a8d9ad6aae6dab78d1f4bd6ccf172ad2e3b1bd070247; TS2a5e0c5c027=0828b058d1ab20004fe765867e0e32186f65ccb517c2beacc55d0af0beedced8ec05fcfcb300f9740834779c5f1130006173088e63d094df52c9accfba655295b214a9365fdbcb226b14054a516333fe1e38a9d5e9d13133ef4982c99f522c18; if_id=FMEZARSFG48mVRJgSSjEJAutNIpC7WntCdEVSR+hTxyzWU0KBLA60d5F0CQd3Q7ZCzLFNG+U9rGlsIusRVFPltfCpFr22KkVgR6rlLnZeROt0UhI5RVOef7taW0lXy+NFDjB/yufm68I44jsnFLYYqZD6HRtxf/DyH91PgA4dLquGxrDloz8Hnvw3FEIaQw6DmfS+cPbOSiUdgqtZ+V/C0GHYJaECNoUIzle60JEWW1UN1O+g28QaNbhu3Arul8puGbfHeY7mEkjYxahLgoEtnlJZX9PySVbHWlo4h9xrtZLHXtOQF60uQxg3PlSuWljwy2OYeJRwW3H/Oficg==; TS016ef4c8=01352185ccdb546da094d0729a4f2470a1265b72ef8beb59b21eee3d6d95a1a1f1dec1c598f91982bd42017af406b78a4bfe008c85; TS01f89308=01352185ccdb546da094d0729a4f2470a1265b72ef8beb59b21eee3d6d95a1a1f1dec1c598f91982bd42017af406b78a4bfe008c85; TS8cb5a80e027=089082aa26ab2000c9f5f37cdc35561478595762439a7297a2d950ffb5dd60dcdeff6da309aaf15a08562d65031130006dcdc6fab49502df3149a01409f331a31976f5a9279cd473dad044af1288a261b460c72b1de89004444b5dc0ed5c3fd3; bm_sv=3A5C706D73F13CA13BCB228A3E7FDB58~YAAQSgw0F57SMimbAQAAfO6eeh4XD1YGbW/g5CmhqJBrdiiD1aJNTZgqFdaOWLWgMGDbj/dVh43l8q89JHrgCXINOd9MEDSi4z0NZ4TD8iwfvySeQbMz7zD6ttVBN3x3Q9e59cxatde309sPLmcEuqSzKXqPijlw6r1tPbMDgV9QnjrSp3xuRReysi+7ZAykHODPnl3z9G+US4GPgeQr+6KAn7KWwz+kYp253L+81ax5JWaNDVje69BPPwlqRuQfVXU=~1',
}

nest_asyncio.apply()

def parse_search(html_text:str) -> tuple[list[dict], int]:
    """extract search results from search HTML response"""
    sel = Selector(text=html_text)
    data = sel.xpath('//script[@id="__NEXT_DATA__"]/text()').get()
    data = json.loads(data)

    total_results = data["props"]["pageProps"]["initialData"]["searchResult"]["itemStacks"][0]["count"]
    results = data["props"]["pageProps"]["initialData"]["searchResult"]["itemStacks"][0]["items"]
    return results, total_results

async def scrape_walmart_page(session:httpx.AsyncClient, query:str="crackers", page=1):
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

    output_file = export_dir / "walmart_crackers.json"

    async with httpx.AsyncClient(
        headers=headers,
        cookies=cookies,
        timeout=30
    ) as session:
        results = await scrape_search(
            search_query="crackers",
            session=session,
            max_scrape_pages=25
        )

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(results)} products to {output_file}")


if __name__ == "__main__":
    asyncio.run(main())
    
    
    
    
    
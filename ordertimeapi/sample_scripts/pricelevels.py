#!/usr/bin/env python
# coding: utf-8
"""
Retrieves all the Price Levesl for Products
"""

import sys
import os
sys.path.append(os.path.abspath('..'))

import pandas as pd
from api import ordertime
from api.enum_dicts import RecordTypeEnum
from auth import pw, api_key, user

# records to retrieve at a time
RECORDSPERPAGE = 1000

ot = ordertime.OrderTime(user, pw, api_key)
filters = {"IsActive": True, "TypeRef.Id": 130}
ot.build_payload(RecordTypeEnum["Price Level"], **filters)
totals = ot.calc_pages()
ot.url = "https://services.ordertime.com/api/entityref"
responses = ot.get_all_pages(totals.numpages)

dfs = [pd.json_normalize(r.json()) for r in responses]
items = pd.concat(dfs)

items.to_csv("pricelevels_header.csv", index=False)

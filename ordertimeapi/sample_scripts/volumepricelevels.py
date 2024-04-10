#!/usr/bin/env python
# coding: utf-8

"""
Retrieve the volume price levels data from OrderTime
and outputs to a csv file.
"""

import sys
import os
sys.path.append(os.path.abspath('..'))

import pandas as pd
from api import ordertime
from api.enum_dicts import RecordTypeEnum
from auth import pw, api_key, user


RECORDSPERPAGE = 1000

ot = ordertime.OrderTime(user, pw, api_key)

ENUMTYPE = RecordTypeEnum["Volume Price Level Detail"]  # 284

ot.build_payload(ENUMTYPE)

totals = ot.calc_pages()

responses = ot.get_all_pages(totals.numpages)

dfs = [pd.json_normalize(r.json()) for r in responses]

items = pd.concat(dfs)

itemsfinal = items[
    ["Id", "FromQuantity", "Rate", "PriceLevelRef.Name", "PriceLevelRef.Id"]
]

itemsfinal.to_csv("volume_discount_details.csv",
                  sep=",", index=False)

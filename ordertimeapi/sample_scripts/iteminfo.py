#!/usr/bin/env python
# coding: utf-8

"""
Retrieves the product info from the OrderTime app
"""
import sys
import os
sys.path.append(os.path.abspath('..'))

import pandas as pd
from api import ordertime
from api.enum_dicts import RecordTypeEnum
from auth import pw, api_key, user

# records to retrieve at a time
RECORDSPERPAGE = 900

"""I have to use enums 101, 103, 107
because 101 does not return information about price level id
"""
catalogparts = (
    RecordTypeEnum["Part Item"],  # 101
    RecordTypeEnum["Non Part Item"],  # "Non Part Item": 103
    RecordTypeEnum["Assembly Item"],
)  # "Assembly Item": 107

ot = ordertime.OrderTime(user, pw, api_key)

responses = []
for item in catalogparts:
    ot.build_payload(item, IsActive=True)
    totals = ot.calc_pages()
    response = ot.get_all_pages(totals.numpages)
    responses += response

dfs = [pd.json_normalize(r.json()) for r in responses]
items = pd.concat(dfs)


# Retrieve the Some Custom Fields
items["ProductGroup1"] = items.CustomFields.apply(lambda x: x[0]["Value"])
items["ProductGroup2"] = items.CustomFields.apply(lambda x: x[9]["Value"])
items["ProductGroup3"] = items.CustomFields.apply(lambda x: x[10]["Value"])
items["MinOrderQty"] = (items.CustomFields.apply(lambda x: x[6]["Value"])
                        .fillna(1))
items["ItemCust9"] = items.CustomFields.apply(lambda x: x[8]["Value"])
items.rename(columns={"Price": "BasePrice"}, inplace=True)

items.drop(["CustomFields"], axis=1).to_csv(
    "product_info.csv", index=False
)

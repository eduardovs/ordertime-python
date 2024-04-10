# coding: utf-8
"""
Check if the base prices in OrderTime
matches what we have in our Excel data sources
Also checks for duplicated entries in the
Excel data source.
"""

import datetime
import configparser
from pathlib import Path
import pandas as pd
import numpy as np
import filecomparerdaff as daff

today = datetime.datetime.today()

conf = configparser.ConfigParser()
conf.read("../filesources.ini")
PRICINGFOLDER = Path(conf["PricingFiles"]["folder"])
EXCELFILE = "ExcelPricing.xlsx"
xl_vs_ot = Path("../ordertimedata/excelvsordertime")

cols = ["FullName", "Description", "BasePrice", "MinOrderQty"]
df = pd.read_csv("../ordertimedata/product_info.csv", usecols=cols)

xl = pd.read_excel(PRICINGFOLDER.joinpath(EXCELFILE))
xlallcols = pd.read_csv(
    "../diffs between NC and Excel/products_with_esssential_fields.csv"
)

suppldupes = xlallcols.duplicated(subset=["SupplierProductCode"], keep=False)
namedupes = xlallcols.duplicated(subset=["ProductName"], keep=False)
alldupes = (suppldupes) | (namedupes)
dupes = xlallcols[alldupes].dropna(subset=["SupplierProductCode"])
if not dupes.empty:
    dupes[["ProductName", "SupplierProductCode", "File Path"]].to_excel(
        xl_vs_ot / "duplicated_entries_in_excel.xlsx"
    )

xl = xl[["ProductName", "SalesDescription", "SellQty1Price", "SellQty1"]]

xl = xl.rename(
    columns={
        "ProductName": "FullName",
        "SalesDescription": "Description",
        "SellQty1Price": "BasePrice",
        "SellQty1": "MinOrderQty",
    }
)

comp = df.merge(
    xl, on="FullName", how="outer", suffixes=("_nc", "_xl"), indicator=True
)

comp[comp["_merge"] == "right_only"].to_csv(
    xl_vs_ot.joinpath(f"BasePrices_OnlyInExcel_{today:%Y-%m-%d}.csv"),
    index=False,
)
comp[comp["_merge"] == "left_only"].to_csv(
    xl_vs_ot.joinpath(f"BasePrices_OnlyInAllOrders_{today:%Y-%m-%d}.csv"),
    index=False,
)

# Work with only data that are in both sources
both = comp[comp["_merge"] == "both"].copy()

both = both.assign(
    PriceDiff=np.round(both["BasePrice_nc"] - both["BasePrice_xl"], 3)
)

both = both.assign(SameDesc=both["Description_nc"] == both["Description_xl"])

both = both.assign(
    MinQtyDiff=np.round(both["MinOrderQty_nc"] - both["MinOrderQty_xl"], 3)
)

diffprice = both[both.PriceDiff != 0.0].drop("_merge", axis=1)

diffprice[
    ["FullName", "Description_nc", "BasePrice_xl", "BasePrice_nc", "PriceDiff"]
].to_csv(
    xl_vs_ot.joinpath(f"BaseBasePrice_Diffs_{today:%Y-%m-%d_%H%M}.csv"),
    index=False,
)

diffdesc = both[both.SameDesc == False].drop("_merge", axis=1)

diffdesc.head()

if not diffdesc.empty:
    diffdesc.to_csv(
        xl_vs_ot.joinpath(f"Description_Diffs_{today:%Y-%m-%d}.csv"),
        index=False,
    )

diffminord = diffprice = both[both.MinQtyDiff != 0.0].drop("_merge", axis=1)

diffminord.head()

if not diffminord.empty:
    diffminord[
        ["FullName", "Description_nc", "MinOrderQty_xl", "MinOrderQty_nc"]
    ].to_csv(
        xl_vs_ot.joinpath(f"MinOrderQty_Diffs_{today:%Y-%m-%d_%H%M}.csv"),
        index=False,
    )

# Check changes in file BasePrices_OnlyInAllOrders_*.csv
tocompare = daff.get_newest_file(
    path=xl_vs_ot.joinpath("BasePrices_OnlyInAllOrders*.csv")
)

# output = daff.daff_compare(tocompare[0],tocompare[1] )
OUTPUT = daff.daff_compare(*tocompare)

daff.make_csvreport(
    OUTPUT,
    xl_vs_ot.joinpath(f"OnlyInAllOrdersDiffs_{today:%Y-%m-%d_%H%M}.csv"),
)

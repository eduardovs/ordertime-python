# coding: utf-8
"""
Some helper functions to better work with the
daff utility (https://paulfitz.github.io/daff/)
"""

import os
import glob
import io
import subprocess
import pandas as pd


def get_newest_file(path="../costs/itemcosts*.csv"):

    """
    Retrieves the last to files sorted by
    the date the file change
    """
    newest = sorted(glob.iglob(path), key=os.path.getctime)
    return newest[-2:]


def daff_compare(olderfile, newerfile):

    """Invokes the daff utility with simple arguments"""
    diffs = subprocess.Popen(
        ["daff", "--context", "0", olderfile, newerfile],
        stdout=subprocess.PIPE
    )
    out, err = diffs.communicate()
    return out


def make_csvreport(daffoutput, csv_outfile):

    """
    Extracts from the output produced by daff
    relevant information about line differences.
    """
    df = pd.read_csv(io.BytesIO(daffoutput), encoding="utf-8")
    df.fillna("", inplace=True)
    df[(df["@@"] != "")
       & (df["@@"] != "...")
       & (df["@@"] != ":")].to_csv(csv_outfile)

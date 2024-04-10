"""
A basic python module to interact with OrderTime's REST API
"""

import json
from math import ceil
from collections import namedtuple
import requests


RECORDSPERPAGE = 990


class OrderTime:
    """API Wrapper Class"""

    postdict = {"Type": 130}

    def __init__(self, email, password, api_key):
        self.email = email
        self.password = password
        self.api_key = api_key
        self.url = "https://services.ordertime.com/api/list"
        self.headers = {
            "email": email,
            "password": password,
            "Content-Type": "application/json",
            "apiKey": api_key,
        }

    @classmethod
    def build_payload(cls, enumtype, **filters):
        """
        Builds a json payload for querying OrderTime
        Example:
        {
            "Type": 190,
            "Filters" : [
                {
                    "PropertyName": "IsActive",
                    "Operator": 1,
                    "FilterValueArray": "1"
                }]
            }
        """
        payload_dict = {"Type": enumtype}

        if filters:
            filterlist = []
            for k, v in filters.items():
                if isinstance(v, list):
                    prop = {
                        "PropertyName": k,
                        "FilterValueArray": v[0],
                        "Operator": v[1].get("Operator", 1),
                    }
                else:
                    prop = {"PropertyName": k, "FilterValueArray": v}
                filterlist.append(prop)
            payload_dict["Filters"] = filterlist
        cls.postdict.update(payload_dict)

        return payload_dict

    def calc_pages(self, rec_per_page=RECORDSPERPAGE):
        """
        Calculates the number of pages according to the
        RECORDSPERPAGE parameter in order to retrieve all
        records from the query.
        """
        payload = json.dumps(self.postdict)
        try:
            response = requests.request("PUT",
                                        self.url,
                                        headers=self.headers,
                                        data=payload,
                                        timeout=60
                                        )
            response.raise_for_status()
            info = namedtuple("info", ["numpages", "totalrecords"])
            result = info(ceil(int(response.text) / rec_per_page),
                          int(response.text)
                          )

            return result
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err) from err

    def get_all_pages(self, totalpages, rec_per_page=RECORDSPERPAGE):
        """
        Because of the rate limit of n records per page,
        this method builds a list of all responses needed to
        build the final dataframe.
        """
        responses = []
        payload_dict = self.postdict
        payload_dict["NumberOfRecords"] = rec_per_page
        s = requests.Session()

        for p in range(1, totalpages + 1):
            payload_dict["PageNumber"] = p
            print(f"Retrieving Page {p} of {totalpages}")
            payload = json.dumps(payload_dict)

            try:
                r = s.request("POST", self.url,
                              headers=self.headers, data=payload)
                r.raise_for_status()
                responses.append(r)
            except requests.exceptions.HTTPError as err:
                raise SystemExit(err) from err
        return responses

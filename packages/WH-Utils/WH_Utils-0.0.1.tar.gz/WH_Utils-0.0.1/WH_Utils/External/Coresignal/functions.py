"""
Simple functions for interacting with coresignal in a progromatic way
"""


import pandas as pd
import requests
import numpy as np
import os, sys
import json
from pydantic import Json, HttpUrl
from typing import List, Dict, Optional, Any


def get_person_by_id(id_number: int, auth_dict: Dict[str, Any]) -> Any:
    """
    This function just fetches a person by the id number from coresignal.

    Args
    -------
        id_number: int
            the coresignal id number. Should be aquired from a coresignal query.
        auth_dict: auth_dict
            the authorization header. Check here for instructions on how to make this

    Returns
    ----------

        person_data: dict
            the full response from coresignal
    """
    url = "https://api.coresignal.com/dbapi/v1/collect/member/{}".format(id_number)
    response = requests.get(url, headers=auth_dict)
    if response.status_code == 200:
        data = json.loads(response.text)
        return data
    else:
        raise ValueError(
            "Bad Response Code. Response code: {}".format(response.status_code)
        )


def get_person_by_url(linkedin_url: str, auth_dict: Dict[str, Any]) -> Any:
    """Returns the coresignal for a person given the persons linkedin URL

    Args
    -----

        linkedin_url: HttpUrl
            the linkedin url of the person you want info on

        auth_dict: auth_dict
            the authorization header. Check here for instructions on how to make this

    Returns
    ----------

        person_data: dict
            the full json style respose of the person from coresignal

    """
    if linkedin_url.endswith("/"):
        linkedin_url = linkedin_url[:-1]
    short_hand = linkedin_url.split("/")[-1]
    url = "https://api.coresignal.com/dbapi/v1/collect/member/{}".format(short_hand)
    response = requests.get(url, headers=auth_dict)
    if response.status_code == 200:
        data = json.loads(response.text)
        return data
    else:
        raise ValueError(
            "Bad Response Code. Response code: {}".format(response.status_code)
        )


def find_employees_by_work_history(
    company_url: str, auth_dict: Dict[str, Any]
) -> List[int]:
    """
    Finds a list of employee coresignal id numbers based on where the employees worked.

    Args
    ------

        company_url: HttpUrl
            the linkedin_url of the company you want to find past employees of.

        auth_dict: auth_dict
            the authorization header. Check here for instructions on how to make this

    Returns
    --------

        person_ids: List[int]
            list of strings where every item is an id number of someone who worked at the target comapny
    """
    url = "https://api.coresignal.com/dbapi/v1/search/member"
    data = {"experience_company_linkedin_url": company_url}
    response = requests.post(url, headers=auth_dict, json=data)
    t = [int(x) for x in response.text[1:-1].split(",")]
    return t

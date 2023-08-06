"""
Simple functions for interacting with coresignal in a progromatic way
"""

# TODO: make these return WH objects

import pandas as pd
import requests
import numpy as np
import os, sys
import json
from pydantic import Json, HttpUrl
from typing import List, Dict, Optional, Any, Union
from WH_Utils.Objects.Company import Company
from WH_Utils.Objects.Prospect import Prospect
from WH_Utils.Objects.Enums import EventType
from datetime import datetime


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


def coresingal_to_prospect(
    id: Union[int, str],
    auth_dict: Dict[str, Any],
    event_type: Optional[EventType] = None,
    company_id: Optional[str] = None,
) -> Prospect:
    """Build a prospect from an ID or linkedin url

    Args:
        id: Union[int, str]
            coresignal id (int) or linkedin url (str)

        auth_dict: Dict[str, Any]
            the authorization header. Check here for instructions on how to make this

        event_type: Optional[EventType]
            if you know the event type for this prospect you can add it here

        company_id: Optional[Union[int, str]]
            If they are associated with a company event and we know the company, put it here (the WH id)

    Returns
    --------
        prospect: Prospect
            the prospect

    """
    # TODO: cut down extra data
    # TODO: add company id to extra data

    if isinstance(id, int):
        data = get_person_by_id(id, auth_dict)

    elif isinstance(id, str):
        data = get_person_by_url(id, auth_dict)

    else:
        raise ValueError("ID data type is weird")

    data_dict = {
        "id": None,
        "name": data["name"],
        "location": data["location"],
        "coresignal_id": data["id"],
        "linkedin_url": data["url"],
        "picture": data["logo_url"],
        "event_type": event_type,
        "full_data": data,
        "analytics": None,
        "date_created": None,
        "last_modified": None,
    }

    prospect = Prospect(data_dict=data_dict, event_type=event_type)

    return prospect


def coresignal_to_company(id: Union[int, str], auth_dict: Dict[str, str]):
    path = "https://api.coresignal.com/dbapi/v1/linkedin/company/collect/{}".format(id)
    response = requests.get(path, headers=auth_dict)
    assert response.status_code == 200, "Bad Response Code: {}".format(response.text)
    response_data = response.json()

    data_dict = {
        "id": None,
        "name": response_data["name"],
        "coresignal_id": response_data["id"],
        "linkedin_url": response_data["url"],
        "industry": response_data["industry"],
        "description": response_data["description"],
        "location": response_data["headquarters_city"],
        "logo": response_data["logo_url"],
        "type": response_data["type"],
        "website": response_data["website"],
        "full_data": response_data,
        "created": datetime.now().date(),
        "last_modified": datetime.now().date(),
        "CIK": "Unknown",
    }

    return Company(data_dict=data_dict)

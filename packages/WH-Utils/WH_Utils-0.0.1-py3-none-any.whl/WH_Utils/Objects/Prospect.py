from datetime import datetime, date
from typing import Any, Optional, Union, List, Dict, Any
import requests
import uuid
import json
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

from pydantic import Json, HttpUrl

from WH_Utils.Objects.Enums import UserRank, EventType, CompanyType
from WH_Utils.Objects.Object_utils import (
    verify_json,
    verify_auth_header,
    minus_key,
    WH_DB_URL,
)
from WH_Utils.Utils import parse_linkedin_date

from dataclasses import dataclass


@dataclass
class Prospect:
    """
    Class attributes
        - id: Optional[str]
        - name: Optional[str]
        - location: Optional[str]
        - coresignal_id: Optional[int]
        - linkedin_url: Optional[HttpUrl]
        - picture: Optional[HttpUrl]
        - event_type: Optional[EventType]
        - company: Optional[str]
        - start_date: Optional[date]
        - end_date: Optional[date]
        - full_data: Optional[Any]
        - analytics: Optional[Any]
        - date_created: Optional[datetime]
        - last_modified: Optional[datetime]

    Initialization function:
        This function allows several combinations of parameters tha behave differently.

        if only `data_dict` parameter is passed in:
            a `User` object will be constructed from the data passed in via the dictionary. The data dict must
            have the same keys as the object itself.

        if `WH_ID` and `auth_header` are passed in:
            this will cause the program to attempt to pull the user from the WH database. User with that UUID
            must already exist in the database and the credentials must be valid and properly formatted.

        All other combinations of the first 5 parameters are invalid.

    Args
    -----
        WH_ID: Optional[str]
            the UUID of a user in the database

        auth_header: Optional[Dict[str, Any]]
            the authorization header for the WEALTHAWK database

        data_dict: Optional[Dict[str, Any]]
            data to construct a user from
    """

    id: Optional[str]
    name: Optional[str]
    location: Optional[str]
    coresignal_id: Optional[int]
    linkedin_url: Optional[HttpUrl]
    picture: Optional[HttpUrl]
    event_type: Optional[EventType]
    full_data: Optional[Any]
    analytics: Optional[Any]
    date_created: Optional[datetime]
    last_modified: Optional[datetime]

    class Config:
        arbitrary_types_allowed = True

    def __init__(
        self,
        WH_ID: Optional[str] = None,
        auth_header: Optional[Dict[str, Any]] = None,
        data_dict: Optional[Dict[str, Any]] = None,
        company_name: Optional[str] = None,
        event_type: Optional[EventType] = None,
    ) -> None:

        self.company = company_name
        self.event_type = event_type

        if WH_ID and auth_header:
            self._build_from_WH_db(WH_ID, auth_header)
        elif data_dict:
            self._build_from_data_dict(data_dict)
        else:
            raise ValueError("Invalid combination of init parameters")

    @property
    def languages(self) -> Optional[List[str]]:
        """
        parses full_data for prospect languages
        """
        if not self.full_data or "member_languages_collection" not in self.full_data:
            return None

        member_lang = self.full_data["member_languages_collection"]

        # iterate through language info to return a list of language names
        langs = [
            lang_data["member_language_list"]["language"]
            for lang_data in member_lang
            if "member_language_list" in lang_data
        ]

        if len(langs) == 0:
            return None
        else:
            return langs

    @property
    def age(self) -> Optional[int]:
        """
        simple estimator of age sets college graduation at 22 years old
        """
        if not self.full_data:
            return None

        try:
            # first we can try by finding when they graduated high school / college.
            date = None
            member_edu = self.full_data["member_education_collection"]
            education_table = pd.DataFrame.from_records(member_edu).fillna(
                {"title": "", "subtitle": ""}
            )

            high_school_edu = education_table[
                education_table.title.str.contains("high school", case=False)
            ].dropna(
                subset=["date_to"]
            )  # might be able to expand term list here
            if len(high_school_edu):
                date = list(high_school_edu.loc[:, "date_from"])[0]
                date = parse_linkedin_date(date)

            bach_edu = education_table[
                education_table.subtitle.str.contains("Bachelor", case=False)
            ].dropna(
                subset=["date_from"]
            )  # might be able to expand term list here
            if len(bach_edu):
                date = list(bach_edu.loc[:, "date_from"])[0]
                date = parse_linkedin_date(date)

            # we assume they are 18 at `date` if we have it
            if not date:
                return None

            birthdate = date - timedelta(days=18 * 365)
            time_delta = datetime.now() - birthdate
            return int(time_delta.days / 365)

        except:
            return None

    def _build_from_WH_db(
        self, WH_ID: Optional[str], auth_header: Dict[str, Any]
    ) -> None:
        verify_auth_header(auth_header)
        request = requests.get(
            WH_DB_URL + "/person", params={"personID": WH_ID}, headers=auth_header
        )
        content = request.json()

        for key in list(content.keys()):
            self.__dict__[key] = content[key]

        if not self.full_data or self.full_data == '"null"':
            self.full_data = {}

        if not self.analytics or self.analytics == '"null"':
            self.analytics = {}

        self.in_database = True

    def _build_from_data_dict(self, data: Dict[str, Any]) -> None:
        verify_json("client", data)
        for key in list(data.keys()):
            self.__dict__[key] = data[key]

        if not self.id:
            self.id = str(uuid.uuid4())
        self.in_database = False
        if not self.analytics:
            self.analytics = {}

        if not self.full_data:
            self.full_data = {}

    def send_to_db(self, auth_header: Dict[str, Any]) -> requests.Response:
        """
        Sends the current object to the WH Database

        It will try to figure out if the object is already in the database by looking at the initialization
        method by looking at the `in_database` attribute. For example, if you constructed the object using
        WH_auth credentials and a WH_ID, then obviously the object is in the DB and so the function will
        attempt a PUT request to update the user. If 'in_database' is `False` then it will attempt a `POST`
        request. It's python so its mutable obviously so change it if needed.

        Args
        ------
            auth_header: Dict[str, Any]
                the authorization header for the WH database. It should be a dict with at least the key
                'Authorization' where the value is the key generated by logging in

        Returns
        ---------
            response: requests.Response
                the response of the backend API to your request. If it was a sucessful ``POST`` request it will look like:

                 >>> exampleClient.send_to_db(WH_auth_dict).content.decode()

                 ``Not expecting client in database. Attempting Post request.``

                 ``'{"id":"1fd84bd0-779d-4a10-8c71-e2cf008d23ed"}'``

                But a successful ``PUT`` request will look like:

        """
        data = self.__dict__
        data = minus_key("in_database", data)
        url = WH_DB_URL + "/person"
        data["analytics"] = json.dumps(self.analytics)
        data["full_data"] = json.dumps(self.full_data)

        if self.in_database:
            response = requests.put(url, json=data, headers=auth_header)
        else:
            response = requests.post(url, json=data, headers=auth_header)

        if response.status_code != 200:
            raise ConnectionError(response.content)

        return response

    def __repr__(self) -> str:
        return "ProspectID: {} \n Name: {} \n Location: {}".format(
            self.id, self.name, self.location
        )

    def __str__(self) -> str:
        return "ProspectID: {} \n Name: {} \n Location: {}".format(
            self.id, self.name, self.location
        )

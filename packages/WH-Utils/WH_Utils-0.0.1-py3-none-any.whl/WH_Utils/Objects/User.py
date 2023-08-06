from typing import Any, Optional, Union, List, Dict, Any
import requests
import uuid
import json
from datetime import datetime, timedelta

from WH_Utils.Objects.Enums import UserRank
from WH_Utils.Objects.Object_utils import (
    verify_json,
    verify_auth_header,
    minus_key,
    WH_DB_URL,
)

from dataclasses import dataclass


@dataclass
class User:
    """
    Class attributes
        - id: Optional[str]
        - first_name: Optional[str]
        - last_name: Optional[str]
        - email: Optional[str]
        - other_info: Optional[Any]
        - rank: Optional[UserRank]
        - firebase_id: Optional[str]
        - created: Optional[datetime]
        - last_modified: Optional[datetime]


    Initialization function:
        This function allows several combinations of parameters tha behave differently.

        if only `data_dict` parameter is passed in:
            a `User` object will be constructed from the data passed in via the dictionary. The data dict must
            have the same keys as the object itself.

        if `WH_ID` and `auth_header` are passed in:
            this will cause the program to attempt to pull the user from the WH database. User with that UUID
            must already exist in the database and the credentials must be valid and properly formatted.

        All other combinations are invalid.

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
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    other_info: Optional[Any]
    rank: Optional[UserRank]
    firebase_id: Optional[str]
    created: Optional[datetime]
    last_modified: Optional[datetime]

    class Config:
        arbitrary_types_allowed = True

    def __init__(
        self,
        WH_ID: Optional[str] = None,
        auth_header: Optional[Dict[str, Any]] = None,
        data_dict: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Initialization function for user

        This function allows several combinations of parameters tha behave differently.

        if only `data_dict` parameter is passed in:
            a `User` object will be constructed from the data passed in via the dictionary. The data dict must
            have the same keys as the object itself.

        if `WH_ID` and `auth_header` are passed in:
            this will cause the program to attempt to pull the user from the WH database. User with that UUID
            must already exist in the database and the credentials must be valid and properly formatted.

        All other combinations are invalid.

        Args
        -----
            WH_ID: Optional[str]
                the UUID of a user in the database

            auth_header: Optional[Dict[str, Any]]
                the authorization header for the WEALTHAWK database

            data_dict: Optional[Dict[str, Any]]
                data to construct a user from

        """
        if WH_ID and auth_header:
            self._build_from_WH_db(WH_ID, auth_header)
        elif data_dict:
            self._build_from_data_dict(data_dict)
        else:
            raise ValueError("Invalid combination of init parameters")

    def _build_from_WH_db(self, WH_ID: str, auth_header: Dict[str, Any]) -> None:
        verify_auth_header(auth_header)
        request = requests.get(
            WH_DB_URL + "/user", params={"userID": WH_ID}, headers=auth_header
        )
        content = request.json()[0]
        if "detail" in list(content.keys()) and content["detail"] == "User Not Found":
            raise ValueError("User Not Found or bad auth")

        for key in list(content.keys()):
            self.__dict__[key] = content[key]

        # this is a hacky fix for the fact that the api wont send empty JSON types it just sends "null" which
        # breaks the verification on push
        if not self.other_info:
            self.other_info = {}

        self.in_database = True

    def _build_from_data_dict(self, data: Dict[str, Any]) -> None:
        verify_json("user", data)
        for key in list(data.keys()):
            self.__dict__[key] = data[key]

        if not self.id:
            self.id = str(uuid.uuid4())

        self.in_database = False

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

                    ``>>> exampleClient.send_to_db(WH_auth_dict).content.decode()``

                    ``Not expecting client in database. Attempting Post request.``

                    ``'{"id":"1fd84bd0-779d-4a10-8c71-e2cf008d23ed"}'``

                But a successful ``PUT`` request will look like:



        """
        data = self.__dict__
        data = minus_key("in_database", data)
        url = "https://db.wealthawk.com/user"
        data["other_info"] = json.dumps(self.other_info)

        if self.in_database:
            response = requests.put(url, json=data, headers=auth_header)
        else:
            response = requests.post(url, json=data, headers=auth_header)

        if response.status_code != 200:
            raise ConnectionError(response.content)

        return response

    def __repr__(self) -> str:
        return "UserID: {} \n Name: {}, {}\n Email: {}, \n Rank: {}".format(
            self.id, self.last_name, self.first_name, self.email, self.rank
        )

    def __str__(self) -> str:
        return "UserID: {} \n Name: {}, {}\n Email: {}, \n Rank: {}".format(
            self.id, self.last_name, self.first_name, self.email, self.rank
        )

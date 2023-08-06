from WH_Utils import Prospect, Company, Event
from WH_Utils.Connectors.Coresignal import (
    coresignal_to_company,
    coresingal_to_prospect,
    find_employees_by_work_history,
)
from WH_Utils.Analytics.Prospects import get_prospect_tags
from WH_Utils import EventType
from WH_Utils.Utils.test_utils import BASE_URL

import requests
import pandas as pd
import numpy as np
from datetime import datetime
from tqdm import tqdm

from typing import Dict, List, Optional

# TODO: Add analytics functionality to both functions here


def push_person(
    WH_auth_header: dict,
    prospect: Prospect,
    event_WH_ID: str,
    company_WH_ID: Optional[str] = None,
) -> None:
    """
    Pushes a prospect and all relational data to the WH backend

    Args:
        prospect: Prospect
            the person you want to push

        event_WH_ID: str
            the WH_ID of the event you want to push

        company_WH_ID: Optional[str]
            the WH_ID of the event you want to push

    Returns:
        None

    Raised:
        ConnectionError - If any of the pushes fail
    """
    response = prospect.send_to_db(WH_auth_header)
    assert (
        response.status_code == 200
    ), "There was an error pushing prospect {} to the DB: {}".format(
        prospect.id, response.text
    )

    prospect_id = response.json()["id"]

    relate_prospect_and_event_url = BASE_URL + "/relate/person_to_event"
    params = {"personID": prospect_id, "eventID": event_WH_ID}
    prospect_to_event_response = requests.post(
        relate_prospect_and_event_url, params=params, headers=WH_auth_header
    )

    assert (
        prospect_to_event_response.status_code == 200
    ), "There was a problem with the prospect to event relation: {}".format(
        prospect_to_event_response.text
    )

    if company_WH_ID:
        relate_prospect_and_company_url = BASE_URL + "/relate/person_to_company"
        params = {"personID": prospect_id, "companyID": company_WH_ID}
        prospect_to_company_response = requests.post(
            relate_prospect_and_company_url, params=params, headers=WH_auth_header
        )

        assert (
            prospect_to_company_response.status_code == 200
        ), "There was a problem with the prospect to event relation: {}".format(
            prospect_to_company_response.text
        )


def push_event(
    WH_auth_dict: dict,
    CS_auth_dict: dict,
    title: str,
    description: str,
    type: EventType,
    date: datetime.date,
    link: str,
    location: str,
    value: int,
    other_info: dict,
    linkedin_of_exited_company: Optional[str] = None,
    associated_people_coresignal_ids: Optional[List[int]] = None,
    associated_people_WH_ids: Optional[List[str]] = None,
    run_analytics: Optional[bool] = False,
) -> None:
    """
    This is a big boy. Given enough information it will handle all the data inputation for an event.
    We might want to rework this into a few different functions at some point.

    Args:
        WH_auth_dict: dict
            the authorization dict we always use for the WH backend
        CS_auth_dict: dict
            creds to use coresignal
        title: str
            title of the event
        description: str
            description of the event
        type: EventType
            type of the event
        date: datetime.date
            date of the event
        link: str
            link to the news article
        location: str
            where the event took place
        value: int
            value of the event
        other_info: dict
            any other info for the event
        linkedin_of_exited_company: Optional[str] = None
            self explanitory. only applyied for IPOs and aquisitions
        associated_people_coresignal_ids: Optional[List[int]] = None
            if you already ran the "get people at company" func
        associated_people_WH_ids: Optional[List[str]] = None
            if you want to use preformulated people
        run_analytics: Optional[bool] = False
            if you want to run analytics

    Returns:
        None

    Raises:
        AssertionError: If any thing goes wrong



    """

    # make company if applicable
    if linkedin_of_exited_company:
        if linkedin_of_exited_company[-1] == "/":
            linkedin_of_exited_company = linkedin_of_exited_company[:-1]
        shorthand_path = linkedin_of_exited_company.split("/")[-1]

        company = coresignal_to_company(shorthand_path, CS_auth_dict)
        company_push_response = company.send_to_db(WH_auth_dict)
        assert (
            company_push_response.status_code == 200
        ), "Problem pushing company: {}".format(company_push_response.text)
        company_id = company_push_response.json()["id"]

        industry = company.industry

    else:
        industry = None
        company = False

    # make event
    data_dict = {
        "id": None,
        "title": title,
        "description": description,
        "type": type,
        "date_of": date,
        "link": link,
        "location": location,
        "value": value,
        "other_info": other_info,
        "created": datetime.now(),
        "last_modified": datetime.now(),
    }

    event = Event(data_dict=data_dict)
    event_push_response = event.send_to_db(WH_auth_dict)
    assert event_push_response.status_code == 200, "Problem pushing event: {}".format(
        event_push_response.text
    )
    event_id = event_push_response.json()["id"]

    # gather prospects
    prospects = []

    if (
        not associated_people_coresignal_ids
        and not associated_people_WH_ids
        and linkedin_of_exited_company
    ):
        associated_people_coresignal_ids = find_employees_by_work_history(
            company.linkedin_url, auth_dict=CS_auth_dict
        )
        print(
            "Found {} people for this event".format(
                len(associated_people_coresignal_ids)
            )
        )

    if associated_people_coresignal_ids:
        print("making prospects")
        for id in tqdm(associated_people_coresignal_ids):
            try:
                prosp = coresingal_to_prospect(id, CS_auth_dict, type)
                prospects.append(prosp)
            except Exception as e:
                print("Problem with coresignal id {}: {}".format(id, e))

    if associated_people_WH_ids:
        for id in associated_people_coresignal_ids:
            try:
                prosp = Prospect(WH_ID=id, auth_header=WH_auth_dict)
                prospects.append(prosp)
            except Exception as e:
                print("Problem with WH id {}: {}".format(id, e))

    # run analytics if requested
    if run_analytics:
        print("running analytics")
        for prosp in tqdm(prospects):
            try:
                if company:
                    tags = get_prospect_tags(
                        prosp, company_id=company.coresignal_id, event_date=date
                    )
                else:
                    tags = get_prospect_tags(prosp, event_date=date)

                prosp.analytics = tags

            except Exception as e:
                print("Problem with prospect id {}: {}".format(prosp.id, e))

    # pushig prospects
    print("pushing prospects")
    for prosp in tqdm(prospects):
        try:
            if company:
                push_person(WH_auth_dict, prosp, event_id, company_id)
            else:
                push_person(WH_auth_dict, prosp, event_id)

        except Exception as e:
            print(
                "Problem pushing prospect with connectors. Prospect: {}, Error: {}".format(
                    prosp.id, e
                )
            )
    print(f"Finished event {title}")

    return None

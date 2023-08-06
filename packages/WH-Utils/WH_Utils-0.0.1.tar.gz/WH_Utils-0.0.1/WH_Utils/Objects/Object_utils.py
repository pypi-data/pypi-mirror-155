import json
from typing import List, Union, Dict, Any
import re
import validators
import datetime

WH_DB_URL = "https://db.wealthawk.com"


class AuthError(Exception):
    pass


class JsonError(Exception):
    pass


def verify_json(expected_class: str, json: Dict[str, Any]) -> None:
    """ """
    if expected_class == "client":
        _verify_as_client(json)
    elif expected_class == "company":
        _verify_as_company(json)
    elif expected_class == "user":
        _verify_as_user(json)
    elif expected_class == "event":
        _verify_as_event(json)

    return None


def _verify_as_client(json: Dict[str, Any]) -> None:
    expected_keys = [
        "id",
        "name",
        "location",
        "coresignal_id",
        "linkedin_url",
        "picture",
        "event_type",
        "full_data",
        "analytics",
        "date_created",
        "last_modified",
    ]
    actual_keys = list(json.keys())
    same_keys = set(expected_keys) == set(actual_keys)
    if not same_keys:
        raise JsonError(
            "JSON did not have expected keys. Expected keys are {} and actual keys are {}".format(
                expected_keys, actual_keys
            )
        )


def _verify_as_company(json: Dict[str, Any]) -> None:
    expected_keys = [
        "id",
        "name",
        "coresignal_id",
        "linkedin_url",
        "industry",
        "description",
        "location",
        "logo",
        "type",
        "website",
        "full_data",
        "created",
        "last_modified",
        "CIK",
    ]
    actual_keys = list(json.keys())
    same_keys = set(expected_keys) == set(actual_keys)
    if not same_keys:
        raise JsonError(
            "JSON did not have expected keys. Expected keys are {} and actual keys are {}".format(
                expected_keys, actual_keys
            )
        )


def _verify_as_user(json: Dict[str, Any]) -> None:
    expected_keys = [
        "id",
        "first_name",
        "last_name",
        "email",
        "other_info",
        "rank",
        "firebase_id",
        "created",
        "last_modified",
    ]
    actual_keys = list(json.keys())
    same_keys = set(expected_keys) == set(actual_keys)
    if not same_keys:
        raise JsonError(
            "JSON did not have expected keys. Expected keys are {} and actual keys are {}".format(
                expected_keys, actual_keys
            )
        )


def _verify_as_event(json: Dict[str, Any]) -> None:
    expected_keys = [
        "id",
        "description",
        "type",
        "title",
        "date_of",
        "link",
        "location",
        "value",
        "other_info",
        "created",
        "last_modified",
    ]
    actual_keys = list(json.keys())
    same_keys = set(expected_keys) == set(actual_keys)
    if not same_keys:
        raise JsonError(
            "JSON did not have expected keys. Expected keys are {} and actual keys are {}".format(
                expected_keys, actual_keys
            )
        )


def verify_auth_header(json: Dict[str, Any]) -> None:
    if "Authorization" not in json:
        raise AuthError("The auth header dict doesn't appear to be in the right format")
    s = json["Authorization"]
    if "Bearer " not in s:
        raise AuthError("The auth header dict doesn't appear to be in the right format")
    return None


def minus_key(key, dictionary):
    shallow_copy = dict(dictionary)
    del shallow_copy[key]
    return shallow_copy


def is_string_an_url(url_string: str) -> bool:
    """
    Checks if a string is an url or not. Only returns true if it starts with http or https or similar
    :param url_string:
    :type url_string:
    :return:
    :rtype:
    """
    result = validators.url(url_string)

    if isinstance(result, validators.ValidationFailure):
        return False

    return result


def company_urls_similar(url1, url2):
    """
    linkedin is weird and has a bunch of subdomians they bounce stuff off
    so this is a utility function to check if the last part of the url is
    the same or not. i.e. after the "linkedin.com" part.
    """
    # assert "linkedin.com" in url1, "URL #1 doesn't look like a linkedin url"
    # assert "linkedin.com" in url2, "URL #1 doesn't look like a linkedin url"
    if not url1 or not url2:
        return False

    url1, url2 = url1.lower(), url2.lower()

    comp1, comp2 = url1.split("linkedin.com")[-1], url2.split("linkedin.com")[-1]

    comp1 = comp1.replace("/", "").lower().strip()
    comp2 = comp2.replace("/", "").lower().strip()

    return comp1 == comp2


def get_company_data(company, exp_dict):
    """
    If a clients MIM event is a company exit, then there are additional
    columns in for the client included 'company' and start and end dates.
    This matches the MIM event to the correct company and returns a dict
    of the relevent information.

    Args:
        company (str): the name or LINKEDIN url of the company. If using url,
                        must start with http or https
        exp_dict (dict): this is the subsection of a coresignal member seach
                         called 'member_experience_collection'. See example

    Returns:
        dict: keys: [company_name, company_url, location, title, date_from, date_to, duration, company_id]

    Example:
        >>> employee_data = wh_employee_data[0] # raw response from coresignal
        >>> employee_data.keys()
        dict_keys(['id', 'name', 'title', 'url', 'hash', 'location', 'industry', 'summary', 'connections',
        'recommendations_count', 'logo_url', 'last_response_code', ...
        >>> member_exp = employee_data['member_experience_collection']
        >>> member_exp
        [{'id': 451609982,
          'member_id': 329972624,
          'title': 'Executive Director',
          'location': 'Greater San Diego Area',
          'company_name': 'Advisor of the Year',
          'company_url': None,
          'date_from': 'June 2016',
          'date_to': None, ...
        >>> get_company_data('wealthawk', exp_dict)
        {'title': 'Co-founder & CEO',
         'location': 'San Diego, California, United States',
         'company_name': 'WEALTHAWK',
         'company_url': 'https://cf.linkedin.com/company/wealthawk',
         'date_from': 'June 2021',
         'date_to': None,
         'duration': None,
         'description': '[Early stage fintech] Develop strategy, assemble a world-class team, build a product users love, form a company to deliver that product.',
         'company_id': 33158580}
        >>>


    """
    company = company.lower()
    flag = False

    if is_string_an_url(company):
        for exp in exp_dict:
            if company_urls_similar(company, exp["company_url"]):
                flag = True
                break
    else:
        for exp in exp_dict:
            if exp["company_name"].lower() == company:
                flag = True
                break

    if not flag:
        company_names = [x["company_name"] for x in exp_dict]
        raise ValueError(
            "Could not find any expirences with company: {}. Available company names are: {}".format(
                company, company_names
            )
        )

    keys_we_want = [
        "title",
        "location",
        "company_name",
        "company_url",
        "date_from",
        "date_to",
        "duration",
        "description",
        "company_id",
    ]
    return {k: exp[k] for k in keys_we_want}


def linkedin_dates_to_ts(date_string):
    """
    Linkedin job history uses times like "June 2021" and this parses that to datetime

    """
    return datetime.datetime.strptime(date_string, "%B %Y")

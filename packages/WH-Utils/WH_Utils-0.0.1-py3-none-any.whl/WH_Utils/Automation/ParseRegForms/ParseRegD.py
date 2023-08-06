import pprint
import sys

from bs4 import BeautifulSoup
from WH_Utils.Automation.ParseRegForms.Utils import strip
from typing import List, Union, Optional, Any, Dict
import requests


def get_and_parse_reg_d(url: str) -> dict[str, Any]:
    """
    Finds and parses a reg D from from the source.

    Args
    ------
        url: str
            the url of the reg D for you want to parse

    Returns
    --------
        data: dict
            Keys: 'Issuer', 'Contact', 'Persons', 'Industry', 'Size', 'Exemptions', 'FilingType', 'LongerThanAYear', 'TypeOfSecurities', 'BusinessCombination', 'MinimumInvestment', 'SalesCompensation', 'OfferingAndSalesAmount'
    """
    response = requests.get(
        url,
        headers={"Accept": "*/*", "Accept-Encoding": "*", "User-Agent": "Mozilla/5.0"},
    )

    return parse_reg_d(response.text)


def parse_reg_d(text: str) -> Dict[str, Any]:
    """
    This works just like get_and_parse_reg_d except that the input is the text itself. This
    function won't get the data for you.

    Args
    ------
        text: string
            the string of the data pulled from url of the reg D for you want to parse

    Returns
    --------
        data: dict
            Keys: 'Issuer', 'Contact', 'Persons', 'Industry', 'Size', 'Exemptions', 'FilingType', 'LongerThanAYear', 'TypeOfSecurities', 'BusinessCombination', 'MinimumInvestment', 'SalesCompensation', 'OfferingAndSalesAmount'
    """

    soup = BeautifulSoup(text, features="html.parser")

    FormData = {
        "Issuer": get_issuer(soup),
        "Contact": get_location(soup),
        "Persons": get_related_people(soup),
        "Industry": get_industry(soup),
        "Size": None,
        "Exemptions": get_exemptions(soup),
        "FilingType": get_type(soup),
        "LongerThanAYear": get_duration(soup),
        "TypeOfSecurities": get_security_types(soup),
        "BusinessCombination": get_combo(),
        "MinimumInvestment": get_min_investment(soup),
        "SalesCompensation": get_sales_comp(soup),
        "OfferingAndSalesAmount": get_offering_amt(soup),
    }
    return FormData


def get_issuer(soup: BeautifulSoup) -> Dict[str, str]:
    """
    Gets the issuer dict from the form.

    Args
    ------
        soup: BeautifulSoup
            the BeautifulSoup generated from the reg d for scrape

    Returns
    --------
        data: Dict
            keys: 'CIK', 'EntityType', 'PreviousNames', 'Name of Issuer', 'Jurisdiction of Incorporation/Organization', 'Year of Incorporation/Organization'
    """
    identity = {}

    # ------------------ 1. Issuer Identity Information ------------------
    table = soup.find("table", attrs={"summary": "Issuer Identity Information"})
    table_body = table.find("tbody")

    rows = table_body.find_all("tr")

    noPreviousNames = rows[1].find("td").get_text() == "X"
    if noPreviousNames:
        identity["previousNames"] = "None"

    row = rows[2]
    cols = row.find_all("td")

    cols = [strip(ele.text) for ele in cols]
    while "" in cols:
        cols.remove("")

    identity["CIK"] = cols[0]
    identity["EntityType"] = cols[cols.index("X") + 1]
    if not noPreviousNames:
        identity["PreviousNames"] = cols[1]
    i = 3
    while "Issuer" not in row.get_text():
        i += 1
        row = rows[i]

    for row in rows[i : i + 6]:
        header = row.find("th")
        data = row.find("td")

        if header:
            last_header = header
        if data:
            if data.find("table"):
                cols = data.find_all("td")
                cols = [strip(ele.text) for ele in cols]
                while "" in cols:
                    cols.remove("")
                data = cols[cols.index("X") + 1]
            else:
                data = data.get_text()

            identity[last_header.get_text()] = data
    return identity


def get_location(soup: BeautifulSoup) -> Dict[str, str]:
    """
    Gets the location dict from the form.

    Args
    ------
        soup: BeautifulSoup
            the BeautifulSoup generated from the reg d for scrape

    Returns
    --------
        data: Dict
            keys: 'Name of Issuer', 'Street Address 1', 'Street Address 2', 'City', 'State/Province/Country', 'ZIP/PostalCode', 'Phone Number of Issuer'
    """
    table = soup.find(
        "table",
        attrs={"summary": "Principal Place of Business and Contact Information"},
    )
    rows = table.find_all("tr")
    location = {}
    for row in rows:
        header = row.find_all("th")
        data = row.find_all("td", recursive=False)
        data = [ele.get_text() for ele in data]

        if header:
            last_header = header
        if data:
            for i, head in enumerate(last_header):
                if len(data) > i:
                    location[head.get_text()] = data[i]
                else:
                    location[head.get_text()] = ""
    return location


def get_related_people(soup: BeautifulSoup) -> List[dict]:
    """
    Gets the list of related people dict from the form.

    Args
    ------
        soup: BeautifulSoup
            the BeautifulSoup generated from the reg d for scrape

    Returns
    --------
        data: List
            each item in the list is a dict and has the following keys: 'Last Name', 'First Name', 'Middle Name', 'Street Address 1', 'Street Address 2', 'City', 'State/Province/Country', 'ZIP/PostalCode'

    """
    tables = soup.find_all("table", attrs={"summary": "Related Persons"})
    relations = []
    for table in tables:
        rows = table.find_all("tr")
        relation = {}
        for row in rows:
            header = row.find_all("th")
            data = row.find_all("td", recursive=False)
            data = [ele.get_text() for ele in data]

            if header:
                last_header = header
            if data:
                for i, head in enumerate(last_header):
                    if len(data) > i:
                        relation[head.get_text()] = data[i]
                    else:
                        relation[head.get_text()] = ""
        relations.append(relation)
        return relations


def get_industry(soup: BeautifulSoup) -> str:
    """
    Gets the industry from the form.

    Args
    ------
        soup: BeautifulSoup
            the BeautifulSoup generated from the reg d for scrape

    Returns
    --------
        data: string
            the industry
    """
    table = soup.find("table", attrs={"summary": "Industry Group"})
    cols = table.find_all("td")

    cols = [strip(ele.text) for ele in cols]
    while "" in cols:
        cols.remove("")

    industry = cols[cols.index("X") + 1]

    # ------------------ 5. Issuer Size ------------------

    table = soup.find("table", attrs={"summary": "Issuer Size"})
    cols = table.find_all("td")

    cols = [strip(ele.text) for ele in cols]
    while "" in cols:
        cols.remove("")

    issuerSize = cols[cols.index("X") + 1]
    return industry


def get_exemptions(soup: BeautifulSoup) -> List[str]:
    """
    Gets the list of exceptions from the form.

    Args
    ------
        soup: BeautifulSoup
            the BeautifulSoup generated from the reg d for scrape

    Returns
    --------
        data: List[str]
            Idk what else to say but for example: ['Rule 504(b) (not (i), (ii) or (iii))', 'Rule 506']
    """
    table = soup.find(
        "table", attrs={"summary": "Federal Exemptions and Exclusions Claimed"}
    )
    cols = table.find_all("td")

    cols = [strip(ele.text) for ele in cols]
    while "" in cols:
        cols.remove("")

    indices = [index for index, element in enumerate(cols) if element == "X"]
    exemptions = [cols[i + 1] for i in indices]
    return exemptions


def get_type(soup: BeautifulSoup) -> str:
    """
    Truly no idea what this is.

    Args
    ------
        soup: BeautifulSoup
            the BeautifulSoup generated from the reg d for scrape

    Returns
    --------
        type: string
            yeah I really dont know. The example is: 'New Notice'
    """
    table = soup.find("table", attrs={"summary": "Type of Filing"})
    cols = table.find_all("td")

    cols = [strip(ele.text) for ele in cols]
    while "" in cols:
        cols.remove("")

    filingType = cols[cols.index("X") + 1]
    return filingType


def get_duration(soup: BeautifulSoup) -> bool:
    """
    Also not sure what this is. Seems to just be a bool where its greater or less than a year.


    Args
    ------
        soup: BeautifulSoup
            the BeautifulSoup generated from the reg d for scrape

    Returns
    --------
        longer_that_year: bool
            If false its shorter than a year
    """
    table = soup.find("table", attrs={"summary": "Duration of Offering"})
    cols = table.find_all("td")

    cols = [strip(ele.text) for ele in cols]
    while "" in cols:
        cols.remove("")

    longerThanAYear = cols[cols.index("X") + 1] == "Yes"
    return longerThanAYear


def get_security_types(soup: BeautifulSoup) -> List[str]:
    """
    Gets the list of security types from the form.

    Args
    ------
        soup: BeautifulSoup
            the BeautifulSoup generated from the reg d for scrape

    Returns
    --------
        data: List[str]
            Idk what else to say but for example: ['Equity']
    """
    table = soup.find("table", attrs={"summary": "Types of Securities Offered"})
    cols = table.find_all("td")

    cols = [strip(ele.text) for ele in cols]
    while "" in cols:
        cols.remove("")

    indices = [index for index, element in enumerate(cols) if element == "X"]
    securityTypes = [cols[i + 1] for i in indices]
    return securityTypes


def get_combo(soup: BeautifulSoup) -> bool:
    """
    Actually no idea whats going on here

    Args
    ------
        soup: BeautifulSoup
            the BeautifulSoup generated from the reg d for scrape

    Returns
    --------
        data: bool
            business combo?
    """
    table = soup.find("table", attrs={"summary": "Business Combination Transaction"})
    cols = table.find_all("td")

    cols = [strip(ele.text) for ele in cols]
    while "" in cols:
        cols.remove("")

    businessCombo = cols[cols.index("X") + 1] == "Yes"
    return businessCombo


def get_min_investment(soup: BeautifulSoup) -> str:
    """
    Returns the minimum investment as a string. Amount then currency type.

    Args
    ------
        soup: BeautifulSoup
            the BeautifulSoup generated from the reg d for scrape

    Returns
    --------
        min_investment: str
            Example: '$0 USD'
    """
    table = soup.find("table", attrs={"summary": "Minimum Investment"})
    cols = table.find_all("td")

    cols = [strip(ele.text) for ele in cols]
    while "" in cols:
        cols.remove("")

    minInvestment = " ".join(cols[1:])
    return minInvestment


def get_sales_comp(soup: BeautifulSoup) -> List[dict]:
    """
    Returns the sales comp.

    Args
    ------
        soup: BeautifulSoup
            the BeautifulSoup generated from the reg d for scrape

    Returns
    --------
        min_investment: str
            List of dicts. Schema for dicts is: 'Recipient', 'Recipient CRD Number', '(Associated) Broker or Dealer', '(Associated) Broker or Dealer CRD Number', 'Street Address 1', 'Street Address 2', 'City', 'State/Province/Country', 'ZIP/Postal Code', 'State(s) of Solicitation (select all that apply)Check “All States” or check individual States', 'All States', 'Foreign/non-US'
    """
    tables = soup.find_all("table", attrs={"summary": "Sales Compensation"})
    compensations = []
    for table in tables:
        table = table.find("tbody")
        rows = table.find_all("tr", recursive=False)
        compensation = {}
        data = None
        header = None
        for i, row in enumerate(rows):
            if i % 2 == 0:
                data = None
                header = row.find_all(
                    "td", recursive="False", attrs={"class": "FormText"}
                )
                header = [
                    h for h in header if not h.find("table") and not h.text == "None"
                ]
                if not header:
                    header = row.find_all("th", recursive="False")
            else:
                data = row.find_all("td", recursive=False)
                if row.find("table"):
                    newdata = []
                    for cell in data:
                        if cell.find("table"):
                            data = [[ele.get_text() for ele in cell.find_all("tr")]]
                else:
                    data = [strip(ele.get_text()) for ele in data]

            if data:
                for i, head in enumerate(header):
                    if len(data) > i:
                        compensation[head.get_text()] = data[i]
                    else:
                        compensation[head.get_text()] = ""
        compensations.append(compensation)
        return compensations


def get_offering_amt(soup: BeautifulSoup) -> Dict[str, str]:
    """
    Returns the offering amount in dict form.

    Args
    ------
        soup: BeautifulSoup
            the BeautifulSoup generated from the reg d for scrape

    Returns
    --------
        data: dict
            example: {'Total Offering Amount': '$51,605,250',
                     'Total Amount Sold': '$51,605,250',
                     'Total Remaining to be Sold': 'Indefinite'}
    """
    table = soup.find("table", attrs={"summary": "Offering and Sales Amounts"}).find(
        "tbody"
    )
    rows = table.find_all("tr", recursive=False)
    amount = {}
    for row in rows:
        cols = row.find_all("td", recursive=False)
        elements = [strip(c.text) for c in cols[1:]]
        amount[cols[0].text] = (
            elements[0] if "orXIndefinite" not in elements else "Indefinite"
        )
    return amount

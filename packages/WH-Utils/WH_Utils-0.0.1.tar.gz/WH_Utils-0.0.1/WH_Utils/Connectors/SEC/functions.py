import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests_random_user_agent
import datetime
import re
from typing import List, Dict, Optional
import time
from tqdm import tqdm

# from secedgar.cik_lookup import CIKLookup


def get_info_from_line(line: str) -> dict:
    """
    Takes a line (string) from parse_recent_reg_D and gets the relevant info from it

    Args:
      line: str
        the string. should look like 05-19-2022   <a href="/Archives/edgar/data/1929752/0001929752-22-000001-index.html">D</a>             <a href="browse-edgar?action=getcompany&amp;CIK=1929752">1929752</a>   BenWick Inc.

    Returns:
      info: dict
        keys include 'date' (date form was submitted),  'form_type', 'form_link', 'CIK_code', 'info' (what was on the form), 'company_name'
    """

    data = {}
    root_url = "https://www.sec.gov"
    api_url = "https://data.sec.gov/submissions/CIK{}.json"
    date, form, CIK_code, name = [x for x in line.split("   ") if x]

    data["date"] = datetime.datetime.strptime(date, "%m-%d-%Y")
    form_bs = BeautifulSoup(form, "html.parser")
    data["form_type"] = form_bs.text
    data["form_link"] = root_url + form_bs.a["href"]

    CIK_code = BeautifulSoup(CIK_code, "html.parser").text.strip()
    CIK_code = "0" * (10 - len(CIK_code)) + CIK_code

    data["CIK_code"] = CIK_code

    try:
        req = requests.get(api_url.format(CIK_code))
        if req.status_code != 200:
            info = {"Error": req.text}
        else:
            info = req.json()
    except Exception as e:
        info = {"Error": e}

    data["info"] = info
    data["company_name"] = name

    return data


def get_reg_D_page() -> str:
    """
    pulls the list of recent reg D fillings from the SEC
    """
    list_of_results = "https://www.sec.gov/cgi-bin/current?q1=0&q2=4&q3=D"
    list_html = requests.get(list_of_results)
    assert list_html.status_code == 200, "Problem pulling list of reg D fillings"

    return list_html.text


def parse_recent_reg_D(webpage: str) -> List[str]:
    """
    Does some basic string processing to parse the webpage
    """
    match = r"\d{2}-\d{2}-\d{4}"
    entries = [x for x in webpage.split("\n") if bool(re.match(match, x))]
    return entries


def get_all_recent_reg_D(webpage: str) -> List[Dict]:
    """ """
    reg_d_info = []
    for line in tqdm(parse_recent_reg_D(webpage)):
        reg_d_info.append(get_info_from_line(line))
        time.sleep(0.5)

    return reg_d_info


# def get_CIK_from_ticker

from WH_Utils.Objects.Prospect import Prospect
from WH_Utils.Analytics.Prospects.Nodes import (
    get_company_data_by_id,
    classify_job_title,
)

from typing import List, Dict, Union, Optional, Any
import datetime


def get_prospect_tags(
    prospect: Prospect,
    company_id: Optional[int] = None,
    event_date: Optional[datetime.date] = None,
) -> Dict[str, Any]:
    """This function takes a prospect and generates all the tags for this prospeect"""
    if company_id and event_date:
        company_info = get_company_data_by_id(prospect, company_id, event_date)

    else:
        return {
            "title": "None",
            "employee_rank": "None",
            "languages_spoken": prospect.languages,
            "age": prospect.age,
            "joined_pre_exit": None,
            "days_at_company_preexist": None,
        }

    data = {
        "title": company_info["title"],
        "employee_rank": classify_job_title(company_info["title"]),
        "languages_spoken": prospect.languages,
        "age": prospect.age,
        "joined_pre_exit": company_info["joined_pre_exit?"],
        "days_at_company_preexist": company_info["time_pre_exit"],
    }
    return data

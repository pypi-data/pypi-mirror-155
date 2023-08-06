import os
import sys
from datetime import datetime, timedelta


def backend_auth():
    """
    This returns an auth header to access the WEALTHAWK backend
    """


def parse_linkedin_date(date: str) -> datetime:
    """
    parses than annoying linkedin style date into a real datetime
    """
    month = None
    try:
        year = int(date)
    except ValueError:
        return None

    if month:
        return datetime(year, month, 1)

    else:
        return datetime(year, 1, 1)

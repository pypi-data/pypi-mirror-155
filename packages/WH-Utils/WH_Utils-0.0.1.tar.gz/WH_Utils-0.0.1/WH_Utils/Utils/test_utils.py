import os
from dotenv import load_dotenv
import requests
import warnings

load_dotenv()

# setting up authentication for testing

WH_API_KEY = ""

WH_auth_dict = {"accept": "application/json", "Authorization": WH_API_KEY}

login_header = {
    "accept": "application/json",
    "Content-Type": "application/x-www-form-urlencoded",
}

login_data = {
    "username": "mcclain.thiel@berkeley.edu",
    "password": os.getenv("WH_ACCOUNT_PASSWORD"),
}

response = requests.post(
    "https://db.wealthawk.com/login", headers=login_header, data=login_data
)

assert response.status_code == 200, "Error getting auth token: {}".format(response.text)

key = response.json()["access_token"]
access_token_string = "Bearer {}".format(key)

WH_auth_dict["Authorization"] = access_token_string

CS_API_KEY = "Bearer " + os.getenv("CORESIGNAL_API_KEY")
CS_auth_dict = {"accept": "application/json", "Authorization": CS_API_KEY}

BASE_URL = "https://db.wealthawk.com"

try:
    HF_TOKEN = os.environ["HF_AUTH_TOKEN"]
except Exception as e:
    HF_TOKEN = ""
    warnings.warn(
        "No huggingface token found. This will limit use of analytics package"
    )

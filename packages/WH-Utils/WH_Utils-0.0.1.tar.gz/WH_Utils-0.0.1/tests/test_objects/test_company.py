import json
from WH_Utils.Objects.Company import Company
from WH_Utils.Utils.test_utils import WH_auth_dict, BASE_URL
import requests
import warnings



class TestCompany:

    def test_company_valid_json(self):
        with open("tests/test_data/objects_data/company.json", 'r') as f:
            data = json.load(f)
        company = Company(data_dict=data)
        assert isinstance(company, Company)

    def test_company_invalid_json(self):
        assert True

    def test_company_from_db(self):
        company_id="0701bd03-423f-46d3-afcc-7fac9c2a279f"
        company = Company(WH_ID=company_id, auth_header=WH_auth_dict)
        assert isinstance(company, Company)

    def test_push_to_db(self):
        with open("tests/test_data/objects_data/company.json", 'r') as f:
            data = json.load(f)
        company = Company(data_dict=data)

        response = company.send_to_db(WH_auth_dict)

        if response.status_code == 200:
            id = response.json()['id']
            response2 = requests.delete(BASE_URL + "/company", params={'companyID': id}, headers=WH_auth_dict)
            if response2.status_code != 200:
                print(response2.text)
                warnings.warn("Test Company Not deleted. Company {} was added but there was a problem deleting. {}".format(id, response2.text))

        assert response.status_code == 200

import json
from WH_Utils.Objects.Event import Event
from WH_Utils.Utils.test_utils import WH_auth_dict, BASE_URL
import requests
import warnings



class TestEvent:

    def test_event_valid_json(self):
        with open("tests/test_data/objects_data/event.json", 'r') as f:
            data = json.load(f)
        prospect = Event(data_dict=data)
        assert isinstance(prospect, Event)

    def test_event_invalid_json(self):
        assert True

    def test_event_from_db(self):
        event_id="e936e1a3-1114-426f-927a-186a92287d66"
        event = Event(WH_ID=event_id, auth_header=WH_auth_dict)
        assert isinstance(event, Event)

    def test_push_to_db(self):
        with open("tests/test_data/objects_data/event.json", 'r') as f:
            data = json.load(f)
        event = Event(data_dict=data)

        response = event.send_to_db(WH_auth_dict)

        if response.status_code == 200:
            id = response.json()['id']
            response2 = requests.delete(BASE_URL + "/event", params={'eventID': id}, headers=WH_auth_dict)
            if response2.status_code != 200:
                warnings.warn("Test event Not deleted. EventID {} was added but there was a problem deleting. {}".format(id, response2.text))

        assert response.status_code == 200

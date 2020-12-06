from unittest import mock

import pytest

from services.hubspot.endpoints.deals import Deals
from services.hubspot.endpoints.endpoint import Endpoint
from services.hubspot.endpoints.exceptions import (
    FetchEndpointError,
    UnregisterdEndpoint
)


@pytest.fixture
def mocked_deals_response():
    return {'deals': [
        {'portalId': 8946942, 'dealId': 3569506599, 'isDeleted': False, 'associations': None,
         'properties': {
             'dealname': {
                 'value': 'Brian Halligan (Sample Contact) - New Deal',
                 'timestamp': 1607209523547,
                 'source': 'CRM_UI', 'sourceId': 'salocinov@gmail.com', 'updatedByUserId': 12732151,
                 'versions': [
                                                 {'name': 'dealname', 'value': 'Brian Halligan (Sample Contact) - New Deal',
                                                  'timestamp': 1607209523547, 'sourceId': 'salocinov@gmail.com', 'source': 'CRM_UI',
                                                  'sourceVid': [], 'updatedByUserId': 12732151
                                                  }
                 ]
             },
             'amount': {
                 'value': '3455', 'timestamp': 1607247854662, 'source': 'CRM_UI',
                 'sourceId': 'salocinov@gmail.com', 'updatedByUserId': 12732151,
                 'versions': [
                             {'name': 'amount', 'value': '3455', 'timestamp': 1607247854662,
                              'sourceId': 'salocinov@gmail.com', 'source': 'CRM_UI', 'sourceVid': [],
                              'requestId': 'fc6dcfb9-e548-4010-ab3c-abacc47eadce', 'updatedByUserId': 12732151
                              }
                 ]
             },
             'dealstage': {'value': 'contractsent', 'timestamp': 1607247864523,
                           'source': 'CRM_UI', 'sourceId': 'salocinov@gmail.com', 'updatedByUserId': 12732151,
                           'versions': [
                               {'name': 'dealstage', 'value': 'contractsent', 'timestamp': 1607247864523,
                                        'sourceId': 'salocinov@gmail.com', 'source': 'CRM_UI', 'sourceVid': [],
                                        'requestId': '74539893-3a63-48fd-ac9f-9f1fb06daa55', 'updatedByUserId': 12732151
                                }
                           ]
                           },
             'createdate': {
                 'value': '1607247864523',
             }
         },
         'imports': [], 'stateChanges': []}],
        'hasMore': False, 'offset': 3569506600
    }


def test_deals_fetch_data(mocked_deals_response):
    deal_endpoint = Endpoint.create('deals')
    mocked_response = mock.MagicMock()
    mocked_response.status_code = 200
    mocked_response.json.return_value = mocked_deals_response
    mocked_hubspot_api = mock.MagicMock()
    mocked_hubspot_api.fetch_data.return_value = mocked_response
    response = deal_endpoint.fetch_data(mocked_hubspot_api)
    assert len(response) == 1
    assert set(response[0].keys()) == {'dealname', 'amount', 'dealstage', 'createdate', 'deal_id'}


def test_deals_fetch_data_error(mocked_deals_response):
    deal_endpoint = Endpoint.create('deals')
    mocked_response = mock.MagicMock()
    mocked_response.status_code = 404
    mocked_hubspot_api = mock.MagicMock()
    mocked_hubspot_api.fetch_data.return_value = mocked_response
    with pytest.raises(FetchEndpointError):
        deal_endpoint.fetch_data(mocked_hubspot_api)

import pytest

from services.hubspot.endpoints.deals import Deals
from services.hubspot.endpoints.endpoint import Endpoint


@pytest.fixture
def mocked_deals_response():
    return [
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
          'imports': [], 'stateChanges': [],
          'hasMore': True, 'offset': 3569506600}
    ]


def test_deals_parsing(mocked_deals_response):
    deal_endpoint = Endpoint.create('deals')
    response = deal_endpoint._parse_response(mocked_deals_response)
    assert len(response) == 1
    assert set(response[0].keys()) == {'dealname', 'amount', 'dealstage', 'createdate', 'deal_id'}

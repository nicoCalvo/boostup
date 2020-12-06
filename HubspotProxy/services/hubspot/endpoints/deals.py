from .endpoint import Endpoint


class Deals(Endpoint):
    SCOPE = 'contacts'
    PATH = f'deals/v1/deal/paged'
    PROPERTIES = ('dealname', 'dealstage', 'amount')

    def _get_custom_params(self, furl):
        for property in self.PROPERTIES:
            furl.add({'properties': property})
        return furl

    def _parse_response(self, response):
        """
        Obtain only targeted properies defined on the endpoint and discard remaining data

        response eg:
        {'deals': 
            [
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
                                            }
                                },
                                'imports': [], 'stateChanges': []}], 'hasMore': True, 'offset': 3569506600}
        """
        deals = []
        for deal in response:
            deal_data = {x: deal['properties'][x]['value'] for x in deal['properties']}
            deal_data['deal_id'] = deal['dealId']
            deals.append(deal_data)
        return deals            

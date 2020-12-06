import time
from unittest import mock

import pytest

from models.token import Token
from services.hubspot.hubspot_api import HubSpotApi


@pytest.fixture
def token(request):
    token = Token(**request.param).save()
    return token


@mock.patch('landing.home.HubSpotApi.get_new_token', return_value={'refresh_token': '', 'access_token': '',
                                                                   'expires_in': 1, 'expires_at': 123})
@pytest.mark.parametrize("token", [{'refresh_token': 'random_string',
                                    'access_token': 'random_string',
                                    'expires_in': 21600, 'expires_at': int(time.time()) - 1}], indirect=True)
def test_renew_token(db, token, client):
    redirect_url = client.get('https://localhost:9999/')
    assert redirect_url.status_code == 302
    assert redirect_url.headers['location'] == 'https://localhost:9999/deals'


@pytest.mark.parametrize("token", [{'refresh_token': 'random_string', 'access_token': 'random_string',
                                    'expires_in': 21600, 'expires_at': int(time.time()) - 1}

                                   ], indirect=True)
def test_renew_token_error_db(db, token, client):
    with mock.patch.object(Token, 'save', side_effect=Exception()):
        response = client.get('https://localhost:9999/')
    assert response.status_code == 500


@mock.patch('landing.home.HubSpotApi.fetch_token', return_value={'refresh_token': '', 'access_token': '',
                                                                 'expires_in': 1, 'expires_at': 123})
def test_callback_fetch_token(db, client):
    redirect_url = client.get('https://localhost:9999/callback')
    assert redirect_url.status_code == 302
    assert redirect_url.headers['location'] == 'https://localhost:9999/deals'


@pytest.mark.parametrize("token", [{'refresh_token': '', 'access_token': '', 'expires_in': 1, 'expires_at': 0}], indirect=True)
@mock.patch.object(Token, 'is_valid', return_value=True)
@mock.patch('landing.home.Endpoint.fetch_data', return_value=[{'dealname': 'Brian Halligan (Sample Contact) - New Deal', 'amount': '3455',
                                                               'dealstage': 'contractsent',
                                                               'createdate': 'Sun Dec  6 06:44:24 2020',
                                                               'deal_id': 3569506599}])
def test_get_deals(db, mocked_hubspot_api, token, client):
    response = client.get('https://localhost:9999/deals')
    assert response.status_code == 200


def test_reset_flow(client):
    response = client.post('https://localhost:9999/reset_flow')
    assert response.status_code == 302

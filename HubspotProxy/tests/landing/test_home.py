import time
from unittest import mock

import pytest

from models.token import Token


@mock.patch('landing.home.HubSpotApi.get_new_token', return_value={'refresh_token': '', 'access_token': '',
                                                                   'expires_in': 1, 'expires_at': 123})
def test_renew_token(db, client):
    expires_at = int(time.time()) - 1  # force expiration
    token_data = {'refresh_token': 'random_string',
                  'access_token': 'random_string',
                  'expires_in': 21600, 'expires_at': expires_at}

    Token(**token_data).save()
    redirect_url = client.get('https://localhost:9999/')
    assert redirect_url.status_code == 302
    assert redirect_url.headers['location'] == 'https://localhost:9999/deals'


@mock.patch('landing.home.HubSpotApi.get_new_token', return_value={'refresh_token': '', 'access_token': '',
                                                                   'expires_in': 1, 'expires_at': 123})
def test_renew_token_error_db(db, client):
    expires_at = int(time.time()) - 1  # force expiration
    token_data = {'refresh_token': 'random_string',
                  'access_token': 'random_string',
                  'expires_in': 21600, 'expires_at': expires_at}

    Token(**token_data).save()
    with mock.patch.object(Token, 'save', side_effect=Exception()):
        response = client.get('https://localhost:9999/')
    assert response.status_code == 500


@mock.patch('landing.home.HubSpotApi.fetch_token', return_value={'refresh_token': '', 'access_token': '',
                                                                 'expires_in': 1, 'expires_at': 123})
def test_callback_fetch_token(db, client):
    redirect_url = client.get('https://localhost:9999/callback')
    assert redirect_url.status_code == 302
    assert redirect_url.headers['location'] == 'https://localhost:9999/deals'

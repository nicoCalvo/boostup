from unittest import mock

import pytest
from requests_oauthlib import OAuth2Session

from services.hubspot.hubspot_api import HubSpotApi
from services.hubspot.exceptions import (
    InvalidScope,
    AuthorizationError
)


def test_invalid_scope():
    with pytest.raises(InvalidScope):
        HubSpotApi.get_auth_url(auth_callback_url='', scopes=['invalid'])


def test_get_auth_url():
    resp = HubSpotApi.get_auth_url(auth_callback_url='https://localhost', scopes=['contacts'])
    expected_url = ''.join(['https://app.hubspot.com/oauth/authorize?',
                            'response_type=code&client_id=105c5a0a-0ea',
                            'f-41de-ba45-58350a44c82a&redirect_uri=htt',
                            'ps%3A%2F%2Flocalhost&scope=contacts&state=random_string'
                            ])
    assert resp == expected_url


def test_fetch_token_error():
    with pytest.raises(AuthorizationError):
        HubSpotApi.fetch_token(code='some_code', auth_resp_url='', auth_callback_url='')


@mock.patch.object(OAuth2Session, 'fetch_token', return_value='a token')
def test_fetch_token(mocked_token):
    token = HubSpotApi.fetch_token(code='some_code', auth_resp_url='', auth_callback_url='')
    assert token == 'a token'


def test_get_new_token_error():
    with pytest.raises(AuthorizationError):
        HubSpotApi.get_new_token(refresh_token='some_token')


@mock.patch.object(OAuth2Session, 'refresh_token', return_value='a token')
def test_get_new_token(mocked_token):
    token = HubSpotApi.get_new_token(refresh_token='some_token')
    assert token == 'a token'

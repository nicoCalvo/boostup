import logging

from oauthlib.oauth2 import (
    MissingTokenError,
    InsecureTransportError
)
from requests_oauthlib import OAuth2Session

from services.hubspot.constants import (
    CLIENT_ID,
    CLIENT_SECRET
)
from services.hubspot.exceptions import (
    InvalidScope,
    AuthorizationError
)


logger = logging.getLogger(__name__)


class HubSpotApi:
    ALLOWED_SCOPES = {'contacts'}
    AUTH_URL = 'https://app.hubspot.com/oauth/authorize'
    CSRF_STATE = 'random_string'
    TOKEN_URL = 'https://api.hubapi.com/oauth/v1/token'

    @classmethod
    def get_auth_url(cls, auth_callback_url, scopes):
        """
        Returns target url for OAuth2 authorization on Hubspot site

        Args:
            auth_callback_url (str): url targeted to expect callback auth
            scopes (list): List of scopes to be authorized by the session

        Returns:
            str: url to initiate OAuth2 process

        Raises:
            InvalidScope: Invalid scope provided

        """

        if invalid_scopes := set(scopes) - cls.ALLOWED_SCOPES:
            raise InvalidScope(invalid_scopes)

        hubspot = OAuth2Session(client_id=CLIENT_ID, scope=scopes, redirect_uri=auth_callback_url)
        authorization_url, _ = hubspot.authorization_url(cls.AUTH_URL, state=cls.CSRF_STATE)
        return authorization_url

    @classmethod
    def fetch_token(cls, code, auth_resp_url, auth_callback_url):
        """
        Returns token from Hubspot site

        Args:
            code(str): Code provided by HubspotApi
            auth_resp_url(str): auth url provided after redirect by HubspotApi authorization
            auth_callback_url (str): url targeted to expect callback
        Returns:
            dict: a json token https://legacydocs.hubspot.com/docs/methods/oauth2/get-access-and-refresh-tokens


        Raises:
            AuthorizationError: Any auhentication/authorization related error with HubSpot Api

        """
        hubspot = OAuth2Session(CLIENT_ID, state=cls.CSRF_STATE)
        req_body = f'grant_type=authorization_code&client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&redirect_uri={auth_callback_url}&code={code}'
        try:
            return hubspot.fetch_token(cls.TOKEN_URL, method="POST", client_secret=CLIENT_SECRET,
                                       authorization_response=auth_resp_url, body=req_body)
        except Exception as e:
            logging.exception('Error fetching access token')
            raise AuthorizationError() from e

    @classmethod
    def get_new_token(cls, refresh_token):
        """
        Using the refresh_token previously fetched, a new access token is requested to HubSpot API.
        The new token invalidates previous token

        Args:
            refresh_token(str): refresh token provided on first token fetch
        Returns:
            dict: a json token https://legacydocs.hubspot.com/docs/methods/oauth2/get-access-and-refresh-tokens

        Raises:
            AuthorizationError: Any auhentication/authorization related error with HubSpot Api

        """
        hubspot=OAuth2Session(CLIENT_ID, token = refresh_token)
        try:
            return hubspot.refresh_token(token_url = cls.TOKEN_URL, refresh_token = refresh_token,
                                         client_id = CLIENT_ID, client_secret = CLIENT_SECRET)
        except Exception as e:
            logging.exception('Error fetching new access token')
            raise AuthorizationError() from e

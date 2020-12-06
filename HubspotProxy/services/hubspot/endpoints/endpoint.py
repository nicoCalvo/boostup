from abc import (
    ABCMeta,
    abstractmethod
)

from furl import furl


class UnregisterdEndpoint(Exception):
    pass


class FetchEndpointError(Exception):
    pass


class Endpoint(metaclass=ABCMeta):
    """
    Base class to interact with HubSpot API
    and fetch data in json format
    """
    PAGINATED = False
    BASE_URL = 'https://api.hubapi.com/'
    SCOPE = None  # scope of the endpoint
    LIMIT_SECS = 10
    LIMIT_AMOUNT = 1
    EXTRA_PARAMS = {'limit': 100}
    PATH = None  # path for each endpoint

    def __init__(self):
        self._offset = 0

    @abstractmethod
    def _get_custom_params(self, furl):
        pass

    @classmethod
    def create(cls, endpoint):
        try:
            endpoint_klass = next(klass for klass in cls.__subclasses__() if klass.__name__.lower() == endpoint)
        except KeyError:
            raise UnregisterdEndpoint(endpoint)
        return endpoint_klass()

    @classmethod
    def get_registered_scopes(cls):
        return {klass.SCOPE for klass in cls.__subclasses__()}

    def get_url(self):
        f = furl(self.BASE_URL)
        f /= self.PATH
        f.args = self.EXTRA_PARAMS
        f.args['limit'] = self.LIMIT_AMOUNT
        f.args['offset'] = self._offset
        self._get_custom_params(f)
        return f.url

    @abstractmethod
    def _parse_response(self, json_data):
        pass

    def fetch_data(self, hubspot_api, response_data=[]):
        url = self.get_url()
        try:
            response = hubspot_api.fetch_data(url)
            assert response.status_code == 200
        except Exception as e:
            raise FetchEndpointError() from e
        json_data = response.json()
        response_data.extend(json_data[self.__class__.__name__.lower()])
        self._offset = json_data['offset']
        if json_data['hasMore']:
            self.fetch_data(hubspot_api, response_data)
        return self._parse_response(response_data)
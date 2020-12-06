from abc import (
    ABCMeta,
    abstractmethod
)

from furl import furl

from .exceptions import (
    FetchEndpointError,
    UnregisterdEndpoint
)


class Endpoint(metaclass=ABCMeta):
    """
    Base class to interact with HubSpot API
    and fetch data in json format
    """
    BASE_URL = 'https://api.hubapi.com/'
    SCOPE = None  # scope of the endpoint
    LIMIT_SECS = 10
    LIMIT_AMOUNT = 100
    EXTRA_PARAMS = {'limit': 100}
    PATH = None  # path for each endpoint

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

    def get_url(self, offset=0):
        f = furl(self.BASE_URL)
        f /= self.PATH
        f.args = self.EXTRA_PARAMS
        f.args['limit'] = self.LIMIT_AMOUNT
        f.args['offset'] = offset
        self._get_custom_params(f)
        return f.url

    @abstractmethod
    def _parse_response(self, json_data):
        pass

    def fetch_data(self, hubspot_api, offset=0):
        response_data = []
        has_more = True
        while has_more:
            try:
                url = self.get_url(offset)
                response = hubspot_api.fetch_data(url)
                assert response.status_code == 200
            except Exception as e:
                raise FetchEndpointError() from e

            json_data = response.json()
            response_data.extend(json_data[self.__class__.__name__.lower()])
            has_more = json_data['hasMore']
        return self._parse_response(response_data)

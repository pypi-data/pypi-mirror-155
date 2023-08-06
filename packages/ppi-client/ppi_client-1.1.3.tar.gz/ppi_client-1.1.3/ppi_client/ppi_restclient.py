from json.encoder import JSONEncoder
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
import requests
import platform
import logging
from collections import namedtuple
from signalrcore.hub_connection_builder import HubConnectionBuilder
from ppi_client.api.constants import MIME_JSON, ACCOUNT_LOGIN, ACCOUNT_LOGIN_API

logger = logging.getLogger(__name__)

PPIAPIResponse = namedtuple("PPIAPIResponse", "httpStatus response")


class RestClient(object):
    client_id = None
    client_secret = None
    authorized_client = None
    client_key = None
    token_ws = None
    refresh_token_ws = None
    api_key = None
    api_secret = None
    def __init__(self, versionSDK, sandbox):
        self.USER_AGENT = "PPI Python SDK v" + versionSDK
        self.TRACKING_ID = "platform:" + platform.python_version() + ",type:SDK" + versionSDK + ",so;"

        self.__API_BASE_URL = "https://clientapi.portfoliopersonal.com/api/"
        self.__WS_BASE_URL = f"https://realtimeclientapi.portfoliopersonal.com/"
        self.__WS_BASE_URL_WS = f"wss://realtimeclientapi.portfoliopersonal.com/"
        self.__WS_TRACE = False
        self.__SSL_VERIFY = True
        if sandbox is True:
            self.__API_BASE_URL = "https://clientapi_sandbox.portfoliopersonal.com/api/"
            self.__WS_BASE_URL = f"https://realtimeclientapi-sandbox.portfoliopersonal.com/"
            self.__WS_BASE_URL_WS = f"wss://realtimeclientapi-sandbox.portfoliopersonal.com/"
            self.__WS_TRACE = False
            self.__SSL_VERIFY = True

    def get_session(self):
        """Creates and returns a ready-to-use requests.Session, with all the
        customizations made to access PPI
        """
        session = requests.Session()
        session.mount(self.__API_BASE_URL,
                      get_transport_adapter())
        return session

    def get(self, uri, params=None, headers=None, data=None, content_type=MIME_JSON):
        s = self.get_session()

        if data is not None and content_type == MIME_JSON:
            data = JSONEncoder().encode(data)
            headers.update({'x-tracking-id': self.TRACKING_ID,
                            'User-Agent': self.USER_AGENT,
                            'Accept': MIME_JSON,
                            'Content-type': content_type
                            })
            api_result = s.get(self.__API_BASE_URL + uri, data=data, headers=headers, verify=self.__SSL_VERIFY)

        else:
            headers.update({'x-tracking-id': self.TRACKING_ID,
                            'User-Agent': self.USER_AGENT,
                            'Accept': MIME_JSON
                            })

            api_result = s.get(self.__API_BASE_URL + uri, params=params, headers=headers, verify=self.__SSL_VERIFY)

        if not api_result.text:
            return PPIAPIResponse(api_result.status_code, '')

        return PPIAPIResponse(api_result.status_code, api_result.json())

    def post(self, uri, data=None, params=None, headers=None, content_type=MIME_JSON):
        if data is not None and content_type == MIME_JSON:
            data = JSONEncoder().encode(data)

        s = self.get_session()

        complete_headers = {'x-tracking-id': self.TRACKING_ID,
                            'User-Agent': self.USER_AGENT,
                            'Accept': MIME_JSON,
                            'Content-type': content_type
                            }
        complete_headers.update(headers)
        api_result = s.post(self.__API_BASE_URL + uri, params=params, data=data, headers=complete_headers,
                            verify=self.__SSL_VERIFY)

        if not api_result.text:
            return PPIAPIResponse(api_result.status_code, '')

        return PPIAPIResponse(api_result.status_code, api_result.json())

    def put(self, uri, data=None, params=None, headers=None, content_type=MIME_JSON):
        if data is not None and content_type == MIME_JSON:
            data = JSONEncoder().encode(data)

        s = self.get_session()

        complete_headers = {'x-tracking-id': self.TRACKING_ID,
                            'User-Agent': self.USER_AGENT,
                            'Accept': MIME_JSON,
                            'Content-type': content_type
                            }

        complete_headers.update(headers)

        api_result = s.put(self.__API_BASE_URL + uri, params=params, data=data,
                           headers=complete_headers, verify=self.__SSL_VERIFY)

        if not api_result.text:
            return PPIAPIResponse(api_result.status_code, '')

        return PPIAPIResponse(api_result.status_code, api_result.json())

    def delete(self, uri, data=None, params=None, headers=None, content_type=MIME_JSON):
        s = self.get_session()

        complete_headers = {'x-tracking-id': self.TRACKING_ID,
                            'User-Agent': self.USER_AGENT,
                            'Accept': MIME_JSON,
                            'Content-type': content_type}

        complete_headers.update(headers)

        api_result = s.delete(self.__API_BASE_URL + uri, params=params, data=data,
                              headers=complete_headers, verify=self.__SSL_VERIFY)

        if not api_result.text:
            return PPIAPIResponse(api_result.status_code, '')

        return PPIAPIResponse(api_result.status_code, api_result.json())

    def login_ws(self):
        auth_headers = {'AuthorizedClient': self.authorized_client, 'ClientKey': self.client_key}

        if self.api_key is not None and self.api_secret is not None:
            auth_headers.update({'ApiKey': self.api_key})
            auth_headers.update({'ApiSecret': self.api_secret})
            res = self.post(ACCOUNT_LOGIN_API, None, None, auth_headers, MIME_JSON)
        else:
            data = {
                "user": self.client_id,
                "password": self.client_secret
            }
            res = self.post(ACCOUNT_LOGIN, data, None, auth_headers, MIME_JSON)

        if res.httpStatus == 200:
            self.token_ws = res.response['accessToken']
            self.refresh_token_ws = res.response['refreshToken']
            return res.response['accessToken']

    async def connect_to_websocket(self, hub_name):
        server_url = self.__WS_BASE_URL_WS + hub_name
        hub_connection = HubConnectionBuilder() \
            .with_url(server_url,
                      options={"verify_ssl": self.__SSL_VERIFY,
                               "access_token_factory": self.login_ws}) \
            .configure_logging(logging.INFO, socket_trace=self.__WS_TRACE) \
            .with_automatic_reconnect({
            "type": "raw",
            "keep_alive_interval": 10,
            "reconnect_interval": 5,
            "max_attempts": 5
        }).build()

        return hub_connection


class PPISSLAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block)


def get_transport_adapter():
    """Creates and returns the transport adaptor for PPI"""
    return PPISSLAdapter()

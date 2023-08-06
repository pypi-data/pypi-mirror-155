from ppi_client.api.constants import MIME_JSON, ACCOUNT_REFRESH_TOKEN, ACCOUNT_LOGIN, MARKETDATA_HUB, ACCOUNTDATA_HUB
from ppi_client.ppi_restclient import RestClient


class PPIClient(object):
    __access_data = None
    __rest_client = None
    token = None
    refreshToken = None
    refreshedCant = 0
    __client_id = None
    __client_secret = None

    ws_connection_marketdata = None
    __on_connect_handler_marketdata = None
    __on_disconnect_handler_marketdata = None
    __on_data_handler_marketdata = None
    __on_error_handler_marketdata = None

    ws_connection_accountdata = None
    __on_connect_handler_accountdata = None
    __on_disconnect_handler_accountdata = None
    __on_data_handler_accountdata = None
    __on_error_handler_accountdata = None

    def __init__(self, version, sandbox):
        if sandbox:
            self.__client_key = 'ppPYTHONDev'
            self.__authorized_client = 'API-PYTHON'
        else:
            self.__client_key = 'pp19CliApp12'
            self.__authorized_client = 'API-CLI'

        self.__rest_client = RestClient(version, sandbox)
        self.__rest_client.client_key = self.__client_key
        self.__rest_client.authorized_client = self.__authorized_client

        self.ws_connection_marketdata = None
        self.__ws_isconnected_marketdata = False

        self.ws_connection_accountdata = None
        self.__ws_isconnected_accountdata = False

    def get_rest_client(self):
        return self.__rest_client

    def get(self, uri, params=None, data=None, content_type=MIME_JSON):
        auth_headers = {'AuthorizedClient': self.__authorized_client, 'ClientKey': self.__client_key}
        if self.token is not None:
            auth_headers.update({'Authorization': 'Bearer ' + self.token})
        res = self.__rest_client.get(uri, params, auth_headers, data, content_type)

        if res.httpStatus == 401 and self.refreshToken is not None and self.refreshedCant < 5:
            try:
                self.renew_token()
                auth_headers.update({'Authorization': 'Bearer ' + self.token})
                return self.get(uri=uri, params=params, data=data)
            except Exception as e:
                print(e)

        if res.httpStatus == 401 and not res.response:
            raise Exception("Unauthorized")
        elif res.httpStatus != 200:
            raise Exception(res.response)

        return res.response

    def post(self, uri, data=None, params=None, content_type=MIME_JSON, api_key=None, api_secret=None):
        auth_headers = {'AuthorizedClient': self.__authorized_client, 'ClientKey': self.__client_key }
        if self.token is not None:
            auth_headers.update({'Authorization': 'Bearer ' + self.token})

        if api_key is not None and api_secret is not None:
            auth_headers.update({'ApiKey': api_key})
            auth_headers.update({'ApiSecret': api_secret})

        res = self.__rest_client.post(uri, data, params, auth_headers, content_type)
        if res.httpStatus == 401 and self.refreshToken is not None and self.refreshedCant < 5:
            try:
                self.renew_token()
                auth_headers.update({'Authorization': 'Bearer ' + self.token})
                return self.post(uri=uri, params=params, data=data)
            except Exception as e:
                print(e)

        if res.httpStatus == 401 and not res.response:
            raise Exception("Unauthorized")
        elif res.httpStatus != 200:
            raise Exception(res.response)

        return res.response

    def put(self, uri, data=None, params=None, content_type=MIME_JSON):
        auth_headers = {'AuthorizedClient': self.__authorized_client, 'ClientKey': self.__client_key}
        if self.token is not None:
            auth_headers.update({'Authorization': 'Bearer ' + self.token})

        res = self.__rest_client.put(uri, data, params, auth_headers, content_type)

        if res.httpStatus == 401 and self.refreshToken is not None and self.refreshedCant < 5:
            try:
                self.renew_token()
                auth_headers.update({'Authorization': 'Bearer ' + self.token})
                return self.put(uri=uri, params=params, data=data)
            except Exception as e:
                print(e)

        if res.httpStatus == 401 and not res.response:
            raise Exception("Unauthorized")
        elif res.httpStatus != 200:
            raise Exception(res.response)

        return res.response

    def delete(self, uri, data=None, params=None, content_type=MIME_JSON):
        auth_headers = {'AuthorizedClient': self.__authorized_client, 'ClientKey': self.__client_key}
        if self.token is not None:
            auth_headers.update({'Authorization': 'Bearer ' + self.token})

        res = self.__rest_client.delete(uri, data, params, auth_headers, content_type)

        if res.httpStatus == 401 and self.refreshToken is not None and self.refreshedCant < 5:
            try:
                self.renew_token()
                auth_headers.update({'Authorization': 'Bearer ' + self.token})
                return self.delete(uri=uri, params=params, data=data)
            except Exception as e:
                print(e)

        if res.httpStatus == 401 and not res.response:
            raise Exception("Unauthorized")
        elif res.httpStatus != 200:
            raise Exception(res.response)

        return res.response

    async def connect_ws_marketdata(self, onconnect_handler=None, ondisconnect_handler=None, marketdata_handler=None):
        self.__on_connect_handler_marketdata = onconnect_handler
        self.__on_disconnect_handler_marketdata = ondisconnect_handler
        self.__on_data_handler_marketdata = marketdata_handler

        if self.ws_connection_marketdata and self.__ws_isconnected_marketdata:
            return self.ws_connection_marketdata
        else:
            conn = await self.__rest_client.connect_to_websocket(MARKETDATA_HUB)
            self.ws_connection_marketdata = conn

            def on_open():
                self.__ws_isconnected_marketdata = True
                self.__on_connect_handler_marketdata()

            def on_marketdata(msj):
                self.__on_data_handler_marketdata(msj[0])

            def on_close(msg):
                lambda: print("connection to marketdata closed" + msg)
                self.__ws_isconnected_marketdata = False
                self.__on_disconnect_handler_marketdata()

            def on_scheduled_disconnection(msg):
                print("connection closed by server")
                conn.stop()
                on_close(msg)

            def on_error():
                lambda data: print(f"An exception on marketdata was thrown closed: {data.error}")

            conn.on_open(on_open)
            conn.on_close(on_close)
            conn.on("marketdata", on_marketdata)
            conn.on("scheduled-md-disconnection", on_scheduled_disconnection)
            conn.on_error(on_error)

            conn.start()
            return conn

    async def connect_ws_accountdata(self, onconnect_handler=None, ondisconnect_handler=None, data_handler=None):
        self.__on_connect_handler_accountdata = onconnect_handler
        self.__on_disconnect_handler_accountdata = ondisconnect_handler
        self.__on_data_handler_accountdata = data_handler

        if self.ws_connection_accountdata and self.__ws_isconnected_account:
            return self.ws_connection_accountdata
        else:
            conn = await self.__rest_client.connect_to_websocket(ACCOUNTDATA_HUB)
            self.ws_connection_accountdata = conn

            def on_open():
                self.__ws_isconnected_accountdata = True
                self.__on_connect_handler_accountdata()

            def on_data(msj):
                self.__on_data_handler_accountdata(msj[0])

            def on_close(msg):
                lambda: print("connection to accountdata closed" + msg)
                self.__ws_isconnected_accountdata = False
                self.__on_disconnect_handler_accountdata()

            def on_scheduled_disconnection(msg):
                print("connection to account data closed by server")
                conn.stop()
                on_close(msg)

            def on_error():
                lambda data: print(f"An exception on account was thrown closed: {data.error}")

            conn.on_open(on_open)
            conn.on_close(on_close)
            conn.on("account", on_data)
            conn.on("scheduled-ac-disconnection", on_scheduled_disconnection)
            conn.on_error(on_error)

            conn.start()
            return conn

    def renew_token(self):
        self.refreshedCant = self.refreshedCant + 1
        auth_headers = {'AuthorizedClient': self.__authorized_client, 'ClientKey': self.__client_key}
        auth_headers.update({'Authorization': 'Bearer ' + self.token})
        body = {
            "refreshToken": self.refreshToken
        }
        res = self.__rest_client.post(ACCOUNT_REFRESH_TOKEN, body, None, auth_headers, MIME_JSON)
        if res.httpStatus == 200:
            self.token = res.response['accessToken']
            self.refreshToken = res.response['refreshToken']
            self.refreshedCant = 0
        elif self.refreshedCant == 5:
            if bool(self.__rest_client.login_ws()):
                self.token = self.__rest_client.token_ws
                self.refreshToken = self.__rest_client.refresh_token_ws
                self.refreshedCant = 0

from ppi_client.ppi_api_client import PPIClient
from ppi_client.api.accounts import AccountsApi
from ppi_client.api.configuration import ConfigurationApi
from ppi_client.api.marketdata import MarketDataApi
from ppi_client.api.orders import OrdersApi
from ppi_client.api.realtime import RealtimeApi


class PPI(object):
    """
    Entrypoint for PPI's API. Provides access to all the available modules.

    Attributes
    ----------
    account : AccountsApi
        Module to login and access account information
    configuration : ConfigurationApi
        Module to access configuration collections endpoints
    marketdata : MarketDataApi
        Module to access market data and instrument endpoints
    realtime : RealtimeApi
        Module to access streaming modules, for market data and notifications
    """
    version = "1.0.4"
    __sandbox = False
    account: AccountsApi = None
    configuration: ConfigurationApi = None
    marketdata: MarketDataApi = None
    orders: OrdersApi = None
    realtime: RealtimeApi = None

    def __init__(self, sandbox=False, *args):
        """
        Instantiate PPI client on the given environment: sandbox or production (default production).

        ppi_client = ppi_client.PPI(sandbox=False)
        """
        self.__sandbox = sandbox

        self.__apiClient = PPIClient(
                                     self.version,
                                     self.__sandbox)

        self.account = AccountsApi(self.__apiClient)
        self.configuration = ConfigurationApi(self.__apiClient)
        self.marketdata = MarketDataApi(self.__apiClient)
        self.orders = OrdersApi(self.__apiClient)
        self.realtime = RealtimeApi(self.__apiClient)


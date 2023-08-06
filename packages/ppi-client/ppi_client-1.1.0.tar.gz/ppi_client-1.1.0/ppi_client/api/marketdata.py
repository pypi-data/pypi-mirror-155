from ppi_client.api.constants import MARKETDATA_SEARCH_INSTRUMENT, MARKETDATA_SEARCH, MARKETDATA_CURRENT, \
    MARKETDATA_BOOK, MARKETDATA_INTRADAY
from ppi_client.ppi_api_client import PPIClient
from ppi_client.models.search_instrument import SearchInstrument
from ppi_client.models.search_datemarketdata import SearchDateMarketData
from ppi_client.models.search_marketdata import SearchMarketData


class MarketDataApi(object):
    __api_client: PPIClient

    def __init__(self, api_client):
        self.__api_client = api_client

    def search_instrument(self, parameters: SearchInstrument):
        """Search for items matching a given filter.
        :param parameters: Parameters for the search: ticker: str, name: str, market: str, type: str
        :type parameters: SearchInstrument
        :rtype: List of instruments
        """
        body = {
            'ticker': parameters.ticker,
            'name': parameters.name,
            'market': parameters.market,
            'type': parameters.type
        }
        return self.__api_client.get(MARKETDATA_SEARCH_INSTRUMENT, data=body)

    def search(self, parameters: SearchDateMarketData):
        """Search for historical market data.
        :param parameters: Parameters for the search: ticker: str, type: str, settlement: str, dateFrom: datetime, dateTo: datetime
        :type parameters: SearchDateMarketData
        :rtype: List of Market Data
        """
        body = {
            "ticker": parameters.ticker,
            "type": parameters.type,
            "settlement": parameters.settlement,
            "dateFrom": parameters.dateFrom,
            "dateTo": parameters.dateTo
        }
        return self.__api_client.get(MARKETDATA_SEARCH, data=body)

    def current(self, parameters: SearchMarketData):
        """Search for current market data.
        :param parameters: Parameters for the search: ticker: str, type: str, settlement: str
        :type parameters: SearchMarketData
        :rtype: current Market Data
        """
        body = {
            "ticker": parameters.ticker,
            "type": parameters.type,
            "settlement": parameters.settlement
        }
        return self.__api_client.get(MARKETDATA_CURRENT, data=body)

    def book(self, parameters: SearchMarketData):
        """Search for current book information.
        :param parameters: Parameters for the search: ticker: str, type: str, settlement: str
        :type parameters: SearchMarketData
        :rtype: current Book
        """
        body = {
            "ticker": parameters.ticker,
            "type": parameters.type,
            "settlement": parameters.settlement
        }
        return self.__api_client.get(MARKETDATA_BOOK, data=body)

    def intraday(self, parameters: SearchMarketData):
        """Search for intraday market data.
        :param parameters: Parameters for the search: ticker: str, type: str, settlement: str
        :type parameters: SearchMarketData
        :rtype: list of intraday Market Data
        """
        body = {
            "ticker": parameters.ticker,
            "type": parameters.type,
            "settlement": parameters.settlement
        }
        return self.__api_client.get(MARKETDATA_INTRADAY, data=body)


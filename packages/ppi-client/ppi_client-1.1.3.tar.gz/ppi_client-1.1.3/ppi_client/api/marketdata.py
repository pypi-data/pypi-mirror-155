from ppi_client.api.constants import MARKETDATA_SEARCH_INSTRUMENT, MARKETDATA_SEARCH, MARKETDATA_CURRENT, \
    MARKETDATA_BOOK, MARKETDATA_INTRADAY
from ppi_client.ppi_api_client import PPIClient
from datetime import datetime

class MarketDataApi(object):
    __api_client: PPIClient

    def __init__(self, api_client):
        self.__api_client = api_client

    def search_instrument(self, ticker: str, instrument_name: str, market: str, instrument_type: str):
        """Search for items matching a given filter.
        :param ticker: ticker
        :param instrument_name: instrument_name
        :param market: market
        :param instrument_type: instrument_type
        :rtype: List of instruments
        """

        test = MARKETDATA_SEARCH_INSTRUMENT.format(ticker, instrument_name, market, instrument_type)


        return self.__api_client.get(MARKETDATA_SEARCH_INSTRUMENT.format(ticker, instrument_name, market,
                                                                         instrument_type))

    def search(self, ticker: str, instrument_type: str, settlement: str, date_from: datetime, date_to: datetime):
        """Search for historical market data.
        :param ticker: ticker
        :param instrument_type: instrument type
        :param settlement: settlement
        :param date_from: date from
        :param date_to: date to

        :rtype: List of Market Data
        """
        return self.__api_client.get(MARKETDATA_SEARCH.format(ticker, instrument_type, date_from, date_to, settlement))

    def current(self, ticker: str, instrument_type: str, settlement: str):
        """Search for current market data.
        :param ticker: ticker
        :param instrument_type: instrument type
        :param settlement: settlement
        :rtype: current Market Data
        """

        return self.__api_client.get(MARKETDATA_CURRENT.format(ticker, instrument_type, settlement))

    def book(self, ticker: str, instrument_type: str, settlement: str):
        """Search for current book information.
        :param ticker: ticker
        :param instrument_type: instrument type
        :param settlement: settlement
        :rtype: current Book
        """

        return self.__api_client.get(MARKETDATA_BOOK.format(ticker, instrument_type, settlement))

    def intraday(self, ticker: str, instrument_type: str, settlement: str):
        """Search for intraday market data.
        :param ticker: ticker
        :param instrument_type: instrument type
        :param settlement: settlement
        :rtype: list of intraday Market Data
        """

        return self.__api_client.get(MARKETDATA_INTRADAY.format(ticker, instrument_type, settlement))


from ppi_client.api.constants import CONFIGURATION_INSTRUMENT_TYPES, CONFIGURATION_MARKETS, CONFIGURATION_SETTLEMENTS, \
    CONFIGURATION_QUANTITY_TYPES, \
    CONFIGURATION_OPERATION_TERMS, CONFIGURATION_OPERATION_TYPES, CONFIGURATION_OPERATIONS, CONFIGURATION_HOLIDAYS, \
    CONFIGURATION_IS_LOCAL_HOLIDAY, CONFIGURATION_IS_USA_HOLIDAY
from ppi_client.ppi_api_client import PPIClient
from datetime import datetime

class ConfigurationApi(object):
    __api_client: PPIClient

    def __init__(self, api_client):
        self.__api_client = api_client

    def get_instrument_types(self):
        """Retrieves a list of available instrument types.

        :rtype: List of instrument types
        """
        return self.__api_client.get(CONFIGURATION_INSTRUMENT_TYPES, None)

    def get_markets(self):
        """Retrieves a list of available markets.

        :rtype: List of markets
        """
        return self.__api_client.get(CONFIGURATION_MARKETS, None)

    def get_settlements(self):
        """Retrieves a list of available settlements.

        :rtype: List of settlements
        """
        return self.__api_client.get(CONFIGURATION_SETTLEMENTS, None)

    def get_quantity_types(self):
        """Retrieves a list of available quantity types.

        :rtype: List of quantity types
        """
        return self.__api_client.get(CONFIGURATION_QUANTITY_TYPES, None)

    def get_operation_terms(self):
        """Retrieves a list of available operation terms.

        :rtype: List of operation terms
        """
        return self.__api_client.get(CONFIGURATION_OPERATION_TERMS, None)

    def get_operation_types(self):
        """Retrieves a list of available operation types.

        :rtype: List of operation types
        """
        return self.__api_client.get(CONFIGURATION_OPERATION_TYPES, None)

    def get_operations(self):
        """Retrieves a list of available operations.

        :rtype: List of operations
        """
        return self.__api_client.get(CONFIGURATION_OPERATIONS, None)

    def get_holidays(self, start_date: datetime = None, end_date: datetime = None, is_usa: bool = False):
        """Retrieves a list of holidays.

        :rtype: List of holidays
        """
        params = {
            'start': start_date,
            'end': end_date,
            'isUSA': is_usa
            }
        return self.__api_client.get(CONFIGURATION_HOLIDAYS, params=params)

    def is_local_holiday(self):
        """Retrieves if actual date is a local holiday.

        :rtype: Boolean
        """
        return self.__api_client.get(CONFIGURATION_IS_LOCAL_HOLIDAY, None)

    def is_usa_holiday(self):
        """Retrieves if actual date is a holiday in the USA.

        :rtype: Boolean
        """
        return self.__api_client.get(CONFIGURATION_IS_USA_HOLIDAY, None)

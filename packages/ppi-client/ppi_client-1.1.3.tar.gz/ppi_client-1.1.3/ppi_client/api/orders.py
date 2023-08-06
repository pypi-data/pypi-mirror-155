from ppi_client.api.constants import ORDER_ORDERS, ORDER_DETAIL, \
    ORDER_BUDGET, ORDER_CONFIRM, ORDER_CANCEL, ORDER_MASS_CANCEL, ORDER_ACTIVE_ORDERS
from ppi_client.ppi_api_client import PPIClient
from ppi_client.models.order import Order
from ppi_client.models.order_budget import OrderBudget
from ppi_client.models.order_confirm import OrderConfirm
from datetime import datetime

class OrdersApi(object):
    __api_client: PPIClient

    def __init__(self, api_client):
        self.__api_client = api_client

    def get_orders(self, account_number: str, date_from: datetime, date_to: datetime):
        """Retrieves all the filter and active orders for the given account.
        :param account_number: account number
        :param date_from: date from
        :param date_to: date to
        :rtype: List of orders between two dates
        """

        return self.__api_client.get(ORDER_ORDERS.format(account_number, date_from, date_to))

    def get_active_orders(self, account_number: str):
        """Retrieves all the active orders for the given account.
        :param account_number: account number
        :rtype: List of active orders
        """

        return self.__api_client.get(ORDER_ACTIVE_ORDERS.format(account_number))

    def get_order_detail(self, account_number: str, order_id: str, external_id: str):
        """Retrieves the information for the order.
        :param account_number: account number
        :param order_id: order id
        :param external_id: external id
        :rtype: Order information
        """

        return self.__api_client.get(ORDER_DETAIL.format(account_number, order_id, external_id))

    def budget(self, parameters: OrderBudget):
        """Retrieves a budget for a new order.
        :param parameters: Parameters for the budget: account_number: str, quantity: int, price: int,
        ticker: str, instrumentType: str, quantityType: str, operationType: str, operationTerm: str,
        operationMaxDate: datetime, operation: str, settlement: str, activationPrice: decimal
        :type parameters: OrderBudget
        :rtype: Order budget
        """
        body = {
            "accountNumber": parameters.accountNumber,
            "quantity": parameters.quantity,
            "price": parameters.price,
            "ticker": parameters.ticker,
            "instrumentType": parameters.instrumentType,
            "quantityType": parameters.quantityType,
            "operationType": parameters.operationType,
            "operationTerm": parameters.operationTerm,
            "operationMaxDate": parameters.operationMaxDate,
            "operation": parameters.operation,
            "settlement": parameters.settlement,
            "activationPrice": parameters.activationPrice
        }
        result = self.__api_client.post(ORDER_BUDGET, data=body)

        return result

    def confirm(self, parameters: OrderConfirm):
        """Confirm the creation for a new order.
        :param parameters: Parameters for the confirmation: account_number: str, quantity: int, price: int,
        ticker: str, instrumentType: str, quantityType: str, operationType: str, operationTerm: str,
        operationMaxDate: datetime, operation: str, settlement: str, disclaimers: dict [str, bool], externalId: str,
        activationPrice: decimal
        :type parameters: OrderConfirm
        :rtype: Order information
        """
        disclaimers = []
        if parameters.disclaimers is not None:
            for disclaimer in parameters.disclaimers:
                disclaimers.append({"code": disclaimer.code,
                                    "accepted": disclaimer.accepted
                                    })
        body = {
            "accountNumber": parameters.accountNumber,
            "quantity": parameters.quantity,
            "price": parameters.price,
            "ticker": parameters.ticker,
            "instrumentType": parameters.instrumentType,
            "quantityType": parameters.quantityType,
            "operationType": parameters.operationType,
            "operationTerm": parameters.operationTerm,
            "operationMaxDate": parameters.operationMaxDate,
            "operation": parameters.operation,
            "settlement": parameters.settlement,
            "disclaimers": disclaimers,
            "externalId": parameters.externalId,
            "activationPrice": parameters.activationPrice
        }
        result = self.__api_client.post(ORDER_CONFIRM, data=body)
        return result

    def cancel_order(self, parameters: Order):
        """Request the cancel for an order.
        :param parameters: Parameters for the cancel request: account_number: str, orderId: int, externalID: string
        :type parameters: Order
        :rtype: Order information
        """
        body = {
            "accountNumber": parameters.account_number,
            "orderID": parameters.id,
            "externalID": parameters.externalId
        }

        return self.__api_client.post(ORDER_CANCEL, data=body)

    def mass_cancel_order(self, account_number: str):
        """Request the cancel for all alive orders for the given account.
        :param account_number: account number
        :type account_number: str
        :rtype: Order message
        """

        return self.__api_client.post(ORDER_MASS_CANCEL.format(account_number))

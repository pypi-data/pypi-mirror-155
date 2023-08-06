import decimal
from dataclasses import dataclass
from datetime import datetime


@dataclass
class OrderConfirm:
    accountNumber: str
    quantity: int
    price: decimal
    ticker: str
    instrumentType: str
    quantityType: str
    operationType: str
    operationTerm: str
    operationMaxDate: datetime
    operation: str
    settlement: str
    disclaimers: str
    externalId: str
    activationPrice: decimal = None

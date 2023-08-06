import decimal
from dataclasses import dataclass
from datetime import datetime


@dataclass
class OrderBudget:
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
    activationPrice: decimal = None

from dataclasses import dataclass
from datetime import datetime


@dataclass
class OrdersFilter:
    from_date: datetime
    to_date: datetime
    account_number: str

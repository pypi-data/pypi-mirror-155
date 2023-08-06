from dataclasses import dataclass
from datetime import datetime


@dataclass
class AccountMovements:
    account_number: str
    from_date: datetime
    to_date: datetime
    ticker: str

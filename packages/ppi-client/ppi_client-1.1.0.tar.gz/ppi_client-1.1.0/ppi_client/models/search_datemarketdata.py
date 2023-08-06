from dataclasses import dataclass
from datetime import datetime


@dataclass
class SearchDateMarketData:
    ticker: str
    type: str
    settlement: str
    dateFrom: datetime
    dateTo: datetime

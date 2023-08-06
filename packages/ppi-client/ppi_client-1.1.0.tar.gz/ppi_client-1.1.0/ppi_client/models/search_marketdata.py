from dataclasses import dataclass


@dataclass
class SearchMarketData:
    ticker: str
    type: str
    settlement: str

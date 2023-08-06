from dataclasses import dataclass


@dataclass
class SearchInstrument:
    ticker: str
    name: str
    market: str
    type: str

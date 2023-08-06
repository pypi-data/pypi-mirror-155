from dataclasses import dataclass


@dataclass
class Instrument:
    ticker: str
    type: str
    settlement: str

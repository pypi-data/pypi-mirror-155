from dataclasses import dataclass


@dataclass
class Order:
    id: int
    account_number: str
    externalId: str

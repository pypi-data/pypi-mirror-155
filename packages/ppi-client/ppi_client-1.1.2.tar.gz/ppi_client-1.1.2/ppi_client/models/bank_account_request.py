from dataclasses import dataclass


@dataclass
class BankAccountRequest:
    account_number: str
    currency: str
    cbu: str
    cuit: str
    alias: str
    bank_account_number: str

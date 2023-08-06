from dataclasses import dataclass


@dataclass
class CancelBankAccountRequest:
    account_number: str
    cbu: str
    bank_account_number: str

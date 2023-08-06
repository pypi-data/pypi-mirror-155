from dataclasses import dataclass


@dataclass
class ForeignBankAccountRequestDTO:
    account_number: str
    cuit: str
    intermediary_bank: str
    intermediary_bank_account_number: str
    intermediary_bank_swift: str
    bank: str
    bank_account_number: str
    swift: str
    ffc: str
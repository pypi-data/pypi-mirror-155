from dataclasses import dataclass
from ppi_client.models.foreign_bank_account_request_dto import ForeignBankAccountRequestDTO

@dataclass
class ForeignBankAccountRequest:
    request: ForeignBankAccountRequestDTO
    extract_file: bytes

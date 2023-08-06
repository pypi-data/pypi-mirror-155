from ppi_client.api.constants import ACCOUNT_LOGIN, ACCOUNT_REFRESH_TOKEN, ACCOUNT_ACCOUNTS, ACCOUNT_BANK_ACCOUNTS, \
    ACCOUNT_AVAILABLE_BALANCE, ACCOUNT_BALANCE_POSITIONS, ACCOUNT_MOVEMENTS, ACCOUNT_INVESTING_PROFILE_QUESTIONS, \
    ACCOUNT_INVESTING_PROFILE_INSTRUMENT_TYPES, ACCOUNT_INVESTING_PROFILE, ACCOUNT_SET_INVESTING_PROFILE, \
    ACCOUNT_REGISTER_BANK_ACCOUNT, ACCOUNT_REGISTER_FOREIGN_BANK_ACCOUNT, ACCOUNT_CANCEL_BANK_ACCOUNT, ACCOUNT_LOGIN_API
from ppi_client.ppi_api_client import PPIClient
from ppi_client.models.account_movements import AccountMovements
from ppi_client.models.investing_profile import InvestingProfile
from ppi_client.models.bank_account_request import BankAccountRequest
from ppi_client.models.foreign_bank_account_request import ForeignBankAccountRequest
from ppi_client.models.cancel_bank_account_request import CancelBankAccountRequest
from requests_toolbelt import MultipartEncoder
import json

class AccountsApi(object):
    __api_client: PPIClient

    def __init__(self, api_client):
        self.__api_client = api_client

    def login(self, client_id: str, client_secret: str):
        """Tries to log in with the given credentials. Returns a session token which is needed to use the API.

        :param client_id: Client id
        :type client_id: str
        :param client_secret: Client secret
        :type client_secret: str
        :rtype: authorization payload, including access_token, refresh_token and expiration date.
        """
        login = {
            "user": client_id,
            "password": client_secret
        }
        res = self.__api_client.post(ACCOUNT_LOGIN, data=login)
        self.__api_client.token = res['accessToken']
        self.__api_client.refreshToken = res['refreshToken']
        self.__api_client.refreshedCant = 0
        self.__api_client.get_rest_client().client_id = client_id
        self.__api_client.get_rest_client().client_secret = client_secret

        return res

    def login_api(self, api_key: str, api_secret: str):
        """Tries to log in with the given api credentials. Returns a session token which is needed to use the API.

        :param api_key: api key
        :type api_secret: str
        :param api_secret: api secret
        :type api_secret: str
        :rtype: authorization payload, including access_token, refresh_token and expiration date.
        """

        res = self.__api_client.post(ACCOUNT_LOGIN_API, api_key=api_key, api_secret=api_secret)
        self.__api_client.token = res['accessToken']
        self.__api_client.refreshToken = res['refreshToken']
        self.__api_client.refreshedCant = 0
        self.__api_client.get_rest_client().api_key = api_key
        self.__api_client.get_rest_client().api_secret = api_secret

        return res

    def get_accounts(self):
        """Retrieves all the available accounts and their officer for the current session.

        :rtype: list of accounts
        """
        return self.__api_client.get(ACCOUNT_ACCOUNTS, None)

    def get_bank_accounts(self, account_number: str):
        """Retrieves all the available bank accounts for the given account.

        :param account_number: Account number to retrieve bank accounts
        :type account_number: str
        :rtype: list of bank accounts
        """
        return self.__api_client.get(ACCOUNT_BANK_ACCOUNTS.format(account_number))

    def get_available_balance(self, account_number: str):
        """Retrieves cash balance available for trading for the given account.

        :param account_number: Account number to retrieve availability
        :type account_number: str
        :rtype: List of availability
        """
        return self.__api_client.get(ACCOUNT_AVAILABLE_BALANCE.format(account_number))

    def get_balance_and_positions(self, account_number: str):
        """Retrieves account balance and positions for the given account.

        :param account_number: Account number to retrieve balance and position
        :type account_number: Grouped availability and grouped instruments
        """
        return self.__api_client.get(ACCOUNT_BALANCE_POSITIONS.format(account_number))

    def get_movements(self, parameters: AccountMovements):
        """Retrieves movements for the given account between the specified dates.

        :param parameters: Parameters for the report: account_number: str, from_date: datetime, to_date: datetime, ticker: str
        :type parameters: AccountMovements
        :rtype: List of movements
        """
        params = {
            'dateFrom': parameters.from_date,
            'dateTo': parameters.to_date,
            'ticker': parameters.ticker
            }
        return self.__api_client.get(ACCOUNT_MOVEMENTS.format(parameters.account_number), params=params)

    def get_investing_profile_questions(self):
        """Retrieves questions and possible answers for investing profile test.
        :rtype: List of investing profile questions and answers
        """
        return self.__api_client.get(ACCOUNT_INVESTING_PROFILE_QUESTIONS, None)

    def get_investing_profile_instrument_types(self):
        """Retrieves instrument types for investing profile test.
        :rtype: List of investing profile instrument types
        """
        return self.__api_client.get(ACCOUNT_INVESTING_PROFILE_INSTRUMENT_TYPES, None)

    def get_investing_profile(self, account_number: str):
        """Retrieves investing profile result for the given account.
        :param account_number: Account number to retrieve investing profile
        :type account_number: str
        """
        return self.__api_client.get(ACCOUNT_INVESTING_PROFILE.format(account_number))

    def set_investing_profile(self, parameters: InvestingProfile):
        """Set a new investing profile for the given account.
        :param parameters: Parameters of InvestingProfile: account_number: str, answers: [], instrument_types: []
        :type parameters: InvestingProfile
        :rtype: Investing Profile information
        """
        answers = []
        if parameters.answers is not None:
            for answer in parameters.answers:
                answers.append({"QuestionCode": answer.question_code,
                                "AnswerCode": answer.answer_code})
        body = {
            "AccountNumber": parameters.account_number,
            "Answers": answers,
            "InstrumentTypes": parameters.instrument_types
        }
        result = self.__api_client.post(ACCOUNT_SET_INVESTING_PROFILE, data=body)
        return result

    def register_bank_account(self, parameters: BankAccountRequest):
        """Register a bank account for the given account.
        :param parameters: Parameters of BankAccountRequest: account_number: str, currency: str, cbu: str,
        cuit: str, alias: str, bank_account_number: str
        :type parameters: BankAccountRequest
        :rtype: String message with information of the request
        """
        data = {
            "AccountNumber": parameters.account_number,
            "Currency": parameters.currency,
            "CBU": parameters.cbu,
            "Cuit": parameters.cuit,
            "Alias": parameters.alias,
            "BankAccountNumber": parameters.bank_account_number
        }
        result = self.__api_client.post(ACCOUNT_REGISTER_BANK_ACCOUNT, data=data)
        return result

    def register_foreign_bank_account(self, parameters: ForeignBankAccountRequest):
        """Register a foreign bank account for the given account.
        :param parameters: Parameters of ForeignBankAccountRequest: request: ForeignBankAccountRequestDTO,
        extract_file: bytes
        :type parameters: ForeignBankAccountRequest
        :rtype: String message with information of the request
        """
        dto = {
            "AccountNumber": parameters.request.account_number,
            "Cuit": parameters.request.cuit,
            "IntermediaryBank": parameters.request.intermediary_bank,
            "IntermediaryBankAccountNumber": parameters.request.intermediary_bank_account_number,
            "SwiftIntermediaryBank": parameters.request.intermediary_bank_swift,
            "Bank": parameters.request.bank,
            "BankAccountNumber": parameters.request.bank_account_number,
            "Swift": parameters.request.swift,
            "FFC": parameters.request.ffc,
        }
        multipart_data = MultipartEncoder(
            fields={
                'ExtractFile': parameters.extract_file,
                'Request': json.dumps(dto)
            }
        )
        result = self.__api_client.post(ACCOUNT_REGISTER_FOREIGN_BANK_ACCOUNT, data=multipart_data,
                                        content_type=multipart_data.content_type)
        return result

    def cancel_bank_account(self, parameters: CancelBankAccountRequest):
        """Cancel a bank account for the given account.
        :param parameters: Parameters of CancelBankAccountRequest: account_number: str, cbu: str,
        bank_account_number: str
        :type parameters: CancelBankAccountRequest
        :rtype: String message with information of the request
        """
        data = {
            "AccountNumber": parameters.account_number,
            "CBU": parameters.cbu,
            "BankAccountNumber": parameters.bank_account_number
        }
        result = self.__api_client.post(ACCOUNT_CANCEL_BANK_ACCOUNT, data=data)
        return result

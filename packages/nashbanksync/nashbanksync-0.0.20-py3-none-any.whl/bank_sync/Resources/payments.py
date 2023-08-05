from bank_sync.Resources.resource import Resource
from bank_sync.APIs.utils.generate_code import get_code
from datetime import date


class Payments(Resource):

    urls = {}

    def set_bank_id(self, bank_id):
        super().set_action(action='payment')
        return super().set_bank_id(bank_id)

    def ift(self, payload=None):

        return super().read(payload=payload)

    def eft(self, payload=None):

        return super().read(payload=payload)

    def rtgs(self, payload=None):

        return super().read(payload=payload)

    def swift(self, payload=None):

        return super().read(payload=payload)

    def transaction_status(self, payload=None):

        return super().read(payload=payload)

    def mobile_wallet(self, payload=None):

        return super().read(payload=payload)

    def pesalink_to_bank(self, payload=None):

        return super().read(payload=payload)

    def pesalink_to_mobile(self, payload=None):

        return super().read(payload=payload)

    # API Endpoint used by third party integrations
    def initiate_payment(self, payload=None):

        return super().read(payload=payload)

    def serialize(self, payload=None, operation=None):

        # Might need refractoring
        super().set_operation(operation)

        data = {}

        if operation is None:
            return "Specify the operation: Resource.BALANCE, Resource.MINI_STATEMENT, Resource.FULL_STATEMENT, Resource.ACCOUNT_VALIDATION or Resource.ACCOUNT_TRANSACTIONS"

        if operation == super().IFT:

            # If bank_id is COOP
            if super().get_bank_id() == super().COOP:
                data.update({
                    "MessageReference": f'{get_code(length=14)}'
                })
                data.update({
                    "CallBackUrl": payload.get("transfer", {}).get("callback_url", "")
                })
                data.update({
                    "Source": {
                        "AccountNumber": payload.get("source", {}).get("account_number", None),
                        "Amount": payload.get("source", {}).get("amount", None),
                        "TransactionCurrency": payload.get("transfer", {}).get("currency_code", None),
                        "Narration": payload.get("transfer", {}).get("description", "")
                    }
                })

                destinations = payload.get("destinations", [])

                for i in range(len(destinations)):
                    if i == 0:
                        data.update({
                            "Destinations": []
                        })

                    data["Destinations"].append(
                        {
                            "ReferenceNumber": payload.get("transfer", {}).get("reference", None),
                            "AccountNumber": destinations[i].get("account_number", None),
                            "BankCode": payload.get("transfer", {}).get("bank_code", None),
                            "BranchCode": payload.get("transfer", {}).get("branch_code", None),
                            "Amount": destinations[i].get("amount", None),
                            "TransactionCurrency": payload.get("transfer", {}).get("currency_code", None),
                            "Narration": payload.get("transfer", {}).get("description", "")
                        }
                    )
            # If bank_id is EQUITY
            elif super().get_bank_id() == super().EQUITY:
                data.update({
                    "source": {
                        "countryCode": payload.get("source", {}).get("country_code", None),
                        "name": payload.get("source", {}).get("name", None),
                        "accountNumber": payload.get("source", {}).get("account_number", None)
                    }
                })

                destinations = payload.get("destinations", [])
                if len(destinations) > 0:
                    destination = destinations[0]

                    data.update({
                        "destination": {
                            "type": "bank",
                            "countryCode": destination.get("country_code", None),
                            "name": destination.get("name", None),
                            "accountNumber": destination.get("account_number", None),
                        }
                    })

                    data.update({
                        "transfer": {
                            "type": "InternalFundsTransfer",
                            "amount": f'{destination.get("amount",None)}',
                            "currencyCode": payload.get("transfer", {}).get("currency_code", None),
                            "reference": payload.get("transfer", {}).get("reference", None),
                            "date": payload.get("transfer", {}).get("date", None),
                            "description": payload.get("transfer", {}).get("description", ""),
                        }
                    })
            # If bank_id is NCBA
            elif super().get_bank_id() == super().NCBA:

                destinations = payload.get("destinations", [])
                if len(destinations) > 0:
                    destination = destinations[0]

                    date = payload.get("transfer", {}).get("date", None)
                    if date is not None:
                        date = date.split("-")
                        if len(date) > 0:
                            date = f'{date[0]}{date[1]}{date[2]}'

                    data.update({
                        "BankCode": payload.get("transfer", {}).get("bank_code", None),
                        "BankSwiftCode": payload.get("transfer", {}).get("bank_swift_code", None),
                        "BranchCode": payload.get("transfer", {}).get("branch_code", None),
                        "BeneficiaryAccountName": payload.get("destination", {}).get("name", None),
                        "Country": payload.get("transfer", {}).get("country", None),
                        "Reference": f'{get_code(length=14)}',
                        "Currency": payload.get("transfer", {}).get("currency_code", None),
                        "Account": destination.get("account_number", None),
                        "Amount": destination.get("amount", None),
                        "Narration": payload.get("transfer", {}).get("description", None),
                        "Transaction Date": date,
                    })
        elif operation == super().MOBILE_WALLET:

            # If bank_id is COOP
            if super().get_bank_id() == super().COOP:
                data.update({
                    "MessageReference": f'{get_code(length=14)}'
                })
                data.update({
                    "CallBackUrl": payload.get("transfer", {}).get("callback_url", "")
                })
                data.update({
                    "Source": {
                        "AccountNumber": f'{payload.get("source", {}).get("account_number", None)}',
                        "Amount": payload.get("source", {}).get("amount", None),
                        "TransactionCurrency": payload.get("transfer", {}).get("currency_code", None),
                        "Narration": payload.get("transfer", {}).get("description", "")
                    }
                })

                destinations = payload.get("destinations", [])

                for i in range(len(destinations)):
                    if i == 0:
                        data.update({
                            "Destinations": []
                        })

                    data["Destinations"].append(
                        {
                            "ReferenceNumber": payload.get("transfer", {}).get("reference", None),
                            "MobileNumber": f'{destinations[i].get("mobile_number",None)}',
                            "Amount": destinations[i].get("amount", None),
                            "Narration": payload.get("transfer", {}).get("description", "")
                        }
                    )
            # If bank_id is EQUITY
            elif super().get_bank_id() == super().EQUITY:
                data.update({
                    "source": {
                        "countryCode": payload.get("source", {}).get("country_code", None),
                        "name": payload.get("source", {}).get("name", None),
                        "accountNumber": payload.get("source", {}).get("account_number", None)
                    }
                })

                destinations = payload.get("destinations", [])
                if len(destinations) > 0:
                    destination = destinations[0]

                    data.update({
                        "destination": {
                            "type": "mobile",
                            "countryCode": destination.get("country_code", None),
                            "name": destination.get("name", None),
                            "mobileNumber": destination.get("mobile_number", None),
                            "walletName": destination.get("wallet_name", None),
                        }
                    })

                    data.update({
                        "transfer": {
                            "type": "MobileWallet",
                            "amount": f'{destination.get("amount",None)}',
                            "currencyCode": payload.get("transfer", {}).get("currency_code", None),
                            "reference": payload.get("transfer", {}).get("reference", None),
                            "date": payload.get("transfer", {}).get("date", None),
                            "description": payload.get("transfer", {}).get("description", ""),
                        }
                    })
            # If bank_id is NCBA
            elif super().get_bank_id() == super().NCBA:

                destinations = payload.get("destinations", [])
                if len(destinations) > 0:
                    destination = destinations[0]

                    date = payload.get("transfer", {}).get("date", None)
                    if date is not None:
                        date = date.split("-")
                        if len(date) > 0:
                            date = f'{date[0]}{date[1]}{date[2]}'

                    data.update({
                        "BankCode": payload.get("transfer", {}).get("bank_code", None),
                        "BankSwiftCode": payload.get("transfer", {}).get("bank_swift_code", None),
                        "BranchCode": payload.get("transfer", {}).get("branch_code", None),
                        "BeneficiaryAccountName": destination.get("name", None),
                        "Country": payload.get("transfer", {}).get("country", None),
                        "TranType": "Mpesa",
                        "Reference": f'{get_code(length=14)}',
                        "Currency": payload.get("transfer", {}).get("currency_code", None),
                        "Account": destination.get("mobile_number", None),
                        "Amount": destination.get("amount", None),
                        "Narration": payload.get("transfer", {}).get("description", None),
                        "Transaction Date": date,
                        "Validation ID": f'{get_code(length=14)}',
                    })
        elif operation == super().RTGS:

            # If bank_id is COOP
            if super().get_bank_id() == super().COOP:
                pass
            elif super().get_bank_id() == super().EQUITY:
                data.update({
                    "source": {
                        "countryCode": payload.get("source", {}).get("country_code", None),
                        "name": payload.get("source", {}).get("name", None),
                        "accountNumber": payload.get("source", {}).get("account_number", None),
                        "currency": payload.get("transfer", {}).get("currency_code", None),
                    }
                })

                destinations = payload.get("destinations", [])
                if len(destinations) > 0:
                    destination = destinations[0]

                    data.update({
                        "destination": {
                            "type": "bank",
                            "countryCode": destination.get("country_code", None),
                            "name": destination.get("name", None),
                            "bankCode": payload.get("transfer", {}).get("bank_code", None),
                            "accountNumber": f'{destination.get("account_number",None)}',
                        }
                    })

                    data.update({
                        "transfer": {
                            "type": "RTGS",
                            "amount": f'{destination.get("amount",None)}',
                            "currencyCode": payload.get("transfer", {}).get("currency_code", None),
                            "reference": payload.get("transfer", {}).get("reference", None),
                            "date": payload.get("transfer", {}).get("date", None),
                            "description": payload.get("transfer", {}).get("description", ""),
                        }
                    })
            # If bank_id is NCBA
            elif super().get_bank_id() == super().NCBA:

                destinations = payload.get("destinations", [])
                if len(destinations) > 0:
                    destination = destinations[0]

                    date = payload.get("transfer", {}).get("date", None)
                    if date is not None:
                        if len(date.split("-")) == 3:
                            date = date.split("-")
                            date = f'{date[0]}{date[1]}{date[2]}'

                    data.update({
                        "BankCode": payload.get("transfer", {}).get("bank_code", None),
                        "BankSwiftCode": payload.get("transfer", {}).get("bank_swift_code", None),
                        "BranchCode": payload.get("transfer", {}).get("branch_code", None),
                        "BeneficiaryAccountName": destination.get("name", None),
                        "Country": payload.get("transfer", {}).get("country", None),
                        "TranType": "RTGS",
                        "Reference": f'{get_code(length=14)}',
                        "Currency": payload.get("transfer", {}).get("currency_code", None),
                        "Account": destination.get("account_number", None),
                        "Amount": destination.get("amount", None),
                        "Narration": payload.get("transfer", {}).get("description", None),
                        "Transaction Date": date,
                    })
        elif operation == super().SWIFT:

            # If bank_id is COOP
            if super().get_bank_id() == super().EQUITY:
                data.update({
                    "source": {
                        "countryCode": payload.get("source", {}).get("country_code", None),
                        "name": payload.get("source", {}).get("name", None),
                        "accountNumber": payload.get("source", {}).get("account_number", None),
                        "sourceCurrency": payload.get("transfer", {}).get("currency_code", None),
                    }
                })

                destinations = payload.get("destinations", [])
                if len(destinations) > 0:
                    destination = destinations[0]

                    data.update({
                        "destination": {
                            "type": "bank",
                            "countryCode": destination.get("country_code", None),
                            "name": destination.get("name", None),
                            "bankBic": destination.get("bank_bic", None),
                            "accountNumber": f'{destination.get("account_number",None)}',
                            "addressline1": f'{destination.get("address",None)}',
                            "currency": destination.get("currency_code", None),
                        }
                    })

                    data.update({
                        "transfer": {
                            "type": "SWIFT",
                            "amount": f'{destination.get("amount",None)}',
                            "currencyCode": payload.get("transfer", {}).get("currency_code", None),
                            "reference": payload.get("transfer", {}).get("reference", None),
                            "date": payload.get("transfer", {}).get("date", None),
                            "description": payload.get("transfer", {}).get("description", ""),
                            "chargeOption": "SELF"
                        }
                    })
        elif operation == super().EFT:

            # If bank_id is COOP
            if super().get_bank_id() == super().COOP:
                pass
            elif super().get_bank_id() == super().EQUITY:
                pass
            # If bank_id is NCBA
            elif super().get_bank_id() == super().NCBA:

                destinations = payload.get("destinations", [])
                if len(destinations) > 0:
                    destination = destinations[0]

                    date = payload.get("transfer", {}).get("date", None)
                    if date is not None:
                        date = date.split("-")
                        if len(date) > 0:
                            date = f'{date[0]}{date[1]}{date[2]}'

                    data.update({
                        "BankCode": payload.get("transfer", {}).get("bank_code", None),
                        "BankSwiftCode": payload.get("transfer", {}).get("bank_swift_code", None),
                        "BranchCode": payload.get("transfer", {}).get("branch_code", None),
                        "BeneficiaryAccountName": destination.get("name", None),
                        "BeneficiaryName": destination.get("name", None),
                        "Country": payload.get("transfer", {}).get("country", None),
                        "Reference": f'{get_code(length=14)}',
                        "Currency": payload.get("transfer", {}).get("currency_code", None),
                        "Account": destination.get("account_number", None),
                        "Amount": f'{destination.get("amount", None)}',
                        "Narration": payload.get("transfer", {}).get("description", None),
                        "Transaction Date": date,
                    })
        elif operation == super().PESALINK_TO_BANK:

            # If bank_id is COOP
            if super().get_bank_id() == super().COOP:
                data.update({
                    "MessageReference": f'{get_code(length=14)}'
                })
                data.update({
                    "CallBackUrl": payload.get("transfer", {}).get("callback_url", "")
                })
                data.update({
                    "Source": {
                        "AccountNumber": payload.get("source", {}).get("account_number", None),
                        "Amount": payload.get("source", {}).get("amount", None),
                        "TransactionCurrency": payload.get("transfer", {}).get("currency_code", None),
                        "Narration": payload.get("transfer", {}).get("description", "")
                    }
                })

                destinations = payload.get("destinations", [])

                for i in range(len(destinations)):
                    if i == 0:
                        data.update({
                            "Destinations": []
                        })

                    data["Destinations"].append(
                        {
                            "ReferenceNumber": payload.get("transfer", {}).get("reference", None),
                            "AccountNumber": destinations[i].get("account_number", None),
                            "BankCode": payload.get("transfer", {}).get("bank_code", None),
                            "Amount": destinations[i].get("amount", None),
                            "TransactionCurrency": payload.get("transfer", {}).get("currency_code", None),
                            "Narration": payload.get("transfer", {}).get("description", "")
                        }
                    )
            # If bank_id is EQUITY
            elif super().get_bank_id() == super().EQUITY:
                data.update({
                    "source": {
                        "countryCode": payload.get("source", {}).get("country_code", None),
                        "name": payload.get("source", {}).get("name", None),
                        "accountNumber": payload.get("source", {}).get("account_number", None)
                    }
                })

                destinations = payload.get("destinations", [])
                if len(destinations) > 0:
                    destination = destinations[0]

                    data.update({
                        "destination": {
                            "type": "bank",
                            "countryCode": destination.get("country_code", None),
                            "name": destination.get("name", None),
                            "mobileNumber": destination.get("mobile_number", None),
                            "accountNumber": destination.get("account_number", None),
                            "bankCode": payload.get("transfer", {}).get("bank_code", None),
                        }
                    })

                    data.update({
                        "transfer": {
                            "type": "PesaLink",
                            "amount": f'{destination.get("amount",None)}',
                            "currencyCode": payload.get("transfer", {}).get("currency_code", None),
                            "reference": payload.get("transfer", {}).get("reference", None),
                            "date": payload.get("transfer", {}).get("date", None),
                            "description": payload.get("transfer", {}).get("description", ""),
                        }
                    })
            # If bank_id is NCBA
            elif super().get_bank_id() == super().NCBA:

                destinations = payload.get("destinations", [])
                if len(destinations) > 0:
                    destination = destinations[0]

                    date = payload.get("transfer", {}).get("date", None)
                    if date is not None:
                        date = date.split("-")
                        if len(date) > 0:
                            date = f'{date[0]}{date[1]}{date[2]}'

                    data.update({
                        "BankCode": payload.get("transfer", {}).get("bank_code", None),
                        "BankSwiftCode": payload.get("transfer", {}).get("bank_swift_code", None),
                        "BranchCode": payload.get("transfer", {}).get("branch_code", None),
                        "BeneficiaryAccountName": destination.get("name", None),
                        "Country": payload.get("transfer", {}).get("country", None),
                        "Reference": f'{get_code(length=14)}',
                        "Currency": payload.get("transfer", {}).get("currency_code", None),
                        "Account": destination.get("account_number", None),
                        "Amount": destination.get("amount", None),
                        "Narration": payload.get("transfer", {}).get("description", None),
                        "Transaction Date": date,
                    })
        elif operation == super().PESALINK_TO_MOBILE:

            # If bank_id is COOP
            if super().get_bank_id() == super().COOP:
                data.update({
                    "MessageReference": f'{get_code(length=14)}'
                })
                data.update({
                    "CallBackUrl": payload.get("transfer", {}).get("callback_url", "")
                })
                data.update({
                    "Source": {
                        "AccountNumber": payload.get("source", {}).get("account_number", None),
                        "Amount": payload.get("source", {}).get("amount", None),
                        "TransactionCurrency": payload.get("transfer", {}).get("currency_code", None),
                        "Narration": payload.get("transfer", {}).get("description", "")
                    }
                })

                destinations = payload.get("destinations", [])

                for i in range(len(destinations)):
                    if i == 0:
                        data.update({
                            "Destinations": []
                        })

                    data["Destinations"].append(
                        {
                            "ReferenceNumber": payload.get("transfer", {}).get("reference", None),
                            "PhoneNumber": destinations[i].get("mobile_number", None),
                            "Amount": destinations[i].get("amount", None),
                            "TransactionCurrency": payload.get("transfer", {}).get("currency_code", None),
                            "Narration": payload.get("transfer", {}).get("description", "")
                        }
                    )
            # If bank_id is EQUITY
            elif super().get_bank_id() == super().EQUITY:
                data.update({
                    "source": {
                        "countryCode": payload.get("source", {}).get("country_code", None),
                        "name": payload.get("source", {}).get("name", None),
                        "accountNumber": payload.get("source", {}).get("account_number", None)
                    }
                })

                destinations = payload.get("destinations", [])
                if len(destinations) > 0:
                    destination = destinations[0]

                    data.update({
                        "destination": {
                            "type": "mobile",
                            "countryCode": destination.get("country_code", None),
                            "name": destination.get("name", None),
                            "mobileNumber": destination.get("mobile_number", None),
                            "bankCode": payload.get("transfer", {}).get("bank_code", None),
                        }
                    })

                    data.update({
                        "transfer": {
                            "type": "PesaLink",
                            "amount": f'{destination.get("amount",None)}',
                            "currencyCode": payload.get("transfer", {}).get("currency_code", None),
                            "reference": payload.get("transfer", {}).get("reference", None),
                            "date": payload.get("transfer", {}).get("date", None),
                            "description": payload.get("transfer", {}).get("description", ""),
                        }
                    })
            # If bank_id is NCBA
            elif super().get_bank_id() == super().NCBA:
                pass
        elif operation == super().TRANSACTION_STATUS:

            # If bank_id is COOP
            if super().get_bank_id() == super().COOP:
                data.update({
                    "MessageReference": payload.get("reference", None)
                })
            # If bank_id is EQUITY
            elif super().get_bank_id() == super().EQUITY:
                data.update({
                    "reference": payload.get("reference", None)
                })
            # If bank_id is NCBA
            if super().get_bank_id() == super().NCBA:
                data.update({
                    "reference_number": payload.get("reference", None),
                    "country": payload.get("country", None)
                })
        elif operation == super().INITIATE_PAYMENT:

            if super().get_bank_id() in super().THIRD_PARTY_BANKING.keys():
                destinations = payload.get("destinations", [])
                if len(destinations) > 0:
                    destination = destinations[0]

                    data = {
                        "secret": payload.get("transfer", {}).get("secret", ""),
                        "clientId": payload.get("transfer", {}).get("client_id", ""),
                        "receiptName": destination.get("name", ""),
                        "targetAccount": destination.get("account_number", ""),
                        "sortCode": payload.get("transfer", {}).get("sort_code", ""),
                        "currency": payload.get("transfer", {}).get("currency_code", ""),
                        "value": destination.get("amount", 0),
                        "referenceID": payload.get("transfer", {}).get("reference", ""),
                        # "referenceMetaData": "string",
                        "type":  payload.get("type", {}).get("sort_code", ""),
                        "description": payload.get("transfer", {}).get("description", ""),
                        # "nickname": "string",
                        "country": payload.get("transfer", {}).get("country", ""),
                        "branchAddress": payload.get("transfer", {}).get("branch_address", ""),
                        "branchName": payload.get("transfer", {}).get("branch_name", ""),
                        "swiftCode": payload.get("transfer", {}).get("bank_swift_code", ""),
                        "iban": payload.get("transfer", {}).get("iban", ""),
                        "bankName": payload.get("transfer", {}).get("bank_name", ""),
                    }

        data.update(payload.get("additional_properties", {}))

        return data

    def response(self):

        data = {}

        response_data = super().response()

        if super().get_bank_id() == super().COOP:

            data["message"] = response_data.get("MessageDescription", "")
            data["code"] = int(response_data.get("MessageCode", -1111111))

            if 'MessageDescription' in response_data.keys():
                if response_data.get("MessageDescription", "") == "Full Success":
                    data["message"] = "success"
                else:
                    data["message"] = response_data.get(
                        "MessageDescription", "")

            if 'MessageCode' in response_data.keys():
                data["code"] = int(response_data.get("MessageCode", -1111111))

            if 'Destinations' in response_data.keys():
                if response_data.get("Destinations", [{}]) is not None:

                    data["transaction_id"] = response_data.get(
                        "Destinations", [{}])[0].get("TransactionID", "")

            if 'MessageDateTime' in response_data.keys():
                data["date"] = response_data.get(
                    "MessageDateTime", date.today().strftime('%d/%m/%y %H:%M:%S'))

            if 'messageDescription' in response_data.keys():
                if response_data.get("messageDescription", "") == "Full Success":
                    data["message"] = "success"
                else:
                    data["message"] = response_data.get(
                        "messageDescription", "")

            if 'messageCode' in response_data.keys():
                data["code"] = response_data.get("messageCode", -1111111)

            if 'destination' in response_data.keys():
                if response_data.get("destination", {}) is not None:
                    data["transaction_id"] = response_data.get(
                        "destination", {}).get("transactionID", "")

            if 'messageDateTime' in response_data.keys():
                data["date"] = response_data.get(
                    "messageDateTime", date.today().strftime('%d/%m/%y %H:%M:%S'))

        elif super().get_bank_id() == super().EQUITY:
            data["message"] = response_data.get("message", "")
            data["code"] = response_data.get("code", -1111111)
            if 'mobileMoneyInfo' in response_data.keys():
                data["transaction_id"] = response_data.get(
                    "mobileMoneyInfo", {}).get("ThirdPartyTranID", "")
            else:
                data["transaction_id"] = response_data.get("data", {}).get("transactionId", "")
            data["date"] = response_data.get(
                "date", date.today().strftime('%d/%m/%y %H:%M:%S'))

        if bool(data):
            return data

        return super().response()

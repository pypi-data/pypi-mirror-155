class Operations(object):

    # These are the billing integrations
    # Each with a unique ID
    GLOBAL = 0
    COOP = GLOBAL + 1
    EQUITY = COOP + 1
    NCBA = EQUITY + 1
    DAPI = NCBA + 1
    MONO = DAPI + 1
    PLAID = EQUITY + 1
    STITCH = PLAID + 1

    # These are the operations to be performed in Billing Identity
    # Each with a unique incremental ID

    # Returns Sample Data
    SAMPLE_DATA = -1
    BANKS = SAMPLE_DATA + 1
    BALANCE = BANKS + 1
    MINI_STATEMENT = BALANCE + 1
    FULL_STATEMENT = MINI_STATEMENT + 1
    ACCOUNT_VALIDATION = FULL_STATEMENT + 1
    ACCOUNT_TRANSACTIONS = ACCOUNT_VALIDATION + 1
    IFT = ACCOUNT_TRANSACTIONS + 1
    TRANSACTION_STATUS = IFT + 1
    MOBILE_WALLET = TRANSACTION_STATUS + 1
    PESALINK_TO_BANK = MOBILE_WALLET + 1
    PESALINK_TO_MOBILE = PESALINK_TO_BANK + 1
    RTGS = PESALINK_TO_MOBILE + 1
    SWIFT = RTGS + 1
    EFT = SWIFT + 1
    INITIATE_PAYMENT = EFT + 1
    FOREX_RATE = INITIATE_PAYMENT + 1
    COUNTRIES = FOREX_RATE + 1

    # All end points are placed in the BILLERS_CONF
    # This is to allow easy standardization of the base url, endpoint and operations
    # When calling the APIs, in this case this is done in the read function
    BANKS_CONF = {
        GLOBAL: {
            "url": "https://dev.bankingservices.nashglobal.co",
            "read": {
                "endpoint": f"api/banks",
                "operations": {
                    SAMPLE_DATA: ("sample_payload", "GET"),
                    BANKS: ("banks", "GET"),
                    COUNTRIES: ("countries", "GET"),
                }
            }

        },
        EQUITY: {
            "url": "https://dev.bankingservices.nashglobal.co",
            "accounts": {
                "endpoint": f"api/banks/accounts/{EQUITY}",
                "operations": {
                    BALANCE: ("get_balance", "POST"),
                    MINI_STATEMENT: ("get_mini_statement", "POST"),
                    ACCOUNT_VALIDATION: ("get_validation", "POST"),
                    FULL_STATEMENT: ("get_full_statement", "POST"),
                    FOREX_RATE: ("get_forex_rates", "POST"),
                }
            },
            "payment": {
                "endpoint": f"api/banks/payment/{EQUITY}",
                "operations": {
                    IFT: ("ift", "POST"),
                    MOBILE_WALLET: ("mobile_wallet", "POST"),
                    RTGS: ("rtgs", "POST"),
                    SWIFT: ("swift", "POST"),
                    EFT: ("eft", "POST"),
                    PESALINK_TO_BANK: ("pesalink/bank", "POST"),
                    PESALINK_TO_MOBILE: ("pesalink/mobile", "POST"),
                    TRANSACTION_STATUS: ("get_transaction_status", "POST"),
                }
            }

        },
        COOP: {
            "url": "https://dev.bankingservices.nashglobal.co",
            "accounts": {
                "endpoint": f"api/banks/accounts/{COOP}",
                "operations": {
                    BALANCE: ("get_balance", "POST"),
                    MINI_STATEMENT: ("get_mini_statement", "POST"),
                    ACCOUNT_VALIDATION: ("get_validation", "POST"),
                    FULL_STATEMENT: ("get_full_statement", "POST"),
                    ACCOUNT_TRANSACTIONS: ("get_transactions", "POST")
                }
            },
            "payment": {
                "endpoint": f"api/banks/payment/{COOP}",
                "operations": {
                    IFT: ("ift", "POST"),
                    MOBILE_WALLET: ("mobile_wallet", "POST"),
                    PESALINK_TO_BANK: ("pesalink/bank", "POST"),
                    PESALINK_TO_MOBILE: ("pesalink/mobile", "POST"),
                    TRANSACTION_STATUS: ("get_transaction_status", "POST"),
                }
            }

        },
        NCBA: {
            "url": "https://dev.bankingservices.nashglobal.co",
            "accounts": {},
            "payment": {
                "endpoint": f"api/banks/payment/{NCBA}",
                "operations": {
                    IFT: ("ift", "POST"),
                    MOBILE_WALLET: ("mobile_wallet", "POST"),
                    RTGS: ("rtgs", "POST"),
                    EFT: ("eft", "POST"),
                    PESALINK_TO_BANK: ("pesalink/bank", "POST"),
                    TRANSACTION_STATUS: ("get_transaction_status", "POST"),
                }
            }
        },
        DAPI: {
            "url": "http://dev.3p.bankingservices.nashglobal.co",
            "accounts": {
                ACCOUNT_TRANSACTIONS: ("get_transactions", "POST")
            },
            "payment": {
                "endpoint": f"v1/Dapi",
                "operations": {
                    INITIATE_PAYMENT: ("initiate_payment", "POST"),
                }
            }
        },
        MONO: {
            "url": "http://dev.3p.bankingservices.nashglobal.co",
            "accounts": {
                ACCOUNT_TRANSACTIONS: ("get_transactions", "POST")
            },
            "payment": {
                "endpoint": f"v1/Mono",
                "operations": {
                    INITIATE_PAYMENT: ("initiate_payment", "POST"),
                }
            }
        },
        PLAID: {
            "url": "http://dev.3p.bankingservices.nashglobal.co",
            "accounts": {
                ACCOUNT_TRANSACTIONS: ("get_transactions", "POST")
            },
            "payment": {
                "endpoint": f"v1/Plaid",
                "operations": {
                    INITIATE_PAYMENT: ("initiate_payment", "POST"),
                }
            }
        },
        STITCH: {
            "url": "http://dev.3p.bankingservices.nashglobal.co",
            "accounts": {
                ACCOUNT_TRANSACTIONS: ("get_transactions", "POST")
            },
            "payment": {
                "endpoint": f"v1/Stitch",
                "operations": {
                    INITIATE_PAYMENT: ("initiate_payment", "POST"),
                }
            }
        },
    }

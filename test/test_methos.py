import asyncio

from core.unconfirmed_transations import (
    find_unconfirmed_transactions,
    connect_mysql,
    get_transaction
)
from core.utils import log_exception


def test_connect_mysql():
    try:
        print("------------------ Testing MYSQL Connection -------------------")
        db = asyncio.run(connect_mysql())
        if db:
            print(f"MYSQL Connection Successful")
        else:
            print("MYSQL Connection Unsuccessful")
        print("--------------------- Tested Successfully ---------------------")
    except Exception as e:
        log_exception(e, "Error while testing connect_mysql")
        print("--------------------- Test Unsuccessfully ---------------------")


def test_find_unconfirmed_transaction():
    try:
        print("--------------- Testing BlockCypher API Calls -----------------")
        return_check = asyncio.run(find_unconfirmed_transactions())
        if return_check:
            print(f"BlockCypher API Calls Successful")
        else:
            print("BlockCypher API Calls Unsuccessful")
        print("--------------------- Tested Successfully ---------------------")
    except Exception as e:
        log_exception(e, "Error while testing find_unconfirmed_transaction")
        print("--------------------- Test Unsuccessfully ---------------------")


def test_get_transaction():
    try:
        print("------------- Testing MYSQL Transaction Retrival --------------")
        records = asyncio.run(get_transaction(limit=10))
        if records and len(records) <= 10:
            print(f"MYSQL Transaction Retrival Successful")
        else:
            print("MYSQL Transaction Retrival Unsuccessful")
        print("--------------------- Tested Successfully ---------------------")
    except Exception as e:
        log_exception(e, "Error while testing get_transaction")
        print("--------------------- Test Unsuccessfully ---------------------")


if __name__ == "__main__":
    test_connect_mysql()
    test_find_unconfirmed_transaction()
    test_get_transaction()


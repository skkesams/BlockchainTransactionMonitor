from blockcypher import get_broadcast_transactions
import json
import os
import pymysql
from time import sleep

from core.utils import log_exception, read_yaml


def serialize(data):
    try:
        s_data = json.dumps(data)
        return s_data
    except Exception as e:
        log_exception(e, "Error while serializing the data")
    return data


async def connect_mysql():
    """
    This method will establish the connection to the MYSQL database running on cloud(aiven)
    :return: db type - database object
    """
    try:
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        mysl_conf = read_yaml(__location__ + "/config/mysql_creds.yaml")

        db = pymysql.connect(
                host=mysl_conf.get("host", None),
                port=mysl_conf.get("port", None),
                user=mysl_conf.get("user", None),
                password=mysl_conf.get("password", None),
                database=mysl_conf.get("database", None),
                cursorclass=pymysql.cursors.DictCursor
            )
        return db
    except Exception as e:
        log_exception(e, "Error in conncting to the MySql Server")
    return None


async def get_transaction(limit=10):
    """
    This method will executes select command and fetches the transactions from the database.

    :param limit: int - default value is 10
    :return: list - list of transactions
    """
    try:
        db = await connect_mysql()
        with db.cursor() as cursor:
            sql = f"SELECT * FROM unconfirmed_transactions order by date DESC LIMIT {limit}"
            cursor.execute(sql)
            transactions = cursor.fetchall()
        db.close()
        return transactions
    except Exception as e:
        log_exception(e, "Exception in selecting the tx from database")
    return []


async def store_transaction(tx):
    """
    This method will execute the insert statement to store the transaction into the table.

    :param tx: dict
    """
    try:
        db = await connect_mysql()
        with db.cursor() as cursor:
            sql = "INSERT INTO unconfirmed_transactions (hash, total, fees, inputs, outputs) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (tx['hash'], tx['total'], tx['fees'],
                                 serialize((tx['inputs'])), serialize(tx['outputs'])))
        db.commit()
        db.close()
    except pymysql.IntegrityError as e:
        if e.args[0] == 1062:
            log_exception(e, "Record already exists in the Database")

    except Exception as e:
        log_exception(e, "Exception in inserting the tx into database")


async def find_unconfirmed_transactions(storage: bool = False):
    """
    This method will call the Blockcypher API with a limit of 100 till transactions are repeated, in parallel it will
    keep track of the transaction with maximum amount and finally calls "store_transaction" the transactions.

    :param storage: bool value - True to store the record into MYSQL table
    :return: bool value - True if successfully executed else False
    """
    try:
        completed = False
        start = True
        start_hash = None
        max_transaction = None
        max_value = 0
        hash_set = set()

        while not completed:
            transactions_block = []
            try:
                transactions_block = get_broadcast_transactions(limit=100)
            except Exception as e:
                log_exception(e, "Exception while calling the Blockcypher API")
                completed = True

            if len(transactions_block) > 0:
                if start:
                    max_transaction = transactions_block.pop(0)
                    start_hash = max_transaction.get("hash", None)
                    max_value = max_transaction.get("total", 0)
                    hash_set.add(start_hash)
                    start = False

                for transaction in transactions_block:
                    cur_hash = transaction.get("hash", None)
                    if start_hash != cur_hash or cur_hash not in hash_set:
                        hash_set.add(start_hash)
                        total_val = transaction.get("total", 0)
                        if total_val > max_value:
                            max_transaction = transaction
                            max_value = total_val
                    else:
                        completed = True
                        break

        if max_transaction and storage:
            await store_transaction(max_transaction)
        return True
    except Exception as e:
        log_exception(e, "Exception while processing the transactions")
        return False


async def start_job():
    while True:
        try:
            print("Started Blockchain transaction fetch")
            await find_unconfirmed_transactions(storage=True)
            print("Completed the Blockchain transaction fetch")
            sleep(300)
        except Exception as e:
            log_exception(e, "Error while running the start-job")

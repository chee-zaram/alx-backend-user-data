#!/usr/bin/env python3
"""
This is the `filtered_logger` module.
It contains the function `filter_datum` which obfuscates certain fields
in a log data.
"""

from typing import List, Dict
import re
import logging
import csv
import os
import mysql.connector


# PII_FIELDS is a list of the top 5 fields in `user_data.csv` that qualify as
# personally identifiable information (PII).
PII_FIELDS = ("name", "email", "phone", "ssn", "password")
regex = {
    "pattern": lambda f, s: r"(?P<field>{})=[^{}]+".format("|".join(f), s),
    "repl": lambda r: r"\g<field>={}".format(r),
}


def filter_datum(
        fields: List[str], redaction: str,
        message: str, separator: str) -> str:
    """This function obfuscates certain fields in a `message`.
    """
    pattern, repl = regex["pattern"], regex["repl"]
    return re.sub(pattern(fields, separator), repl(redaction), message)


def get_logger() -> logging.Logger:
    """
    `get_logger` creates a logger name `user_data`. It logs up to logging.INFO.
    It does not propagate messages to other loggers.
    It has `StreamHandler` which logs to the console, and `RedactingFormatter`
    as formatter.

    Returns:
        logging.Logger: A logger instance.
    """
    name = "user_data"
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    `get_db` returns a connector to the database `my_db`.
    It uses the following environment variables:
        PERSONAL_DATA_DB_USERNAME: default `root`
        PERSONAL_DATA_DB_PASSWORD: default empty string
        PERSONAL_DATA_DB_HOST: default `localhost`
        PERSONAL_DATA_DB_NAME: default `my_db`

    You can use the following command to get some data:
        $ cat main.sql | mysql -uroot -p

    Returns:
        mysql.connector.connection.MySQLConnection: A database connector.
    """
    db_user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_pwd = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME", "my_db")

    return mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_pwd,
        database=db_name,
    )


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        format formats the record according to the format set for the class,
        and filters the given fields for the instance in the record message
        using the `filter_datum` function.

        Returns:
            str: The log message as with necessary fields obfuscated.
        """
        if not isinstance(record, logging.LogRecord):
            raise TypeError("record must be an instance of logging.LogRecord")
        msg = super(RedactingFormatter, self).format(record)
        return filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)


def filter_datum_test() -> None:
    fields = ["password", "date_of_birth"]
    messages = get_data_from_csv()
    for m in messages:
        msg = [f"{k}={v}" for k, v in m.items()]
        print(filter_datum(fields, 'xxx', ";".join(msg), ';'))


def get_logger_test() -> None:
    print(get_logger.__annotations__.get('return'))
    print("PII_FIELDS: {}".format(len(PII_FIELDS)))
    logger = get_logger()

    data = get_data_from_csv()
    for datum in data:
        msg = [f"{k}={v}" for k, v in datum.items()]
        logger.info(";".join(msg))


def redacting_formatter_test() -> None:
    messages = get_data_from_csv()
    formatter = RedactingFormatter(fields=("email", "ssn", "password"))
    for m in messages:
        m = [f"{k}={v}" for k, v in m.items()]
        print(formatter.format(logging.LogRecord("my_logger",
              logging.INFO, None, None, ";".join(m), None, None)))


def get_db_test() -> None:
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM users;")
    for row in cursor:
        print(row[0])
    cursor.close()
    db.close()


def get_data_from_csv() -> List[Dict]:
    data = []
    csv_file = "user_data.csv"
    if not os.path.exists(csv_file) or not os.path.isfile(csv_file):
        return data

    with open("user_data.csv", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            data.append(row)

    return data


if __name__ == "__main__":
    filter_datum_test()
    get_logger_test()
    redacting_formatter_test()
    get_db_test()

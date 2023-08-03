#!/usr/bin/env python3
"""
This is the `filtered_logger` module.
It contains the function `filter_datum` which obfuscates certain fields
in a log data.
"""

from typing import List
import re
import logging
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
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME", "")
    db_user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_pwd = os.getenv("PERSONAL_DATA_DB_PASSWORD", "my_db")

    try:
        connector = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_pwd,
            database=db_name,
        )
    except mysql.connector.Error:
        return None

    return connector


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

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


def test_filter_datum() -> None:
    fields = ["password", "date_of_birth"]
    messages = get_data_from_csv()
    for m in messages:
        msg = [f"{k}={v}" for k, v in m.items()]
        print(filter_datum(fields, 'xxx', ";".join(msg), ';'))


def test_get_logger() -> None:
    print(get_logger.__annotations__.get('return'))
    print("PII_FIELDS: {}".format(len(PII_FIELDS)))
    logger = get_logger()

    data = get_data_from_csv()
    for datum in data:
        msg = [f"{k}={v}" for k, v in datum.items()]
        logger.info(";".join(msg))


def test_redacting_formatter() -> None:
    messages = get_data_from_csv()
    formatter = RedactingFormatter(fields=("email", "ssn", "password"))
    for m in messages:
        m = [f"{k}={v}" for k, v in m.items()]
        print(formatter.format(logging.LogRecord("my_logger",
              logging.INFO, None, None, ";".join(m), None, None)))


def get_data_from_csv() -> List[Dict]:
    data = []
    with open("user_data.csv", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            data.append(row)

    return data


if __name__ == "__main__":
    test_filter_datum()
    test_get_logger()
    test_redacting_formatter()

#!/usr/bin/env python3
"""
This is the `filtered_logger` module.
It contains the function `filter_datum` which obfuscates certain fields
in a log data.
"""

from typing import List
import re
import logging


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


if __name__ == "__main__":
    fields = ["password", "date_of_birth"]
    messages = [
        "name=egg;email=eggmin@eggsample.com;password=eggcellent;" +
        "date_of_birth=12/12/1986;",
        "name=bob;email=bob@dylan.com;password=bobbycool;" +
        "date_of_birth=03/04/1993;",
    ]

    # Test filter_datum
    for message in messages:
        print(filter_datum(fields, 'xxx', message, ';'))

    # Test RedactingFormatter
    formatter = RedactingFormatter(fields=("email", "ssn", "password"))
    for m in messages:
        print(formatter.format(logging.LogRecord("my_logger",
              logging.INFO, None, None, message, None, None)))

    # Test get_logger
    print(get_logger.__annotations__.get('return'))
    print("PII_FIELDS: {}".format(len(PII_FIELDS)))
    logger = get_logger()
    logger.info("This is a name=cheezaram;password=abc; Author of the code.")

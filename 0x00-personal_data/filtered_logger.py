#!/usr/bin/env python3
"""
This is the `filtered_logger` module.
It contains the function `filter_datum` which obfuscates certain fields
in a log data.
"""

from typing import List
import re

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


if __name__ == "__main__":
    fields = ["password", "date_of_birth"]
    messages = [
        "name=egg;email=eggmin@eggsample.com;password=eggcellent;" +
        "date_of_birth=12/12/1986;",
        "name=bob;email=bob@dylan.com;password=bobbycool;" +
        "date_of_birth=03/04/1993;",
    ]

    for message in messages:
        print(filter_datum(fields, 'xxx', message, ';'))

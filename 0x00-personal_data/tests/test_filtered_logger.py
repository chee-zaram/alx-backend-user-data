#!/usr/bin/env python3
import unittest
from unittest.mock import patch
from io import StringIO
import logging
import os
import csv
from typing import List, Dict
import filtered_logger as fl
from filtered_logger import RedactingFormatter


class TestFilteredLogger(unittest.TestCase):
    def test_filter_datum(self) -> None:
        fields = ["password", "date_of_birth"]
        messages = self.get_data_from_csv()
        for m in messages:
            m = [f"{k}={v}" for k, v in m.items()]
            msg = fl.filter_datum(fields, 'xxx', ";".join(m), ';')
            if "password" in msg:
                self.assertIn("password=xxx", msg)
            if "date_of_birth" in msg:
                self.assertIn("date_of_birth=xxx", msg)

    def test_get_logger(self) -> None:
        reval = str(fl.get_logger.__annotations__.get('return'))
        self.assertTrue(reval == "<class 'logging.Logger'>")
        logger = fl.get_logger()
        self.assertTrue(isinstance(logger, logging.Logger))

        data = self.get_data_from_csv()
        expected_outputs = []

        # Construct the expected log messages
        for datum in data:
            msg = [f"{k}={v}" for k, v in datum.items()]
            expected_outputs.append(";".join(msg))

        # Use the 'patch' decorator to trap stdout
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            # logging module caches the handlers when the logger is created,
            # and it won't use the new StreamHandler that we created with the
            # RedactingFormatter. As a result, the log messages are not
            # captured in the mock_stdout.
            # To fix this, we need to explicitly set the handlers for the
            # logger to the new StreamHandler with the RedactingFormatter.
            stream_handler = logging.StreamHandler(mock_stdout)
            stream_handler.setFormatter(fl.RedactingFormatter(fl.PII_FIELDS))
            logger.addHandler(stream_handler)
            for msg in expected_outputs:
                logger.info(msg)
                exp_log = mock_stdout.getvalue().strip()
                for f in fl.PII_FIELDS:
                    if f not in msg:
                        continue
                    self.assertTrue("{0}={1}".format(
                        f, RedactingFormatter.REDACTION) in exp_log)
                mock_stdout.truncate(0)

    def test_redacting_formatter(self) -> None:
        messages = self.get_data_from_csv()
        fields = ("email", "ssn", "password")
        formatter = RedactingFormatter(fields=fields)

        for m in messages:
            m = [f"{k}={v}" for k, v in m.items()]
            msg = str(formatter.format(logging.LogRecord(
                "my_logger",
                logging.INFO,
                None, None,
                ";".join(m), None, None)))
            for f in fields:
                if f not in msg:
                    continue
                self.assertTrue("{}={}".format(f, formatter.REDACTION) in msg)

    def test_get_db(self) -> None:
        db = fl.get_db()
        if not db:
            return
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM users;")
        for row in cursor:
            self.assertTrue(len(row[0]) > 0)
        cursor.close()
        db.close()

    def get_data_from_csv(self) -> List[Dict]:
        data = []
        data_fn = "user_data.csv"
        path_comp = __file__.split(os.path.sep)
        file_path = os.path.join(os.path.sep.join(path_comp[:-1]), data_fn)
        if not os.path.exists(file_path):
            return data
        if not os.path.isfile(file_path):
            return data

        with open(file_path) as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                data.append(row)

        return data


if __name__ == "__main__":
    unittest.main()

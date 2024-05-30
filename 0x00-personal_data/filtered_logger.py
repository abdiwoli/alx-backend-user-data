#!/usr/bin/env python3
""" filter pii """
import re
import mysql.connector
from typing import List, Tuple
import logging
import os


PII_FIELDS: Tuple[str, ...] = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ format function """
        message = super(RedactingFormatter, self).format(record)
        return filter_datum(self.fields, self.REDACTION,
                            message, self.SEPARATOR)


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """ filter data """
    for field in fields:
        pattern = f'{field}=.*?(?={separator}|$)'
        message = re.sub(pattern, f'{field}={redaction}', message)
    return message


def get_logger() -> logging.Logger:
    """ logger function """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(list(PII_FIELDS))
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ secure connection to db """
    usr = os.environ.get('PERSONAL_DATA_DB_USERNAME', "root")
    psw = os.environ.get('PERSONAL_DATA_DB_PASSWORD', "")
    host = os.environ.get('PERSONAL_DATA_DB_HOST', "localhost")
    db = db_name = os.environ.get("PERSONAL_DATA_DB_NAME", "my_db")

    return mysql.connector.connection.MySQLConnection(user=usr,
                                                      password=psw,
                                                      host=host,
                                                      database=db)

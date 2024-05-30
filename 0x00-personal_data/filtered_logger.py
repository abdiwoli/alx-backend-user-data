#!/usr/bin/env python3
""" filter pii """
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """ filter data """
    for field in fields:
        pattern = f'{field}=.*?(?={separator}|$)'
        message = re.sub(pattern, f'{field}={redaction}', message)
    return message

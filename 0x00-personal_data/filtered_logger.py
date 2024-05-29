#!/usr/bin/env python3
from typing import List
import re


def filter_datum(fields: List[str], redaction: str, message: str, sep: str):
    """ filter data """
    for field in fields:
        pattern = rf"({field}=)([^ {sep}]*)"
        message = re.sub(pattern, rf"\1{redaction}", message)
    return message

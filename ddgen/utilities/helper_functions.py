import uuid
from datetime import date, datetime

import numpy as np


def sample_from_array(array, size, replace) -> np.ndarray:
    return np.random.choice(array, size, replace)


def generate_uuid_as_str():
    return str(uuid.uuid4())


def generate_int_primary_key():
    key = 0
    while True:
        key += 1
        yield key


def get_numeric_value(value, is_int: bool) -> int | float:
    if is_int:
        return int(value)
    return value


def _try_time_parse(date_input, formats):
    for fmt in formats:
        try:
            return datetime.strptime(date_input, fmt)
        except ValueError:
            continue
    return None


def convert_to_datetime(date_input):
    if isinstance(date_input, datetime):
        return date_input

    datetime_formats = [
        '%Y-%m-%dT%H:%M:%S%z',
        '%Y-%m-%d %H:%M:%S',
        '%Y/%m/%d %H:%M:%S',
        '%d-%m-%Y %H:%M:%S',
        '%m/%d/%Y %H:%M:%S',
    ]

    datetime_obj = _try_time_parse(date_input, datetime_formats)
    if datetime_obj:
        return datetime_obj

    raise ValueError('No valid datetime format found for: ' + str(date_input))


def convert_to_date(date_input):
    if isinstance(date_input, date):
        return date_input

    date_formats = ['%Y-%m-%d', '%d-%m-%Y', '%m/%d/%Y']

    date_obj = _try_time_parse(date_input, date_formats)
    if date_obj:
        return date_obj.date()

    raise ValueError('No valid date format found for: ' + str(date_input))

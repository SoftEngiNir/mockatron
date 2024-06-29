import numpy as np
import uuid


def sample_from_array(array, size, replace) -> np.ndarray:
    return np.random.choice(array, size, replace)


def generate_uuid_as_str():
    return str(uuid.uuid4())

def generate_int_primary_key():
    key = 0
    while True:
        key += 1
        yield key




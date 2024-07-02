from __future__ import annotations

import random
from typing import Callable
from typing import Final

import numpy as np

from ddgen.engines.base import ArrayEngine
from ddgen.engines.base import Engine
from ddgen.enums import RelationshipType
from ddgen.utilities.helper_functions import sample_from_array

RELATIONSHIP_HANDLERS: Final[dict[RelationshipType, Callable]] = {
    RelationshipType.one_to_one: lambda from_data, n_rows: sample_from_array(
        from_data,
        n_rows,
        False,
    ),
    RelationshipType.one_to_many: lambda from_data, n_rows: sample_from_array(
        from_data,
        n_rows,
        True,
    ),
}


def add_nones(array: np.ndarray, percentage: int):
    array = array.astype('object')
    per_size = int(array.size * percentage / 100)
    indecies = random.sample(range(array.size), per_size)
    np.put(array, indecies, np.array(None))
    return array


def data_from_engine(engine: Engine, n_rows: int) -> np.ndarray:
    a_eng = ArrayEngine(engine, n_rows)  # type: Engine
    return np.array(a_eng.sample())


def fk_data(from_data: np.ndarray, n_rows: int, r_type: RelationshipType):
    return RELATIONSHIP_HANDLERS[r_type](from_data, n_rows)

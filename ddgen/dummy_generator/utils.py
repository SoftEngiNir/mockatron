from __future__ import annotations

import random
from datetime import date
from typing import TYPE_CHECKING, Final

import numpy as np

from ddgen.engines.base import ArrayEngine, Engine
from ddgen.enums import DataType, RelationshipType
from ddgen.utilities.helper_functions import sample_from_array

if TYPE_CHECKING:
    from ddgen.schema.column import RelatedColumn


def add_nones(array: np.ndarray, percentage: int) -> np.ndarray:
    array = array.astype('object')
    per_size = int(array.size * percentage / 100)
    indecies = random.sample(range(array.size), per_size)
    np.put(array, indecies, np.array(None))
    return array


def data_from_engine(engine: Engine, n_rows: int) -> np.ndarray:
    a_eng = ArrayEngine(engine, n_rows)  # type: Engine
    return np.array(a_eng.sample())


def fk_data(from_data: np.ndarray, n_rows: int, rtype: RelationshipType) -> np.ndarray:
    config = RELATIONSHIP_CONFIGS[rtype]
    func, kwargs = config['func'], config['kwargs']
    return func(from_data, n_rows, **kwargs)


def date_delta(
    source_dates: np.ndarray,
    source_pk_data: np.ndarray,
    target_fk_data: np.ndarray,
    before: bool,
) -> np.ndarray:
    max_days = (np.datetime64(date.today()) - source_dates).astype(int)
    sort = np.argsort(source_pk_data)
    rank = np.searchsorted(source_pk_data, target_fk_data, sorter=sort)
    key_indices = sort[rank]
    base_array = source_dates[key_indices]
    max_days_for_indices = np.maximum(1, max_days[key_indices])
    deltas_array = np.random.randint(1, max_days_for_indices + 1).astype(
        'timedelta64[D]',
    )
    if before:
        return base_array - deltas_array
    return base_array + deltas_array


def related_data(column: RelatedColumn, n_rows: int) -> np.ndarray:
    source_pk_data = column.source_pk.data if column.source_pk else None
    source_data = column.source_col.data
    if source_pk_data is not None and source_pk_data.any() and source_data.any():
        np_type = NUMPY_DTYPE.get(column.source_col.dtype)
        source_data = source_data.astype(np_type)
        target_fk_data = column.get_fk_col().data
        config = RELATIONSHIP_CONFIGS[column.rtype]
        func, kwargs = config['func'], config['kwargs']
        return func(source_data, source_pk_data, target_fk_data, **kwargs)
    return np.array([None] * n_rows)


RELATIONSHIP_CONFIGS: Final[dict[RelationshipType, dict]] = {
    RelationshipType.one_to_one: {
        'func': sample_from_array,
        'kwargs': {'replace': False},
    },
    RelationshipType.one_to_many: {
        'func': sample_from_array,
        'kwargs': {'replace': True},
    },
    RelationshipType.after: {'func': date_delta, 'kwargs': {'before': False}},
    RelationshipType.before: {'func': date_delta, 'kwargs': {'before': True}},
}


NUMPY_DTYPE: Final[dict[DataType, str]] = {
    DataType._date: 'datetime64[D]',
    DataType._datetime: 'datetime64[D]',
}

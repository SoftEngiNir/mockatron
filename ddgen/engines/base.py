from __future__ import annotations

from random import Random
from typing import Generic
from typing import TypeVar

import numpy as np
from faker import Faker

T = TypeVar('T')


class Engine(Generic[T]):
    def sample(self):
        raise NotImplementedError('Not implemented')


class RandEngine(Engine[T]):
    def __init__(self) -> None:
        self._engine = Random()


class FakerEngine(Engine[T]):
    def __init__(self) -> None:
        self._engine = Faker()


class NumpyEngine(Engine[T]):
    def __init__(self) -> None:
        self._engine = np.random


class ArrayEngine(Engine[list[T]]):
    def __init__(self, engine: Engine, n_rows=1) -> None:
        super().__init__()
        self.engine = engine
        self.n_rows = n_rows

    def sample(self):
        return [self.engine.sample() for _ in range(self.n_rows)]

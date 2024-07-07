from __future__ import annotations

from random import Random
from typing import Generic, TypeVar

import numpy as np
from faker import Faker

T = TypeVar('T')


class Engine(Generic[T]):
    def sample(self):
        raise NotImplementedError('Not implemented')

    def set_seed(self, seed):
        self.seed = seed


class RandEngine(Engine[T]):
    def __init__(self) -> None:
        self._engine = Random()

    def set_seed(self, seed):
        super().set_seed(seed)
        self._engine.seed(self.seed)
        return self


class FakerEngine(Engine[T]):
    def __init__(self) -> None:
        self._engine = Faker()

    def set_seed(self, seed):
        super().set_seed(seed)
        Faker.seed(seed)
        return self


class NumpyEngine(Engine[T]):
    def __init__(self) -> None:
        self._engine = np.random

    def set_seed(self, seed):
        super().set_seed(seed)
        self._engine.seed(self.seed)
        return self


class ArrayEngine(Engine[list[T]]):
    def __init__(self, engine: Engine, n_rows=1) -> None:
        super().__init__()
        self.engine = engine
        self.n_rows = n_rows

    def sample(self):
        return [self.engine.sample() for _ in range(self.n_rows)]

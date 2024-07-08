from __future__ import annotations

from typing import Union

from ddgen.engines.base import NumpyEngine
from ddgen.engines.registry import register_engine
from ddgen.utilities.helper_functions import get_numeric_value


@register_engine
class NumericalNormalDistEngine(NumpyEngine[Union[int, float]]):
    def __init__(self, mean=0, std=1, is_int=False):
        """Returns a normally distributed value"""
        super().__init__()
        self.mean = mean
        self.std = std
        self.is_int = is_int

    def sample(self) -> int | float:
        value = self._engine.normal(self.mean, self.std)
        return get_numeric_value(value, self.is_int)


@register_engine
class NumericalUniformDistEngine(NumpyEngine[Union[int, float]]):
    def __init__(self, low=0, high=1, is_int=False):
        """Returns a uniformaly distributed value"""
        super().__init__()
        self.low = low
        self.high = high
        self.is_int = is_int

    def sample(self) -> int | float:
        value = self._engine.uniform(self.low, self.high)
        return get_numeric_value(value, self.is_int)


@register_engine
class NumericalExponentialDistEngine(NumpyEngine[Union[int, float]]):
    def __init__(self, scale=1.0, is_int=False):
        """Returns an exponential distributed value"""
        super().__init__()
        self.scale = scale
        self.is_int = is_int

    def sample(self) -> int | float:
        value = self._engine.exponential(self.scale)
        return get_numeric_value(value, self.is_int)


@register_engine
class NumericalBinomialDistEngine(NumpyEngine[Union[int, float]]):
    def __init__(self, n=1, p=0.5, is_int=False):
        """Returns a binomialy distributed value"""
        super().__init__()
        self.n = n
        self.p = p
        self.is_int = is_int

    def sample(self) -> int | float:
        value = self._engine.binomial(self.n, self.p)
        return get_numeric_value(value, self.is_int)


@register_engine
class NumericalPoissonDistEngine(NumpyEngine[Union[int, float]]):
    def __init__(self, lam=1.0, is_int=False):
        """Returns a poisson distributed value"""
        super().__init__()
        self.lam = lam
        self.is_int = is_int

    def sample(self) -> int | float:
        value = self._engine.poisson(self.lam)
        return get_numeric_value(value, self.is_int)

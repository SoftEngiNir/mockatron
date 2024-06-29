from ddgen.engines.base import NumpyEngine
from typing import Union

def get_numeric_value(value, is_int: bool) -> Union[int, float]:
        if is_int:
            return int(value)
        return value

class NumericalNormalDistEngine(NumpyEngine[Union[int, float]]):

    def __init__(self, mean=0, std=1, is_int=False):
        """Returns a normally distributed value"""
        super().__init__()
        self.mean = mean
        self.std = std
        self.is_int = is_int

    def sample(self) -> int:
        value = self._engine.normal(self.mean, self.std)
        return get_numeric_value(value, self.is_int)


class NumericalUniformDistEngine(NumpyEngine[Union[int, float]]):

    def __init__(self, low=0, high=1, is_int=False):
        """Returns a uniformaly distributed value"""
        super().__init__()
        self.low = low
        self.high = high
        self.is_int = is_int

    def sample(self) -> int:
        value = self._engine.uniform(self.low, self.high)
        return get_numeric_value(value, self.is_int)

class NumericalExponentialDistEngine(NumpyEngine[Union[int, float]]):

    def __init__(self, scale=1.0, is_int=False):
        """Returns an exponential distributed value"""
        super().__init__()
        self.scale = scale
        self.is_int = is_int

    def sample(self) -> int:
        value = self._engine.exponential(self.scale)
        return get_numeric_value(value, self.is_int)

class NumericalBinomialDistEngine(NumpyEngine[Union[int, float]]):

    def __init__(self, n=1, p=0.5, is_int=False):
        """Returns a binomialy distributed value"""
        super().__init__()
        self.n = n
        self.p = p
        self.is_int = is_int

    def sample(self) -> int:
        value = self._engine.binomial(self.n, self.p)
        return get_numeric_value(value, self.is_int)


class NumericalPoissonDistEngine(NumpyEngine[Union[int, float]]):

    def __init__(self, lam=1.0, is_int=False):
        """Returns a poisson distributed value"""
        super().__init__()
        self.lam = lam
        self.is_int = is_int

    def sample(self) -> int:
        value = self._engine.poisson(self.lam)
        return get_numeric_value(value, self.is_int)



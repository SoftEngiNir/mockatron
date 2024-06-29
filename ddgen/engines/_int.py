
from ddgen.engines.base import RandEngine, Engine
from ddgen.helper_functions import generate_int_primary_key


class IntRandEngine(RandEngine[int]):

    def __init__(self, min_val=0, max_val=10_000) -> None:
        super().__init__()
        self.min_val = min_val
        self.max_val = max_val
    
    def sample(self):
        return self._engine.randint(self.min_val, self.max_val)

class IntPrimaryKeyEngine(Engine[int]):
    def __init__(self) -> None:
        self.key_generator = generate_int_primary_key()

    def sample(self):
        return next(self.key_generator)
    









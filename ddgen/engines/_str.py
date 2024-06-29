
from ddgen.engines.base import RandEngine, FakerEngine, Engine
import string
from ddgen.helper_functions import generate_uuid_as_str
from typing import List, Optional

class StrRandEngine(RandEngine[str]):

    def __init__(self, lenght=100) -> None:
        super().__init__()
        self.lenght = lenght
    
    def sample(self):
        letters = string.ascii_letters + string.digits + string.punctuation
        random_string = ''.join(self._engine.choice(letters) for _ in range(self.lenght))
        return random_string

class StrNameEngine(FakerEngine[str]):
    def sample(self):
        return self._engine.name()


class StrUuidEngine(Engine[str]):
    def sample(self):
        return generate_uuid_as_str()


class StrFromListEngine(RandEngine[str]):

    def __init__(self, selection: List[str], cum_weights: Optional[List[int]] = None) -> None:
        super().__init__()
        self.selection = selection
        self.cum_weights = cum_weights

    def sample(self):
        return self._engine.choices(self.selection, cum_weights=self.cum_weights)[0]



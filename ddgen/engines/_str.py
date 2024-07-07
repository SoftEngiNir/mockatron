from __future__ import annotations

import string

from ddgen.engines.base import Engine, FakerEngine, RandEngine
from ddgen.utilities.helper_functions import generate_uuid_as_str


class StrRandEngine(RandEngine[str]):
    def __init__(self, lenght=100) -> None:
        super().__init__()
        self.lenght = lenght

    def sample(self):
        letters = string.ascii_letters + string.digits + string.punctuation
        random_string = ''.join(
            self._engine.choice(letters) for _ in range(self.lenght)
        )
        return random_string


class StrNameEngine(FakerEngine[str]):
    def sample(self):
        return self._engine.name()


class StrAdressEngine(FakerEngine[str]):
    def sample(self):
        return self._engine.address()


class StrTextEngine(FakerEngine[str]):
    def sample(self):
        return self._engine.text()


class StrIPv4Engine(FakerEngine[str]):
    def sample(self):
        return self._engine.ipv4_private()


class StrEmailEngine(FakerEngine[str]):
    def sample(self):
        return self._engine.email()


class StrUuidEngine(Engine[str]):
    def sample(self):
        return generate_uuid_as_str()


class StrFromListEngine(RandEngine[str]):
    def __init__(
        self,
        selection: list[str],
        cum_weights: list[int] | None = None,
    ) -> None:
        super().__init__()
        self.selection = selection
        self.cum_weights = cum_weights

    def sample(self):
        return self._engine.choices(self.selection, cum_weights=self.cum_weights)[0]

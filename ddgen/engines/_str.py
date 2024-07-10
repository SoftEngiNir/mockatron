from __future__ import annotations

import string

from ddgen.engines.base import Engine, FakerEngine, RandEngine
from ddgen.engines.registry import register_engine
from ddgen.utilities.helper_functions import generate_uuid_as_str


@register_engine
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


@register_engine
class StrFromListEngine(RandEngine[str]):
    def __init__(
        self,
        selection: list[str],
        replace: bool = True,
        cum_weights: list[int] | None = None,
    ) -> None:
        super().__init__()
        self.selection = selection
        self.replace = replace
        self.cum_weights = cum_weights
        if not self.replace:
            self.used_indices: set = set()

    def sample(self):
        if not self.replace:
            if len(self.used_indices) >= len(self.selection):
                raise ValueError('No more unique elements to sample')

            available_indices = set(range(len(self.selection))) - self.used_indices
            chosen_index = self._engine.choice(list(available_indices))
            self.used_indices.add(chosen_index)
            return self.selection[chosen_index]
        return self._engine.choices(self.selection, cum_weights=self.cum_weights)[0]


@register_engine
class StrNameEngine(FakerEngine[str]):
    def sample(self):
        return self._engine.name()


@register_engine
class StrAdressEngine(FakerEngine[str]):
    def sample(self):
        return self._engine.address()


@register_engine
class StrTextEngine(FakerEngine[str]):
    def sample(self):
        return self._engine.text()


@register_engine
class StrIPv4Engine(FakerEngine[str]):
    def sample(self):
        return self._engine.ipv4_private()


@register_engine
class StrEmailEngine(FakerEngine[str]):
    def sample(self):
        return self._engine.email()


@register_engine
class StrUuidEngine(Engine[str]):
    def sample(self):
        return generate_uuid_as_str()

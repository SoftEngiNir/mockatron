class EngineRegistry:
    __shared_state: dict = {}

    def __init__(self) -> None:
        self.__dict__ = self.__shared_state
        if 'registry' not in self.__dict__:
            self.registry: dict = {}


def register_engine(cls):
    """Class decorator to register a class in the registry."""
    borg = EngineRegistry()
    borg.registry[cls.__name__] = cls
    return cls

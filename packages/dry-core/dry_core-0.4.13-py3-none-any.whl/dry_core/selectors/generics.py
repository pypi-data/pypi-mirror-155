from typing import TypeVar, Type, Generic


SelectorInstance = TypeVar("SelectorInstance")


class BaseSelector(Generic[SelectorInstance]):
    model: Type[SelectorInstance]

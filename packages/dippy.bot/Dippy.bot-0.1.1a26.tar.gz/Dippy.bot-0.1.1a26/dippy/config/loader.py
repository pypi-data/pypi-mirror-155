from __future__ import annotations
from typing import Any, Callable, Union
import pathlib


LoaderCallable = Callable[[pathlib.Path], dict[str, Any]]


class Loader:
    __dippy_loaders__: list[Loader] = []

    def __init__(
        self,
        loader_function: LoaderCallable,
        supported_file_types: set[str],
    ):
        self._file_type_predicate = None
        self._file_types = supported_file_types
        self._loader = loader_function
        self.__dippy_loaders__.append(self)

    def file_type_check(
        self, predicate: Callable[[str], bool]
    ) -> Callable[[str], bool]:
        self._file_type_predicate = predicate
        return predicate

    def load(self, config_file_path: pathlib.Path) -> dict[str, Any]:
        return self._loader(config_file_path)

    def supports_file_type(self, file_type: str) -> bool:
        if self._file_type_predicate:
            return self._file_type_predicate(file_type.casefold())

        return file_type.casefold() in self._file_types

    @classmethod
    def find_loader(cls, file_type: str):
        for loader in cls.__dippy_loaders__:
            if loader.supports_file_type(file_type):
                return loader


def loader(
    *args: Union[LoaderCallable, str]
) -> Union[Callable[[LoaderCallable], Loader], Loader]:
    supported_file_types = set()

    def register(loader_callable):
        return Loader(loader_callable, supported_file_types)

    if args and callable(args[0]):
        return register(args[0])

    supported_file_types = {file_type.casefold() for file_type in args}
    return register

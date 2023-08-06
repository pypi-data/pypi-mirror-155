from dippy.config.loader import Loader
from pathlib import Path
from typing import Any, Callable, Optional, TypeVar, Union


ConfigData = dict[str, Any]
T = TypeVar("T")


class Config:
    def __init__(self, *config_file_paths: Path):
        self._config_files = self._load_files(*config_file_paths)

    def get(
        self,
        section: str,
        builder: Optional[Callable[[ConfigData], T]] = None,
        default: Optional[Any] = None,
    ) -> Optional[Union[ConfigData, T]]:
        for config in self._config_files:
            if section in config:
                print(config[section])
                return builder(**config[section]) if builder else config[section]

        return default

    def _load_files(self, *config_file_paths: Path) -> list[ConfigData]:
        configs = []
        for path in config_file_paths:
            file_type = path.suffix.strip(".")
            loader = Loader.find_loader(file_type)
            if not loader:
                raise TypeError(f"No config loader found for '{file_type}' files")

            configs.append(loader.load(path))

        return configs

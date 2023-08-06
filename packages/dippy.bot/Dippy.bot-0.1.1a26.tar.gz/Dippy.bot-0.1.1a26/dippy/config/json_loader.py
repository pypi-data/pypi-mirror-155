from dippy.config.loader import loader
from pathlib import Path
from typing import Any
import json


@loader("json")
def json_loader(config_path: Path) -> dict[str, Any]:
    with open(config_path.resolve(), "r") as json_file:
        return json.load(json_file)

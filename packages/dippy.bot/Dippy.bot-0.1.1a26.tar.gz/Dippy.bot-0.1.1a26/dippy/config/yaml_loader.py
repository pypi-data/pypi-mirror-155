from dippy.config.loader import loader
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    from dippy.utils.missing_module import MissingModule

    yaml = MissingModule("You must install pyyaml to load YAML config files.")


@loader("yaml", "yml")
def yaml_loader(config_path: Path) -> dict[str, Any]:
    with open(config_path.resolve(), "r") as yaml_file:
        return yaml.load(yaml_file, Loader=yaml.FullLoader)

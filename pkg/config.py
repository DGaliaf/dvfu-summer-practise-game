import json
from typing import Any


def getConfig(config_path: str) -> dict[str, Any]:
    with open(config_path) as cfg:
        return json.load(cfg)

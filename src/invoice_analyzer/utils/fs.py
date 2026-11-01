from pathlib import Path
from typing import Any

import yaml


def read_file(filepath: Path) -> str:
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def read_yaml(filepath: Path) -> Any:
    return yaml.safe_load(read_file(filepath))


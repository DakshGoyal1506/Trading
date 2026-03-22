from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

import yaml

def load_yaml(path: str | Path) -> Dict[str, Any]:
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"Configuration file not found: {path}")
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data
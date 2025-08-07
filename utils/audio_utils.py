import json
from pathlib import Path
from typing import Any, Dict


def load_presets(path: str | Path) -> Dict[str, Any]:
    """Load presets configuration from a JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_presets(path: str | Path, presets: Dict[str, Any]) -> None:
    """Save presets configuration to a JSON file."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(presets, f, indent=2)

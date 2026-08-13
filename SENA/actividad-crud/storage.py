"""Módulo para cargar y guardar aprendices en un archivo JSON."""

from __future__ import annotations

import json
from pathlib import Path
from typing import List


def load_aprendices(archivo: str | Path = "aprendices.json") -> List[dict[str, str]]:
    """Carga los aprendices desde un archivo JSON si existe."""
    path = Path(archivo)
    if not path.exists():
        return []

    with path.open("r", encoding="utf-8") as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            return []

    if isinstance(data, list):
        return data

    return []


def save_aprendices(archivo: str | Path, aprendices: List[dict[str, str]]) -> bool:
    """Guarda la lista de aprendices en formato JSON."""
    path = Path(archivo)
    with path.open("w", encoding="utf-8") as file:
        json.dump(aprendices, file, indent=2, ensure_ascii=False)
    return True

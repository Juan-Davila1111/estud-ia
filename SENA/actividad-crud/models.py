"""Modelos y tipos utilizados por el sistema de aprendices."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

TIPOS_DOCUMENTO = {"CC", "TI", "CE"}


@dataclass
class AppContext:
    """Contiene el estado compartido del programa."""

    archivo: Path
    aprendices: List[dict[str, str]] = field(default_factory=list)


class MenuAction(ABC):
    """Contrato base para las estrategias del menú."""

    @abstractmethod
    def execute(self, context: AppContext) -> None:
        """Ejecuta la acción asociada a una opción del menú."""
        raise NotImplementedError

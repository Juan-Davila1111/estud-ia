"""Gestión del menú interactivo y las estrategias del patrón Strategy."""

from __future__ import annotations

from models import AppContext, MenuAction
from services import consultar_aprendiz, eliminar_aprendiz, listar_aprendices, listar_por_ficha, registrar_aprendiz


class RegistrarAprendizStrategy(MenuAction):
    """Estrategia para registrar un aprendiz."""

    def execute(self, context: AppContext) -> None:
        registrar_aprendiz(context.aprendices, context.archivo)


class ConsultarAprendizStrategy(MenuAction):
    """Estrategia para consultar un aprendiz."""

    def execute(self, context: AppContext) -> None:
        consultar_aprendiz(context.aprendices)


class ListarAprendicesStrategy(MenuAction):
    """Estrategia para listar todos los aprendices."""

    def execute(self, context: AppContext) -> None:
        listar_aprendices(context.aprendices)


class ListarPorFichaStrategy(MenuAction):
    """Estrategia para filtrar aprendices por ficha."""

    def execute(self, context: AppContext) -> None:
        listar_por_ficha(context.aprendices)


class EliminarAprendizStrategy(MenuAction):
    """Estrategia para eliminar un aprendiz."""

    def execute(self, context: AppContext) -> None:
        eliminar_aprendiz(context.aprendices, context.archivo)


class SalirStrategy(MenuAction):
    """Estrategia para salir del sistema."""

    def execute(self, context: AppContext) -> None:
        print("Gracias por usar el sistema.")


MENU_OPTIONS = {
    "1": ("Registrar Aprendiz", RegistrarAprendizStrategy()),
    "2": ("Consultar Aprendiz", ConsultarAprendizStrategy()),
    "3": ("Listar Aprendices", ListarAprendicesStrategy()),
    "4": ("Listar por Ficha", ListarPorFichaStrategy()),
    "5": ("Eliminar Aprendiz", EliminarAprendizStrategy()),
    "6": ("Salir", SalirStrategy()),
}


def mostrar_menu() -> None:
    """Imprime las opciones disponibles en el menú."""
    print("\nSistema de Registro de Aprendices SENA")
    for opcion, (nombre, _) in MENU_OPTIONS.items():
        print(f"{opcion}. {nombre}")


def ejecutar_opcion(opcion: str, context: AppContext) -> bool:
    """Ejecuta la estrategia correspondiente a la opción seleccionada."""
    if opcion == "6":
        MENU_OPTIONS[opcion][1].execute(context)
        return False

    estrategia = MENU_OPTIONS.get(opcion)
    if estrategia is None:
        print("Opción no válida.")
        return True

    estrategia[1].execute(context)
    return True

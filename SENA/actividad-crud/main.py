"""Punto de entrada del sistema de registro de aprendices."""

from pathlib import Path

from menu import ejecutar_opcion, mostrar_menu
from models import AppContext
from storage import load_aprendices


def main() -> None:
    """Inicia el programa y mantiene activo el menú interactivo."""
    archivo = Path(__file__).with_name("aprendices.json")
    aprendices = load_aprendices(archivo)
    context = AppContext(archivo=archivo, aprendices=aprendices)

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()
        if not ejecutar_opcion(opcion, context):
            break

main()
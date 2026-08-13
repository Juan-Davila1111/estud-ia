"""Operaciones de negocio del sistema de registro de aprendices."""

from __future__ import annotations

from pathlib import Path
from typing import List

from models import TIPOS_DOCUMENTO
from storage import save_aprendices


def registrar_aprendiz(aprendices: List[dict[str, str]], archivo: str | Path) -> bool:
    """Registra un nuevo aprendiz si el documento no existe."""
    tipo_documento = input("Tipo de documento (CC, TI, CE): ").strip().upper()
    while tipo_documento not in TIPOS_DOCUMENTO:
        print("Tipo de documento inválido. Debe ser CC, TI o CE.")
        tipo_documento = input("Tipo de documento (CC, TI, CE): ").strip().upper()

    numero_documento = input("Número de documento: ").strip()
    while not numero_documento.isdigit() or not numero_documento:
        print("El número de documento debe contener solo dígitos.")
        numero_documento = input("Número de documento: ").strip()

    if any(aprendiz["numero_documento"] == numero_documento for aprendiz in aprendices):
        print("Ya existe un aprendiz con ese número de documento.")
        return False

    nombre_completo = input("Nombre completo: ").strip()
    while not nombre_completo:
        print("El nombre completo es obligatorio.")
        nombre_completo = input("Nombre completo: ").strip()

    numero_ficha = input("Número de ficha: ").strip()
    while not numero_ficha.isdigit() or not numero_ficha:
        print("La ficha debe contener solo dígitos.")
        numero_ficha = input("Número de ficha: ").strip()

    programa_formacion = input("Programa de formación: ").strip()
    while not programa_formacion:
        print("El programa de formación es obligatorio.")
        programa_formacion = input("Programa de formación: ").strip()

    aprendiz = {
        "tipo_documento": tipo_documento,
        "numero_documento": numero_documento,
        "nombre_completo": nombre_completo,
        "numero_ficha": numero_ficha,
        "programa_formacion": programa_formacion,
    }

    aprendices.append(aprendiz)
    save_aprendices(archivo, aprendices)
    print("Aprendiz registrado correctamente.")
    return True


def consultar_aprendiz(aprendices: List[dict[str, str]]) -> bool:
    """Busca un aprendiz por número de documento y muestra su ficha técnica."""
    numero_documento = input("Ingrese el número de documento: ").strip()
    for aprendiz in aprendices:
        if aprendiz["numero_documento"] == numero_documento:
            print("\nFicha técnica del aprendiz")
            print(f"Tipo de documento: {aprendiz['tipo_documento']}")
            print(f"Número de documento: {aprendiz['numero_documento']}")
            print(f"Nombre completo: {aprendiz['nombre_completo']}")
            print(f"Número de ficha: {aprendiz['numero_ficha']}")
            print(f"Programa de formación: {aprendiz['programa_formacion']}")
            return True

    print("No se encontró un aprendiz con ese documento.")
    return False


def listar_aprendices(aprendices: List[dict[str, str]]) -> None:
    """Muestra una lista resumida de todos los aprendices."""
    if not aprendices:
        print("No hay aprendices registrados.")
        return

    print("\nLista de aprendices registrados:")
    for aprendiz in aprendices:
        print(
            f"- {aprendiz['nombre_completo']} | Doc: {aprendiz['numero_documento']} | "
            f"Ficha: {aprendiz['numero_ficha']} | Programa: {aprendiz['programa_formacion']}"
        )


def listar_por_ficha(aprendices: List[dict[str, str]]) -> None:
    """Filtra y muestra los aprendices de una ficha específica."""
    numero_ficha = input("Ingrese el número de ficha: ").strip()
    if not numero_ficha.isdigit():
        print("La ficha debe contener solo dígitos.")
        return

    resultados = [aprendiz for aprendiz in aprendices if aprendiz["numero_ficha"] == numero_ficha]
    if not resultados:
        print("No hay aprendices para esa ficha.")
        return

    print(f"\nAprendices de la ficha {numero_ficha}:")
    for aprendiz in resultados:
        print(f"- {aprendiz['nombre_completo']} | Tipo documento {aprendiz['tipo_documento']} | Doc: {aprendiz['numero_documento']}")


def eliminar_aprendiz(aprendices: List[dict[str, str]], archivo: str | Path) -> bool:
    """Elimina un aprendiz por su número de documento."""
    numero_documento = input("Ingrese el número de documento del aprendiz a eliminar: ").strip()
    for aprendiz in aprendices:
        if aprendiz["numero_documento"] == numero_documento:
            aprendices.remove(aprendiz)
            save_aprendices(archivo, aprendices)
            print("Aprendiz eliminado correctamente.")
            return True

    print("No se encontró un aprendiz con ese documento.")
    return False

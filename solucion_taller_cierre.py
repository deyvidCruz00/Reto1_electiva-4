"""Solucion para las actividades 1 a 4 del Taller Unidad I.

Guarde Unidad1_Reto.json en esta misma carpeta y ejecute:
    python solucion_taller_cierre.py
"""

import json
from pathlib import Path


ARCHIVO = Path(__file__).with_name("Unidad1_Reto.json")
DOMINIO = "@uptc.edu.co"


def texto(valor):
    """Convierte None en cadena vacia y elimina espacios sobrantes."""
    return "" if valor is None else str(valor).strip()


def valor_por_nombre(datos, palabra):
    """Busca un valor en un diccionario usando una parte del nombre de su llave."""
    if not isinstance(datos, dict):
        return ""
    for llave, valor in datos.items():
        if palabra in llave.casefold():
            return texto(valor)
    return ""


def estudiantes_de(datos):
    """Obtiene la lista de estudiantes, aunque el JSON use lista o diccionario."""
    if isinstance(datos, list):
        return datos
    if "estudiantes" in datos:
        return datos["estudiantes"]
    return list(datos.values())


def partes_nombre(estudiante):
    nombres = estudiante.get("nombres", {})
    apellidos = estudiante.get("apellidos", {})

    primer_nombre = valor_por_nombre(nombres, "primer")
    segundo_nombre = valor_por_nombre(nombres, "segundo")
    primer_apellido = valor_por_nombre(apellidos, "primer")
    segundo_apellido = valor_por_nombre(apellidos, "segundo")

    return primer_nombre, segundo_nombre, primer_apellido, segundo_apellido


def promedio_por_asignatura(estudiantes):
    """Actividad 2: acumula notas y cantidad de registros por asignatura."""
    acumulados = {}
    for estudiante in estudiantes:
        for asignatura in estudiante.get("asignaturas", []):
            nombre = asignatura["nombre"]
            nota = float(asignatura["nota"])
            if nombre not in acumulados:
                acumulados[nombre] = {"suma": 0, "cantidad": 0}
            acumulados[nombre]["suma"] += nota
            acumulados[nombre]["cantidad"] += 1

    return {
        nombre: round(datos["suma"] / datos["cantidad"], 2)
        for nombre, datos in acumulados.items()
    }


def promedio_por_estudiante(estudiantes):
    """Actividad 3: calcula solo asignaturas que no fueron retiradas."""
    resultado = []
    for estudiante in estudiantes:
        cursadas = [
            float(asignatura["nota"])
            for asignatura in estudiante.get("asignaturas", [])
            if texto(asignatura.get("retirada")).casefold() == "no"
        ]
        primer_nombre, _, primer_apellido, segundo_apellido = partes_nombre(estudiante)
        nombre_completo = " ".join(
            parte
            for parte in (primer_nombre, primer_apellido, segundo_apellido)
            if parte
        )
        promedio = round(sum(cursadas) / len(cursadas), 2) if cursadas else None
        resultado.append(
            {
                "codigo": estudiante.get("codigo"),
                "estudiante": nombre_completo,
                "promedio": promedio,
                "_apellido": primer_apellido.casefold(),
            }
        )

    resultado.sort(key=lambda estudiante: estudiante["_apellido"])
    for estudiante in resultado:
        del estudiante["_apellido"]
    return resultado


def correo_institucional(estudiante):
    """Actividad 4: construye el correo usando las reglas del enunciado."""
    primer_nombre, segundo_nombre, primer_apellido, segundo_apellido = partes_nombre(estudiante)
    documento = texto(estudiante.get("documento"))[-2:]

    if segundo_nombre:
        usuario = f"{primer_nombre[:1]}{segundo_nombre[:1]}.{primer_apellido}.{documento}"
    else:
        usuario = f"{primer_nombre[:1]}.{primer_apellido[:1]}.{segundo_apellido}.{documento}"
    return usuario.casefold() + DOMINIO


def estudiantes_y_correos(estudiantes):
    """Actividad 4: devuelve una lista de diccionarios con nombre y correo."""
    resultado = []
    for estudiante in estudiantes:
        primer_nombre, segundo_nombre, primer_apellido, segundo_apellido = partes_nombre(estudiante)
        nombre_completo = " ".join(
            parte
            for parte in (primer_nombre, segundo_nombre, primer_apellido, segundo_apellido)
            if parte
        )
        resultado.append(
            {"estudiante": nombre_completo, "correo": correo_institucional(estudiante)}
        )
    return resultado


def main():
    with ARCHIVO.open(encoding="utf-8") as archivo:
        datos = json.load(archivo)

    estudiantes = estudiantes_de(datos)
    print("PROMEDIO POR ASIGNATURA")
    print(promedio_por_asignatura(estudiantes))
    print("\nPROMEDIO POR ESTUDIANTE (ordenado por apellido)")
    for estudiante in promedio_por_estudiante(estudiantes):
        print(estudiante)
    print("\nESTUDIANTES Y CORREOS INSTITUCIONALES")
    for estudiante in estudiantes_y_correos(estudiantes):
        print(estudiante)


if __name__ == "__main__":
    main()

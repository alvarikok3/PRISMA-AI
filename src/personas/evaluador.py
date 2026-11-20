"""Evaluación de cobertura de datos personales, sin predicciones clínicas o actuariales.

Los indicadores son descripciones de exposición, NO probabilidades.
"""
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Categoria:
    nombre: str
    campos: tuple[str, ...]
    descripcion: str


CATEGORIAS = {
    "Movilidad": Categoria(
        "Movilidad", ("transporte", "viajes_semana", "km_semana", "incidentes_viales"),
        "Exposición durante desplazamientos y antecedentes viales.",
    ),
    "Seguridad laboral": Categoria(
        "Seguridad laboral", ("ocupacion", "horas_semana", "exposicion_laboral", "incidentes_laborales"),
        "Condiciones de trabajo y antecedentes de incidentes.",
    ),
    "Riesgos ambientales": Categoria(
        "Riesgos ambientales", ("region", "inundacion", "deslizamiento"),
        "Exposición declarada a peligros del entorno; requiere datos geográficos verificables.",
    ),
    "Estabilidad financiera": Categoria(
        "Estabilidad financiera", ("ingresos", "gastos", "ahorro_emergencia"),
        "Indicadores financieros descriptivos; no representa evaluación crediticia.",
    ),
}


def evaluar_perfil(perfil: dict[str, Any], autorizaciones: dict[str, bool]) -> list[dict[str, Any]]:
    """Identifica módulos habilitados y datos faltantes, sin estimar siniestros."""
    resultados = []
    for nombre, categoria in CATEGORIAS.items():
        if not autorizaciones.get(nombre, False):
            resultados.append({
                "categoria": nombre, "estado": "Sin autorización",
                "faltantes": [], "descripcion": categoria.descripcion,
                "indicadores": [], "prediccion": None,
            })
            continue

        faltantes = [campo for campo in categoria.campos if perfil.get(campo) is None or perfil.get(campo) == ""]
        indicadores = []
        if not faltantes:
            if nombre == "Movilidad":
                indicadores = [
                    f"Desplazamientos semanales: {perfil['viajes_semana']}",
                    f"Distancia semanal declarada: {perfil['km_semana']} km",
                    f"Incidentes viales anteriores: {perfil['incidentes_viales']}",
                ]
            elif nombre == "Seguridad laboral":
                indicadores = [
                    f"Horas laborales semanales: {perfil['horas_semana']}",
                    f"Exposición laboral declarada: {perfil['exposicion_laboral']}",
                    f"Incidentes laborales anteriores: {perfil['incidentes_laborales']}",
                ]
            elif nombre == "Riesgos ambientales":
                indicadores = [
                    f"Exposición a inundación declarada: {perfil['inundacion']}",
                    f"Exposición a deslizamiento declarada: {perfil['deslizamiento']}",
                ]
            elif nombre == "Estabilidad financiera":
                ingresos = perfil["ingresos"]
                gastos = perfil["gastos"]
                if ingresos > 0:
                    indicadores = [f"Gastos / ingresos declarados: {gastos / ingresos:.1%}"]
                else:
                    indicadores = ["Ingresos declarados iguales a cero: proporción no calculable"]
                indicadores.append(f"Meses de ahorro de emergencia: {perfil['ahorro_emergencia']}")

        resultados.append({
            "categoria": nombre,
            "estado": "Datos completos; modelo pendiente" if not faltantes else "Faltan datos",
            "faltantes": faltantes,
            "descripcion": categoria.descripcion,
            "indicadores": indicadores,
            "prediccion": None,
        })
    return resultados

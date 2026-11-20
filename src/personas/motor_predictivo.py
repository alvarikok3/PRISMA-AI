"""Motor de escenarios v0.6: tasas hipotéticas, NO predicción actuarial validada.

Las tasas y multiplicadores son supuestos pedagógicos explícitos. No utilizar
para suscripción, denegación de coberturas ni evaluación de personas reales.
"""
from math import exp

TASAS_ANUALES_HIPOTETICAS = {
    "laboral": 0.035,
    "vial": 0.025,
}
OCUPACION_FACTOR = {
    "Oficina": 0.75, "Salud": 1.15, "Conducción": 1.45,
    "Industria": 1.55, "Deporte": 1.35, "Otra": 1.0,
}
EXPOSICION_FACTOR = {"Baja": 0.7, "Media": 1.0, "Alta": 1.65, "Desconocida": 1.0}
TRANSPORTE_FACTOR = {
    "Automóvil": 1.0, "Motocicleta": 1.8, "Transporte público": 0.65,
    "Bicicleta": 1.25, "Caminata": 0.75, "Otro": 1.0,
}


def probabilidad_evento(tasa_anual: float, meses: int) -> float:
    """Probabilidad hipotética de >=1 evento en un proceso de Poisson."""
    if tasa_anual < 0 or meses <= 0:
        raise ValueError("Tasa y horizonte inválidos")
    return 100 * (1 - exp(-tasa_anual * meses / 12))


def simular_riesgos(perfil: dict, meses: int, autorizaciones: dict) -> list[dict]:
    """Simula escenarios comparables; no aprende de siniestros observados."""
    resultados = []
    if autorizaciones.get("Seguridad laboral"):
        horas = perfil["horas_semana"]
        incidentes = perfil["incidentes_laborales"]
        tasa = (
            TASAS_ANUALES_HIPOTETICAS["laboral"]
            * OCUPACION_FACTOR[perfil["ocupacion"]]
            * EXPOSICION_FACTOR[perfil["exposicion_laboral"]]
            * max(0.25, horas / 40)
            * (1 + 0.20 * min(incidentes, 5))
        )
        resultados.append({
            "evento": "Al menos un incidente laboral (escenario hipotético)",
            "categoria": "Seguridad laboral",
            "porcentaje": round(probabilidad_evento(tasa, meses), 2),
            "factores": [
                f"Ocupación: {perfil['ocupacion']}",
                f"Exposición laboral: {perfil['exposicion_laboral']}",
                f"Horas semanales: {horas}",
                f"Incidentes anteriores: {incidentes}",
            ],
        })
    if autorizaciones.get("Movilidad"):
        km = perfil["km_semana"]
        viajes = perfil["viajes_semana"]
        incidentes = perfil["incidentes_viales"]
        tasa = (
            TASAS_ANUALES_HIPOTETICAS["vial"]
            * TRANSPORTE_FACTOR[perfil["transporte"]]
            * max(0.0, km / 100)
            * (1 + 0.15 * min(incidentes, 5))
            * (1.0 if viajes > 0 else 0.0)
        )
        resultados.append({
            "evento": "Al menos un incidente vial (escenario hipotético)",
            "categoria": "Movilidad",
            "porcentaje": round(probabilidad_evento(tasa, meses), 2),
            "factores": [
                f"Transporte: {perfil['transporte']}",
                f"Distancia semanal: {km} km",
                f"Viajes semanales: {viajes}",
                f"Incidentes anteriores: {incidentes}",
            ],
        })
    return resultados


def orientacion_coberturas(perfil: dict, autorizaciones: dict) -> tuple[list[str], list[str]]:
    """Opciones a consultar y coberturas que requieren verificar pertinencia.

    Nunca genera denegaciones o exclusiones individuales.
    """
    considerar = []
    revisar = []
    if autorizaciones.get("Movilidad"):
        considerar.append(
            "Protección por accidentes personales y asistencia durante desplazamientos: "
            "revisar límites, deducibles y exclusiones."
        )
        if perfil["transporte"] in ("Automóvil", "Motocicleta"):
            considerar.append(
                "Seguro vehicular y responsabilidad civil: comprobar obligaciones "
                "legales, titularidad y cobertura vigente."
            )
        else:
            revisar.append(
                "Cobertura para vehículo propio: comprobar si corresponde; "
                "no contratarla solo por usar transporte público o caminar."
            )
    if autorizaciones.get("Seguridad laboral"):
        considerar.append(
            "Cobertura de riesgos del trabajo: verificar protección del empleador "
            "y mecanismos legales aplicables antes de contratar un complemento."
        )
    revisar.append(
        "Coberturas duplicadas, complementos para actividades no realizadas "
        "y servicios ya incluidos en otras pólizas: comprobar su utilidad."
    )
    return considerar, revisar

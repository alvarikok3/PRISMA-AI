"""Catálogo clínico de investigación; NO es un modelo diagnóstico o pronóstico.

Variables orientativas que deben validarse contra una herramienta clínica concreta.
No se asignan puntuaciones ni probabilidades a personas.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Evaluacion:
    nombre: str
    campos: tuple[str, ...]
    nota: str


EVALUACIONES = {
    "Cardiovascular (infarto/ictus)": Evaluacion(
        "Cardiovascular (infarto/ictus)",
        ("edad", "presion_sistolica", "tabaquismo", "diabetes", "colesterol_total", "hdl"),
        "Un cálculo clínico real requiere seleccionar y validar una ecuación, población y horizonte.",
    ),
    "Diabetes tipo 2": Evaluacion(
        "Diabetes tipo 2", ("edad", "imc", "actividad_fisica", "antecedentes_familiares", "hba1c"),
        "HbA1c puede orientar evaluación clínica; no constituye predicción automática.",
    ),
    "Enfermedad renal": Evaluacion(
        "Enfermedad renal", ("edad", "creatinina", "albuminuria", "diabetes", "hipertension"),
        "La función renal y progresión requieren mediciones clínicas repetidas y modelos adecuados.",
    ),
    "Enfermedad respiratoria": Evaluacion(
        "Enfermedad respiratoria", ("tabaquismo", "exposicion_humo", "diagnostico_respiratorio", "espirometria"),
        "No inferir EPOC, asma ni mortalidad a partir de un cuestionario.",
    ),
    "Cáncer de pulmón": Evaluacion(
        "Cáncer de pulmón", ("edad", "tabaquismo", "paquetes_anio", "antecedentes_familiares"),
        "La elegibilidad para tamizaje depende de guías locales y criterios clínicos.",
    ),
    "Cáncer colorrectal": Evaluacion(
        "Cáncer colorrectal", ("edad", "antecedentes_familiares", "antecedentes_polipos", "enfermedad_intestinal"),
        "La prevención y el tamizaje requieren evaluación de antecedentes y edad.",
    ),
    "Cáncer de mama": Evaluacion(
        "Cáncer de mama", ("edad", "antecedentes_familiares", "antecedentes_mama", "antecedentes_geneticos"),
        "El modelo solo debe aplicarse cuando sea clínicamente pertinente; no diagnostica cáncer.",
    ),
    "Cáncer de cuello uterino": Evaluacion(
        "Cáncer de cuello uterino", ("edad", "estado_vph", "tamizaje_cervical"),
        "La indicación de tamizaje se individualiza según anatomía, edad y guías vigentes.",
    ),
    "Cáncer de próstata": Evaluacion(
        "Cáncer de próstata", ("edad", "antecedentes_familiares", "antecedentes_prostata"),
        "La decisión sobre PSA y tamizaje debe compartirse con profesionales de salud.",
    ),
    "Cáncer de piel": Evaluacion(
        "Cáncer de piel", ("exposicion_uv", "antecedentes_piel", "antecedentes_familiares"),
        "Lesiones sospechosas necesitan valoración clínica; no es diagnóstico por imagen.",
    ),
    "Cáncer de hígado": Evaluacion(
        "Cáncer de hígado", ("hepatitis", "cirrosis", "consumo_alcohol"),
        "La vigilancia de hepatocarcinoma depende de diagnósticos y guías clínicas.",
    ),
    "Mortalidad por causas específicas": Evaluacion(
        "Mortalidad por causas específicas", ("edad", "diagnosticos_confirmados", "seguimiento_longitudinal"),
        "No es posible predecir una causa individual de muerte con este formulario. "
        "Requiere datos longitudinales, mortalidad verificada y modelos de riesgos competitivos.",
    ),
}


def revisar_disponibilidad(datos: dict, autorizadas: list[str]) -> list[dict]:
    resultados = []
    for nombre, evaluacion in EVALUACIONES.items():
        if nombre not in autorizadas:
            continue
        faltantes = [x for x in evaluacion.campos if datos.get(x) in (None, "", "No informado")]
        resultados.append({
            "nombre": nombre,
            "faltantes": faltantes,
            "completitud": round(100 * (len(evaluacion.campos) - len(faltantes)) / len(evaluacion.campos)),
            "nota": evaluacion.nota,
            "probabilidad": None,
            "estado": "Datos descriptivos completos; modelo clínico no integrado" if not faltantes
                      else "Faltan variables",
        })
    return resultados

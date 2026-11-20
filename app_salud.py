"""PRISMA AI v0.7: evaluación de disponibilidad de datos clínicos ficticios."""
import streamlit as st
from src.salud.catalogo import EVALUACIONES, revisar_disponibilidad

st.set_page_config(page_title="PRISMA AI | Salud", page_icon="🩺", layout="wide")
st.title("PRISMA AI v0.7 — Salud, cáncer y mortalidad")
st.error(
    "MÓDULO DE INVESTIGACIÓN. No diagnostica cáncer, no calcula probabilidad de muerte "
    "ni sustituye una evaluación médica. No introducir información clínica real o identificable. "
    "Los datos permanecen en la sesión y no se guardan en una base de datos de esta aplicación."
)
st.markdown(
    "Este módulo identifica **qué información faltaría** para investigar modelos clínicos "
    "específicos. No asigna porcentajes sin un modelo validado para la población."
)
st.subheader("1. Consentimiento y categorías")
consentimiento = st.checkbox("Confirmo que usaré exclusivamente un perfil ficticio para esta demostración.")
autorizadas = st.multiselect(
    "Categorías a revisar automáticamente (puedes elegir todas)",
    list(EVALUACIONES),
    default=["Cardiovascular (infarto/ictus)", "Diabetes tipo 2", "Cáncer de pulmón",
             "Cáncer colorrectal", "Mortalidad por causas específicas"],
    disabled=not consentimiento,
)
if not consentimiento:
    st.info("Confirma el uso de datos ficticios para habilitar el formulario.")
    st.stop()

st.subheader("2. Variables clínicas ficticias")
st.caption("Deja en 'No informado' las variables que desconozcas. No introduzcas datos personales reales.")
datos = {}
campos = sorted({campo for nombre in autorizadas for campo in EVALUACIONES[nombre].campos})
numericos = {
    "edad": (18, 120, 35), "presion_sistolica": (60, 260, 120),
    "colesterol_total": (50, 500, 190), "hdl": (10, 150, 50),
    "imc": (10.0, 80.0, 25.0), "hba1c": (3.0, 20.0, 5.5),
    "creatinina": (0.1, 20.0, 0.9), "albuminuria": (0.0, 10000.0, 10.0),
    "paquetes_anio": (0.0, 150.0, 0.0),
}
etiquetas = {
    "edad": "Edad (años)", "presion_sistolica": "Presión sistólica (mmHg)",
    "colesterol_total": "Colesterol total (mg/dL)", "hdl": "Colesterol HDL (mg/dL)",
    "imc": "Índice de masa corporal (kg/m²)", "hba1c": "HbA1c (%)",
    "creatinina": "Creatinina (mg/dL)", "albuminuria": "Albuminuria (mg/g, si corresponde)",
    "paquetes_anio": "Tabaquismo acumulado (paquetes-año)",
}
opciones = {
    "tabaquismo": ["No informado", "Nunca", "Anterior", "Actual"],
    "actividad_fisica": ["No informado", "Regular", "Insuficiente"],
    "antecedentes_familiares": ["No informado", "Sí", "No"],
    "diabetes": ["No informado", "Diagnóstico confirmado", "No"],
    "hipertension": ["No informado", "Diagnóstico confirmado", "No"],
    "diagnostico_respiratorio": ["No informado", "Sí", "No"],
    "exposicion_humo": ["No informado", "Sí", "No"],
    "antecedentes_polipos": ["No informado", "Sí", "No"],
    "enfermedad_intestinal": ["No informado", "Sí", "No"],
    "antecedentes_mama": ["No informado", "Sí", "No", "No aplica"],
    "antecedentes_geneticos": ["No informado", "Sí", "No"],
    "estado_vph": ["No informado", "Positivo", "Negativo", "No aplica"],
    "tamizaje_cervical": ["No informado", "Al día", "Pendiente", "No aplica"],
    "antecedentes_prostata": ["No informado", "Sí", "No", "No aplica"],
    "exposicion_uv": ["No informado", "Baja", "Media", "Alta"],
    "antecedentes_piel": ["No informado", "Sí", "No"],
    "hepatitis": ["No informado", "Sí", "No"],
    "cirrosis": ["No informado", "Sí", "No"],
    "consumo_alcohol": ["No informado", "No consume", "Ocasional", "Frecuente"],
    "diagnosticos_confirmados": ["No informado", "Sí", "No"],
    "seguimiento_longitudinal": ["No informado", "Disponible", "No disponible"],
    "espirometria": ["No informado", "Disponible", "No disponible"],
}
columnas = st.columns(2)
for i, campo in enumerate(campos):
    with columnas[i % 2]:
        etiqueta = etiquetas.get(campo, campo.replace("_", " ").capitalize())
        if campo in numericos:
            minimo, maximo, predeterminado = numericos[campo]
            conocido = st.checkbox(f"Tengo dato ficticio: {etiqueta}", value=campo == "edad", key="check_" + campo)
            if conocido:
                datos[campo] = st.number_input(
                    etiqueta, min_value=minimo, max_value=maximo,
                    value=predeterminado, key="num_" + campo,
                )
            else:
                datos[campo] = None
        else:
            datos[campo] = st.selectbox(etiqueta, opciones.get(campo, ["No informado", "Sí", "No"]),
                                        key="sel_" + campo)

st.subheader("3. Evaluación de disponibilidad")
if st.button("Analizar categorías de salud", type="primary"):
    resultados = revisar_disponibilidad(datos, autorizadas)
    if not resultados:
        st.info("Selecciona al menos una categoría.")
    for resultado in resultados:
        with st.expander(f"{resultado['nombre']} — {resultado['estado']}", expanded=True):
            st.progress(resultado["completitud"] / 100)
            st.write(f"Completitud del formulario: {resultado['completitud']} %")
            if resultado["faltantes"]:
                st.write("Variables faltantes: " + ", ".join(
                    x.replace("_", " ") for x in resultado["faltantes"]
                ))
            st.info(resultado["nota"])
            st.write("**Probabilidad de enfermedad o muerte: no disponible.**")
    st.warning(
        "La completitud de datos NO mide riesgo de enfermedad. No es válido deducir "
        "una causa de muerte, excluir seguros o emitir diagnósticos con estos resultados."
    )

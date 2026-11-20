"""PRISMA AI v0.6 — simulación de escenarios personales.

Se calculan porcentajes de escenarios hipotéticos, no riesgos actuariales reales.
"""
import streamlit as st
from src.personas.evaluador import CATEGORIAS, evaluar_perfil
from src.personas.motor_predictivo import simular_riesgos, orientacion_coberturas

st.set_page_config(page_title="PRISMA AI | Personas", page_icon="🧭", layout="wide")
st.title("PRISMA AI — Evaluación integral de riesgos personales")
st.info("Nuevo módulo de salud v0.7 disponible: ejecuta `python -m streamlit run app_salud.py --server.address 0.0.0.0 --server.port 8501` después de detener esta aplicación.")
st.warning(
    "DEMOSTRACIÓN CON TASAS HIPOTÉTICAS: los porcentajes son simulaciones matemáticas, "
    "NO probabilidades reales validadas. No utilizar para aceptar, rechazar, tarifar "
    "o excluir coberturas de seguros, ni para decisiones laborales o médicas. "
    "Introduce únicamente perfiles ficticios."
)

st.subheader("1. Perfil general (utiliza datos ficticios)")
edad = st.number_input("Edad (años)", min_value=18, max_value=120, value=35)
ocupacion = st.selectbox(
    "Ocupación", ["Oficina", "Salud", "Conducción", "Industria", "Deporte", "Otra"]
)
horizonte = st.selectbox("Horizonte de análisis futuro", ["12 meses", "3 años", "5 años"])
st.caption("Horizonte aplicado a la simulación; no existe calibración actuarial para ese plazo.")

st.subheader("2. Autorización por categoría")
st.caption("Se revisarán automáticamente todas las categorías que autorices.")
autorizaciones = {}
cols = st.columns(2)
for i, (nombre, categoria) in enumerate(CATEGORIAS.items()):
    with cols[i % 2]:
        autorizaciones[nombre] = st.checkbox(
            nombre, value=nombre in ("Movilidad", "Seguridad laboral"),
            help=categoria.descripcion,
        )

perfil = {"edad": edad, "ocupacion": ocupacion, "horizonte": horizonte}

if autorizaciones["Movilidad"]:
    st.subheader("3. Movilidad")
    perfil["transporte"] = st.selectbox(
        "Transporte habitual", ["Automóvil", "Motocicleta", "Transporte público", "Bicicleta", "Caminata", "Otro"]
    )
    perfil["viajes_semana"] = st.number_input("Desplazamientos por semana", min_value=0, max_value=100, value=10)
    perfil["km_semana"] = st.number_input("Kilómetros aproximados por semana", min_value=0, max_value=10000, value=100)
    perfil["incidentes_viales"] = st.number_input("Incidentes viales anteriores", min_value=0, max_value=100, value=0)

if autorizaciones["Seguridad laboral"]:
    st.subheader("4. Seguridad laboral")
    perfil["horas_semana"] = st.number_input("Horas laborales por semana", min_value=0, max_value=120, value=40)
    perfil["exposicion_laboral"] = st.selectbox("Exposición a peligros laborales", ["Baja", "Media", "Alta", "Desconocida"])
    perfil["incidentes_laborales"] = st.number_input("Incidentes laborales anteriores", min_value=0, max_value=100, value=0)

if autorizaciones["Riesgos ambientales"]:
    st.subheader("5. Entorno")
    perfil["region"] = st.text_input("Región aproximada (sin dirección exacta)", value="Región ficticia")
    perfil["inundacion"] = st.selectbox("Exposición conocida a inundación", ["Desconocida", "Sí", "No"])
    perfil["deslizamiento"] = st.selectbox("Exposición conocida a deslizamiento", ["Desconocida", "Sí", "No"])

if autorizaciones["Estabilidad financiera"]:
    st.subheader("6. Situación financiera ficticia")
    perfil["ingresos"] = st.number_input("Ingresos mensuales (unidad monetaria ficticia)", min_value=0, value=1000)
    perfil["gastos"] = st.number_input("Gastos mensuales (misma unidad)", min_value=0, value=700)
    perfil["ahorro_emergencia"] = st.number_input("Meses cubiertos por ahorro de emergencia", min_value=0.0, max_value=120.0, value=2.0, step=0.5)

st.divider()
if st.button("Evaluar categorías autorizadas", type="primary"):
    resultados = evaluar_perfil(perfil, autorizaciones)
    st.subheader("Resultado del análisis de cobertura")
    for resultado in resultados:
        with st.expander(f"{resultado['categoria']} — {resultado['estado']}", expanded=True):
            st.write(resultado["descripcion"])
            if resultado["faltantes"]:
                st.write("Datos faltantes: " + ", ".join(resultado["faltantes"]))
            for indicador in resultado["indicadores"]:
                st.write("• " + indicador)
            if resultado["estado"] == "Datos completos; modelo pendiente":
                st.info("Datos descriptivos disponibles. No hay un modelo predictivo validado para esta categoría.")
    st.caption("Los resultados se calculan en esta sesión. Esta aplicación no implementa una base de datos de perfiles.")

    st.divider()
    st.subheader("Simulación de eventos futuros — PRISMA AI v0.6")
    st.error(
        "ATENCIÓN: los porcentajes siguientes se calculan con tasas base y "
        "multiplicadores inventados para una demostración educativa. NO son "
        "predicciones reales ni sirven para evaluar o asegurar personas."
    )
    meses = {"12 meses": 12, "3 años": 36, "5 años": 60}[horizonte]
    simulaciones = simular_riesgos(perfil, meses, autorizaciones)
    if simulaciones:
        for simulacion in simulaciones:
            st.markdown(f"### {simulacion['evento']}")
            st.metric("Porcentaje hipotético del escenario", f"{simulacion['porcentaje']:.2f} %")
            st.progress(min(simulacion["porcentaje"] / 100, 1.0))
            st.caption("Factores usados: " + " | ".join(simulacion["factores"]))
        st.caption(
            "Método: P(≥1 evento) = 1 − exp(−tasa hipotética × meses/12). "
            "Las tasas no proceden de registros reales y no han sido validadas."
        )
    else:
        st.info("Autoriza Movilidad o Seguridad laboral para visualizar simulaciones.")

    st.subheader("Orientación general sobre coberturas")
    considerar, revisar = orientacion_coberturas(perfil, autorizaciones)
    st.markdown("**Coberturas que podría ser útil consultar con una aseguradora:**")
    for item in considerar:
        st.write("• " + item)
    if not considerar:
        st.write("No hay categorías de exposición autorizadas para orientar la consulta.")
    st.markdown("**Coberturas o complementos cuya pertinencia conviene revisar:**")
    for item in revisar:
        st.write("• " + item)
    st.info(
        "Este módulo NO determina qué cobertura debe negarse o excluirse a una persona. "
        "La contratación, exclusiones y condiciones dependen de la póliza, la normativa "
        "aplicable y una evaluación profesional individual."
    )

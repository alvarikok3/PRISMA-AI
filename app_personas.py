"""PRISMA AI v0.5 — evaluación personal exploratoria.

No se calculan probabilidades de accidentes, salud, crédito o seguros.
"""
import streamlit as st
from src.personas.evaluador import CATEGORIAS, evaluar_perfil

st.set_page_config(page_title="PRISMA AI | Personas", page_icon="🧭", layout="wide")
st.title("PRISMA AI — Evaluación integral de riesgos personales")
st.warning(
    "Prototipo educativo: identifica exposiciones y suficiencia de datos. "
    "No predice acontecimientos reales ni debe usarse para decisiones sobre seguros, "
    "empleo, crédito o salud. No introduzcas datos reales sensibles."
)

st.subheader("1. Perfil general (utiliza datos ficticios)")
edad = st.number_input("Edad (años)", min_value=18, max_value=120, value=35)
ocupacion = st.selectbox(
    "Ocupación", ["Oficina", "Salud", "Conducción", "Industria", "Deporte", "Otra"]
)
horizonte = st.selectbox("Horizonte de análisis futuro", ["12 meses", "3 años", "5 años"])
st.caption("El horizonte se registra como objetivo de diseño; todavía no existe un modelo calibrado para ese plazo.")

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

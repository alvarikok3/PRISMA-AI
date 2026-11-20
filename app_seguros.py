"""PRISMA AI v0.8 — comparador educativo de seguros de vida."""
import pandas as pd
import streamlit as st
from src.seguros.vida import necesidad_proteccion, revisar_coberturas, comparar_polizas

st.set_page_config(page_title="PRISMA AI | Seguros de vida", page_icon="🛡️", layout="wide")
st.title("PRISMA AI v0.8 — Comparador de seguros de vida")
st.warning(
    "Herramienta de planificación financiera y comparación de pólizas, NO de "
    "suscripción o elegibilidad. No uses diagnósticos médicos, causas probables "
    "de muerte ni datos sensibles para rechazar o excluir personas. "
    "Utiliza cifras ficticias en esta demostración."
)
st.subheader("1. Necesidades de protección")
moneda = st.selectbox("Moneda de comparación", ["CRC", "USD"])
a, b = st.columns(2)
with a:
    ingreso = st.number_input("Ingreso mensual ficticio", min_value=0.0, value=800000.0, step=10000.0)
    dependientes = st.number_input("Número de dependientes económicos", min_value=0, max_value=30, value=2)
    deudas = st.number_input("Deudas pendientes", min_value=0.0, value=12000000.0, step=100000.0)
    gastos_finales = st.number_input("Gastos finales estimados", min_value=0.0, value=2000000.0, step=100000.0)
with b:
    porcentaje = st.slider("Porcentaje de ingresos que se desea reemplazar", 0, 100, 70, 5)
    plazo = st.slider("Años de protección deseados", 1, 40, 15)
    ahorros = st.number_input("Ahorros disponibles para beneficiarios", min_value=0.0, value=3000000.0, step=100000.0)
    existente = st.number_input("Cobertura de vida existente", min_value=0.0, value=0.0, step=100000.0)

necesidad = necesidad_proteccion(ingreso, porcentaje / 100, plazo, deudas, gastos_finales, ahorros, existente)
st.subheader("2. Resultado financiero")
c1, c2, c3 = st.columns(3)
c1.metric("Reemplazo de ingresos", f"{moneda} {necesidad['reemplazo_ingresos']:,.0f}")
c2.metric("Necesidad total bruta", f"{moneda} {necesidad['objetivo_bruto']:,.0f}")
c3.metric("Brecha estimada de cobertura", f"{moneda} {necesidad['brecha_cobertura']:,.0f}")
st.caption(
    "Método simplificado: ingreso mensual × 12 × porcentaje × años + deudas "
    "+ gastos finales − ahorros − cobertura existente. No incluye inflación, "
    "rendimientos, impuestos ni cambios de circunstancias."
)
considerar, revisar = revisar_coberturas(dependientes, deudas, existente, plazo, necesidad)
st.subheader("3. Orientación de coberturas")
st.markdown("**Coberturas que conviene cotizar o considerar**")
for item in considerar:
    st.write("• " + item)
st.markdown("**Coberturas cuyo valor o duplicidad conviene revisar**")
for item in revisar:
    st.write("• " + item)
st.info(
    "Revisar o no contratar un producto innecesario no significa negar cobertura "
    "a una persona. La aseguradora debe evaluar las solicitudes según las "
    "condiciones contractuales y la normativa aplicable."
)

st.subheader("4. Comparación de aseguradoras y pólizas")
st.caption(
    "Ingresa cotizaciones reales o ficticias de la MISMA moneda. "
    "PRISMA AI no consulta tarifas en tiempo real ni verifica condiciones de pólizas."
)
if "ofertas_vida" not in st.session_state:
    st.session_state.ofertas_vida = pd.DataFrame([
        {"aseguradora": "Aseguradora A (ejemplo)", "poliza": "Vida temporal",
         "monto": 100000000.0, "prima_mensual": 18000.0,
         "plazo_anios": 15, "exclusiones": "Ver contrato"},
        {"aseguradora": "Aseguradora B (ejemplo)", "poliza": "Vida temporal",
         "monto": 75000000.0, "prima_mensual": 16000.0,
         "plazo_anios": 10, "exclusiones": "Ver contrato"},
    ])
ofertas = st.data_editor(st.session_state.ofertas_vida, num_rows="dynamic", hide_index=True)
if st.button("Comparar pólizas", type="primary"):
    try:
        registros = comparar_polizas(ofertas.to_dict("records"), necesidad["brecha_cobertura"], plazo)
        if registros:
            tabla = pd.DataFrame(registros)
            st.dataframe(tabla, use_container_width=True, hide_index=True)
            st.download_button(
                "Descargar comparación CSV",
                data=tabla.to_csv(index=False).encode("utf-8-sig"),
                file_name="prisma_comparacion_seguros.csv",
                mime="text/csv",
            )
        else:
            st.info("Agrega al menos una póliza para comparar.")
    except (ValueError, TypeError, KeyError) as error:
        st.error(f"Revisa los datos de las cotizaciones: {error}")
st.caption(
    "Los ejemplos A y B son inventados y no corresponden a aseguradoras reales. "
    "Los precios no son cotizaciones ni estimaciones de prima individual."
)

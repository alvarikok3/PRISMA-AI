"""PRISMA AI 1.0: flujo integral de perfil ficticio a necesidades de protección.

Sin almacenamiento, sin diagnóstico ni suscripción de seguros automatizada.
"""
from datetime import date
from html import escape

import pandas as pd
import streamlit as st

from src.personas.motor_predictivo import simular_riesgos
from src.salud.catalogo import EVALUACIONES, revisar_disponibilidad
from src.seguros.integral import CATALOGO, analizar_coberturas
from src.seguros.vida import comparar_polizas, necesidad_proteccion

st.set_page_config(page_title="PRISMA AI | Plataforma integral", page_icon="🛡️", layout="wide")
st.title("PRISMA AI 1.0 — Riesgos, consecuencias y protección")
st.caption("Perfil → identificación de riesgos → consecuencias → protección → comparación de seguros")
st.error(
    "PROTOTIPO DE INVESTIGACIÓN: usa exclusivamente perfiles ficticios. "
    "Los porcentajes de accidentes se basan en tasas INVENTADAS y no son predicciones reales. "
    "No existen modelos clínicos validados integrados ni estimaciones de cáncer o mortalidad. "
    "No sirve para decisiones médicas, tarificación, rechazo ni exclusión de seguros."
)
confirmado = st.checkbox("Confirmo que utilizaré únicamente información ficticia.", value=False)
if not confirmado:
    st.info("Activa la confirmación para acceder al formulario.")
    st.stop()

with st.form("perfil_integral"):
    st.header("1. Perfil general y entorno")
    a, b, c = st.columns(3)
    with a:
        alias = st.text_input("Alias ficticio (no nombres reales)", "Perfil de ejemplo")
        edad = st.number_input("Edad (años)", min_value=18, max_value=120, value=35)
        ocupacion = st.selectbox("Ocupación", ["Oficina", "Salud", "Conducción", "Industria", "Deporte", "Otra"])
        trabaja = st.checkbox("Actualmente trabaja", value=True)
    with b:
        dependientes = st.number_input("Dependientes económicos", min_value=0, max_value=30, value=2)
        vivienda = st.checkbox("Propietario de vivienda")
        inundacion = st.selectbox("Exposición ambiental declarada", ["No evaluada", "Baja", "Media", "Alta"])
        viajes = st.number_input("Viajes fuera de la región por año", min_value=0, max_value=100, value=1)
    with c:
        horas = st.number_input("Horas laborales por semana", min_value=0, max_value=120, value=40)
        exposicion = st.selectbox("Exposición laboral", ["Baja", "Media", "Alta", "Desconocida"])
        incidentes_laborales = st.number_input("Incidentes laborales anteriores", min_value=0, max_value=100, value=0)
        proteccion_laboral = st.selectbox("Protección por riesgos del trabajo", ["No informado", "Sí", "No"])

    st.header("2. Movilidad y actividades")
    a, b, c = st.columns(3)
    with a:
        transporte = st.selectbox("Transporte principal", ["Automóvil", "Motocicleta", "Transporte público", "Bicicleta", "Caminata", "Otro"])
        conduce = st.checkbox("Conduce o posee vehículo", value=True)
    with b:
        km = st.number_input("Kilómetros por semana", min_value=0, max_value=10000, value=100)
        trayectos = st.number_input("Desplazamientos semanales", min_value=0, max_value=100, value=10)
    with c:
        incidentes_viales = st.number_input("Incidentes viales anteriores", min_value=0, max_value=100, value=0)
        actividad = st.selectbox("Actividad recreativa", ["Habitual", "Deporte regular", "Actividad de mayor exposición", "No informado"])

    st.header("3. Economía, familia y protección existente")
    moneda = st.selectbox("Moneda de todos los montos", ["CRC", "USD"])
    a, b, c = st.columns(3)
    with a:
        ingreso = st.number_input("Ingreso mensual", min_value=0.0, value=450000.0, step=10000.0)
        gastos = st.number_input("Gastos mensuales del hogar", min_value=0.0, value=350000.0, step=10000.0)
        deudas = st.number_input("Deudas pendientes", min_value=0.0, value=3000000.0, step=100000.0)
    with b:
        ahorros = st.number_input("Ahorros disponibles", min_value=0.0, value=1000000.0, step=100000.0)
        gastos_finales = st.number_input("Gastos finales estimados", min_value=0.0, value=4000000.0, step=100000.0)
        cobertura_vida = st.number_input("Suma asegurada de vida existente", min_value=0.0, value=0.0, step=100000.0)
    with c:
        porcentaje = st.slider("Porcentaje de ingreso a reemplazar", 0, 100, 70, 5)
        plazo = st.slider("Años de protección familiar", 1, 40, 15)
        cobertura_medica = st.checkbox("Dispone de protección médica", value=True)
        vigentes = set(st.multiselect("Otras coberturas ya contratadas", list(CATALOGO)))

    st.header("4. Salud: categorías opcionales y datos clínicos")
    st.caption("Esta sección es opcional y solo verifica disponibilidad de datos ficticios. "
               "No predice diagnósticos, cáncer, mortalidad ni determina elegibilidad para seguros.")
    revisar_salud = st.checkbox("Autorizar revisión descriptiva de categorías clínicas ficticias")
    categorias = st.multiselect(
        "Categorías de salud", list(EVALUACIONES),
        default=["Cardiovascular (infarto/ictus)", "Diabetes tipo 2", "Cáncer de pulmón"],
        disabled=not revisar_salud,
    )
    datos_clinicos = {"edad": edad}
    if revisar_salud:
        campos = sorted({campo for nombre in categorias for campo in EVALUACIONES[nombre].campos} - {"edad"})
        numericos = {
            "presion_sistolica": (60.0, 260.0, 120.0),
            "colesterol_total": (50.0, 500.0, 190.0),
            "hdl": (10.0, 150.0, 50.0),
            "imc": (10.0, 80.0, 25.0),
            "hba1c": (3.0, 20.0, 5.5),
            "creatinina": (0.1, 20.0, 0.9),
            "albuminuria": (0.0, 10000.0, 10.0),
            "paquetes_anio": (0.0, 150.0, 0.0),
        }
        opciones = {
            "tabaquismo": ["No informado", "Nunca", "Anterior", "Actual"],
            "actividad_fisica": ["No informado", "Regular", "Insuficiente"],
            "exposicion_uv": ["No informado", "Baja", "Media", "Alta"],
            "consumo_alcohol": ["No informado", "No consume", "Ocasional", "Frecuente"],
            "estado_vph": ["No informado", "Positivo", "Negativo", "No aplica"],
            "tamizaje_cervical": ["No informado", "Al día", "Pendiente", "No aplica"],
        }
        cols = st.columns(3)
        for i, campo in enumerate(campos):
            etiqueta = campo.replace("_", " ").capitalize()
            with cols[i % 3]:
                if campo in numericos:
                    disponible = st.checkbox("Dato disponible: " + etiqueta, key="disp_" + campo)
                    if disponible:
                        minimo, maximo, valor = numericos[campo]
                        datos_clinicos[campo] = st.number_input(
                            etiqueta, min_value=minimo, max_value=maximo,
                            value=valor, key="clin_" + campo,
                        )
                    else:
                        datos_clinicos[campo] = None
                else:
                    datos_clinicos[campo] = st.selectbox(
                        etiqueta, opciones.get(campo, ["No informado", "Sí", "No", "No aplica"]),
                        key="clin_" + campo,
                    )
    st.header("5. Autorizaciones y horizonte de simulación")
    col1, col2, col3 = st.columns(3)
    with col1:
        autor_laboral = st.checkbox("Simular incidentes laborales (hipotético)", value=True)
    with col2:
        autor_movilidad = st.checkbox("Simular incidentes viales (hipotético)", value=True)
    with col3:
        horizonte = st.selectbox("Horizonte de escenarios", [12, 36, 60], format_func=lambda x: f"{x // 12} año(s)")
    generar = st.form_submit_button("Generar informe integral", type="primary")

if not generar:
    st.info("Completa el perfil ficticio y pulsa «Generar informe integral».")
    st.stop()

perfil = {
    "ocupacion": ocupacion, "horas_semana": horas,
    "exposicion_laboral": exposicion, "incidentes_laborales": incidentes_laborales,
    "transporte": transporte, "km_semana": km,
    "viajes_semana": trayectos, "incidentes_viales": incidentes_viales,
}
autorizaciones = {"Seguridad laboral": autor_laboral, "Movilidad": autor_movilidad}
simulaciones = simular_riesgos(perfil, horizonte, autorizaciones)
necesidad = necesidad_proteccion(ingreso, porcentaje / 100, plazo, deudas, gastos_finales, ahorros, cobertura_vida)
meses_reserva = ahorros / gastos if gastos > 0 else None
contexto = {
    "dependientes": dependientes, "deudas": deudas, "viajes_anuales": viajes,
    "movilidad": trayectos > 0, "exposicion_laboral": exposicion,
    "trabaja": trabaja, "meses_emergencia": meses_reserva if meses_reserva is not None else 999,
    "cobertura_medica": cobertura_medica, "conduce": conduce,
    "vivienda_propietario": vivienda,
}
matriz = analizar_coberturas(contexto, vigentes)
evaluaciones = revisar_disponibilidad(datos_clinicos, categorias) if revisar_salud else []

st.divider()
st.header("INFORME INTEGRAL — " + alias)
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Riesgos y prevención", "Consecuencias financieras", "Salud", "Protección y seguros", "Informe exportable"
])
with tab1:
    st.subheader("Escenarios de incidentes")
    st.error("Tasas hipotéticas inventadas: los porcentajes NO son probabilidades reales ni predicciones validadas.")
    if simulaciones:
        for item in simulaciones:
            st.metric(item["categoria"] + f" · {horizonte // 12} año(s)", f"{item['porcentaje']:.2f} %")
            st.progress(item["porcentaje"] / 100)
            st.caption(item["evento"] + " | " + "; ".join(item["factores"]))
    else:
        st.info("No se autorizaron simulaciones de incidentes.")
    st.subheader("Riesgos adicionales identificados descriptivamente")
    if inundacion == "No evaluada":
        st.write("Entorno: falta verificar exposición a inundaciones y otros peligros mediante fuentes geográficas.")
    else:
        st.write(f"Entorno: exposición declarada {inundacion}; no se ha contrastado con mapas oficiales.")
    st.write(f"Actividad recreativa declarada: {actividad}. No existe un modelo de accidentes deportivos integrado.")
    st.write(f"Protección laboral declarada: {proteccion_laboral}. Verificar obligaciones y cobertura aplicable.")
    st.subheader("Medidas preventivas generales")
    st.write("• Revisar condiciones de seguridad en el trabajo y reportar incidentes.")
    st.write("• Mantener medidas de seguridad vial y mantenimiento del transporte.")
    st.write("• Consultar mapas oficiales de amenazas y un plan familiar de emergencia.")
    st.write("• Actualizar periódicamente el perfil y las coberturas existentes.")

with tab2:
    st.subheader("Necesidad de protección ante fallecimiento")
    a, b, c = st.columns(3)
    a.metric("Reemplazo de ingresos", f"{moneda} {necesidad['reemplazo_ingresos']:,.0f}")
    b.metric("Objetivo bruto", f"{moneda} {necesidad['objetivo_bruto']:,.0f}")
    c.metric("Brecha de protección", f"{moneda} {necesidad['brecha_cobertura']:,.0f}")
    st.caption("Ingreso × 12 × porcentaje de reemplazo × años + deudas + gastos finales − ahorros − cobertura de vida existente. "
               "Estimación simplificada, sin inflación, rendimiento, impuestos ni prestaciones.")
    st.subheader("Incapacidad temporal: simulación de consecuencias, NO probabilidad")
    meses = st.slider("Meses sin ingreso laboral", 1, 24, 6, key="meses_incapacidad")
    subsidio = st.number_input("Prestaciones u otros ingresos mensuales durante incapacidad", min_value=0.0, value=0.0, step=10000.0)
    ingreso_perdido = max(0.0, ingreso - subsidio) * meses
    gastos_descubiertos = max(0.0, (gastos - subsidio) * meses - ahorros)
    x, y, z = st.columns(3)
    x.metric("Ingreso no percibido", f"{moneda} {ingreso_perdido:,.0f}")
    y.metric("Gastos sin cubrir tras ahorros", f"{moneda} {gastos_descubiertos:,.0f}")
    z.metric("Meses de reserva", f"{meses_reserva:.1f}" if meses_reserva is not None else "No calculable")
    st.caption("Escenario estático; no incluye impuestos, inflación, gastos médicos adicionales ni variaciones futuras.")
    st.subheader("Horizontes de protección familiar")
    escenarios = []
    for anios in (1, 5, 10, 15, 20, 30):
        n = necesidad_proteccion(ingreso, porcentaje / 100, anios, deudas, gastos_finales, ahorros, cobertura_vida)
        escenarios.append({"Años": anios, "Brecha estimada": n["brecha_cobertura"]})
    st.dataframe(pd.DataFrame(escenarios), hide_index=True, use_container_width=True)

with tab3:
    st.subheader("Disponibilidad de información clínica")
    if not revisar_salud:
        st.info("No se autorizó la revisión clínica.")
    elif not evaluaciones:
        st.info("Selecciona categorías clínicas para revisar sus variables.")
    else:
        for item in evaluaciones:
            with st.expander(item["nombre"] + " — " + item["estado"]):
                st.progress(item["completitud"] / 100)
                st.write(f"Completitud de variables: {item['completitud']} %")
                st.write("Faltantes: " + (", ".join(item["faltantes"]) if item["faltantes"] else "Ninguna"))
                st.info(item["nota"])
                st.write("**Probabilidad clínica: no disponible.**")
    st.warning("La completitud no mide riesgo. No se infiere causa individual de muerte, cáncer ni elegibilidad para seguros.")

with tab4:
    st.subheader("Matriz de coberturas y justificación")
    tabla = pd.DataFrame(matriz)
    st.dataframe(tabla, hide_index=True, use_container_width=True)
    st.download_button("Descargar matriz de coberturas CSV", tabla.to_csv(index=False).encode("utf-8-sig"),
                       "prisma_matriz_coberturas.csv", "text/csv")
    st.caption("«Revisar utilidad» no significa denegar cobertura. Comparar carencias, exclusiones contractuales, "
               "deducibles, topes, renovaciones, beneficiarios y costos.")
    st.subheader("Comparación de cotizaciones de vida")
    st.caption("Introduce ofertas ficticias o cotizaciones verificadas de la misma moneda. No hay tarifas en tiempo real.")
    ofertas = st.data_editor(pd.DataFrame([
        {"aseguradora": "Ejemplo A", "poliza": "Vida temporal", "monto": 20000000.0,
         "prima_mensual": 12000.0, "plazo_anios": 15, "exclusiones": "Consultar contrato"},
        {"aseguradora": "Ejemplo B", "poliza": "Vida temporal", "monto": 15000000.0,
         "prima_mensual": 9000.0, "plazo_anios": 10, "exclusiones": "Consultar contrato"},
    ]), num_rows="dynamic", hide_index=True, key="ofertas_integral")
    try:
        comparacion = comparar_polizas(ofertas.to_dict("records"), necesidad["brecha_cobertura"], plazo)
        st.dataframe(pd.DataFrame(comparacion), hide_index=True, use_container_width=True)
        st.caption("Costo nominal = prima mensual × 12 × años; no compara valor presente ni cambios futuros de prima.")
    except (ValueError, TypeError, KeyError) as error:
        st.error(f"Datos de cotización inválidos: {error}")

with tab5:
    st.subheader("Informe para solicitar asesoría y cotizaciones")
    lineas = [
        "# PRISMA AI — Informe de necesidades de protección",
        f"Fecha: {date.today().isoformat()}",
        f"Perfil ficticio: {alias}",
        "Versión: 1.0 — investigación, no asesoría médica ni suscripción",
        f"Edad: {edad} años | Ocupación: {ocupacion} | Dependientes: {dependientes}",
        f"Horizonte de incidentes: {horizonte // 12} años",
        "## Riesgos evaluados (SIMULACIONES NO VALIDADAS)",
    ]
    for item in simulaciones:
        lineas.append(f"- {item['categoria']}: {item['porcentaje']:.2f}% hipotético; no usar como riesgo real.")
    lineas += [
        "## Consecuencias económicas",
        f"- Brecha financiera estimada de vida: {moneda} {necesidad['brecha_cobertura']:,.0f}",
        f"- Plazo de protección elegido: {plazo} años",
        f"- Ahorros declarados: {moneda} {ahorros:,.0f}",
        "## Coberturas a consultar",
    ]
    for item in matriz:
        lineas.append(f"- {item['cobertura']} — {item['estado']}. {item['justificacion']}")
    lineas += [
        "## Salud",
        f"- Categorías clínicas revisadas: {len(evaluaciones)}. Sin estimaciones médicas de probabilidad.",
        "## Preguntas para la aseguradora",
        "- ¿Cuál es la prima y cómo cambia con el tiempo?",
        "- ¿Cuáles son las exclusiones, carencias, deducibles y topes?",
        "- ¿Qué eventos activan cada beneficio y qué documentos se requieren?",
        "- ¿Cómo se renueva o cancela la póliza? ¿Qué sucede al terminar el plazo?",
        "- ¿Cómo se coordina con seguros existentes y regímenes obligatorios?",
        "## Limitaciones",
        "- Datos ficticios. No introducir datos personales o clínicos reales.",
        "- Los porcentajes de accidentes usan tasas hipotéticas inventadas.",
        "- Sin diagnóstico, pronóstico clínico, mortalidad ni decisiones de elegibilidad.",
        "- Los montos son escenarios financieros simplificados, no ofertas de aseguradoras.",
    ]
    informe = "\n\n".join(lineas)
    st.text_area("Vista previa del informe", informe, height=350)
    st.download_button("Descargar informe Markdown", informe.encode("utf-8"),
                       file_name="prisma_informe_integral.md", mime="text/markdown")
    st.download_button("Descargar informe HTML", (
        "<!doctype html><html lang='es'><meta charset='utf-8'><title>PRISMA AI</title>"
        "<style>body{font-family:Arial;max-width:850px;margin:40px auto;line-height:1.6;}"
        "pre{white-space:pre-wrap;font-family:Arial}</style><h1>PRISMA AI</h1><pre>"
        + escape(informe) + "</pre></html>"
    ).encode("utf-8"), file_name="prisma_informe_integral.html", mime="text/html")
    st.caption("El HTML puede abrirse en el navegador e imprimirse como PDF.")
st.caption("PRISMA AI no almacena expedientes en una base de datos. Los datos permanecen en la sesión de Streamlit; "
           "no uses información identificable en este prototipo ni compartas enlaces de puertos.")

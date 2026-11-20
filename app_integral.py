"""PRISMA AI v0.9 — vista integral de riesgos y protección financiera."""
import pandas as pd
import streamlit as st
from src.personas.motor_predictivo import simular_riesgos
from src.seguros.vida import necesidad_proteccion, comparar_polizas
from src.seguros.integral import CATALOGO, analizar_coberturas

st.set_page_config(page_title="PRISMA AI | Evaluación integral",page_icon="🛡️",layout="wide")
st.title("PRISMA AI v0.9 — Perfil integral y coberturas")
st.warning("Prototipo educativo con perfiles ficticios. Los porcentajes de accidentes son SIMULACIONES con tasas hipotéticas, no predicciones reales. El análisis de coberturas es planificación financiera, no aprobación, denegación ni tarificación de seguros. No introduzcas datos personales reales.")
st.subheader("1. Perfil general y actividad")
c1,c2,c3=st.columns(3)
with c1:
    edad=st.number_input("Edad",18,120,35)
    ocupacion=st.selectbox("Ocupación",["Oficina","Salud","Conducción","Industria","Deporte","Otra"])
    trabaja=st.checkbox("Actualmente trabaja",True)
    horas=st.number_input("Horas laborales por semana",0,120,40)
with c2:
    dependientes=st.number_input("Dependientes económicos",0,30,2)
    exposicion=st.selectbox("Exposición laboral",["Baja","Media","Alta","Desconocida"])
    incidentes_laborales=st.number_input("Incidentes laborales anteriores",0,100,0)
    viajes=st.number_input("Viajes fuera de la región por año",0,100,1)
with c3:
    transporte=st.selectbox("Transporte habitual",["Automóvil","Motocicleta","Transporte público","Bicicleta","Caminata","Otro"])
    conduce=st.checkbox("Conduce o tiene vehículo",True)
    km=st.number_input("Kilómetros recorridos por semana",0,10000,100)
    trayectos=st.number_input("Desplazamientos por semana",0,100,10)
    incidentes_viales=st.number_input("Incidentes viales anteriores",0,100,0)

st.subheader("2. Situación económica y patrimonio")
moneda=st.selectbox("Moneda",["CRC","USD"])
a,b,c=st.columns(3)
with a:
    ingreso=st.number_input("Ingreso mensual",min_value=0.0,value=800000.0,step=10000.0)
    deudas=st.number_input("Deudas pendientes",min_value=0.0,value=12000000.0,step=100000.0)
    ahorros=st.number_input("Ahorros disponibles para beneficiarios",min_value=0.0,value=3000000.0,step=100000.0)
with b:
    gastos=st.number_input("Gastos mensuales del hogar",min_value=0.0,value=500000.0,step=10000.0)
    gastos_finales=st.number_input("Gastos finales estimados",min_value=0.0,value=2000000.0,step=100000.0)
    existente_vida=st.number_input("Suma asegurada de vida existente",min_value=0.0,value=0.0,step=100000.0)
with c:
    propietario=st.checkbox("Propietario de vivienda",False)
    cobertura_medica=st.checkbox("Cuenta con protección médica",True)
    reemplazo=st.slider("Porcentaje de ingresos a reemplazar",0,100,70,5)
    plazo=st.slider("Años de protección deseados",1,40,15)
meses_emergencia=ahorros/gastos if gastos>0 else 0
st.caption(f"Reserva aproximada para gastos del hogar: {meses_emergencia:.1f} meses. No equivale a liquidez comprobada.")

st.subheader("3. Coberturas que ya posee")
vigentes=set(st.multiselect("Selecciona coberturas existentes (si se conocen)",list(CATALOGO)))
st.subheader("4. Evaluación automática por categoría")
autorizacion_laboral=st.checkbox("Autorizar simulación de seguridad laboral",True)
autorizacion_movilidad=st.checkbox("Autorizar simulación de movilidad",True)
st.caption("Salud: el módulo clínico separado permite revisar variables faltantes. No se utilizan diagnósticos para excluir o cotizar pólizas.")
if st.button("Generar evaluación integral",type="primary"):
    perfil={
        "edad":edad,"ocupacion":ocupacion,"horas_semana":horas,
        "exposicion_laboral":exposicion,"incidentes_laborales":incidentes_laborales,
        "transporte":transporte,"km_semana":km,"viajes_semana":trayectos,
        "incidentes_viales":incidentes_viales,
    }
    autorizaciones={"Seguridad laboral":autorizacion_laboral,"Movilidad":autorizacion_movilidad}
    st.subheader("5. Riesgos operativos personales (escenarios hipotéticos)")
    for item in simular_riesgos(perfil,12,autorizaciones):
        st.metric(item["categoria"]+" — 12 meses",f"{item['porcentaje']:.2f} %")
        st.progress(item["porcentaje"]/100)
        st.caption(item["evento"]+" · "+"; ".join(item["factores"]))
    st.error("Los porcentajes anteriores NO representan probabilidad real de accidentes y NO se utilizan para recomendar ni excluir pólizas.")
    necesidad=necesidad_proteccion(ingreso,reemplazo/100,plazo,deudas,gastos_finales,ahorros,existente_vida)
    st.subheader("6. Necesidad financiera de vida")
    x,y,z=st.columns(3)
    x.metric("Reemplazo de ingresos",f"{moneda} {necesidad['reemplazo_ingresos']:,.0f}")
    y.metric("Necesidad bruta",f"{moneda} {necesidad['objetivo_bruto']:,.0f}")
    z.metric("Brecha estimada",f"{moneda} {necesidad['brecha_cobertura']:,.0f}")
    st.caption(f"Plazo: {plazo} años. Cálculo simplificado sin inflación, rendimiento ni impuestos.")
    st.subheader("7. Matriz integral de coberturas")
    p={"dependientes":dependientes,"deudas":deudas,"viajes_anuales":viajes,
       "movilidad":trayectos>0,"exposicion_laboral":exposicion,"trabaja":trabaja,
       "meses_emergencia":meses_emergencia,"cobertura_medica":cobertura_medica,
       "conduce":conduce,"vivienda_propietario":propietario}
    matriz=analizar_coberturas(p,vigentes)
    tabla=pd.DataFrame(matriz)
    st.dataframe(tabla,hide_index=True,use_container_width=True)
    st.download_button("Descargar informe de coberturas (CSV)",tabla.to_csv(index=False).encode("utf-8-sig"),
                       file_name="prisma_coberturas_integrales.csv",mime="text/csv")
    st.info("Las coberturas clasificadas como 'revisar' NO son exclusiones ni rechazos. Se requiere consultar condiciones y cotizaciones reales.")
    st.subheader("8. Comparar cotizaciones reales o ficticias")
    st.caption("Completa cotizaciones de una misma moneda. Las filas son ejemplos inventados.")
    ofertas=st.data_editor(pd.DataFrame([
      {"aseguradora":"Ejemplo A","poliza":"Vida temporal","monto":100000000.0,"prima_mensual":18000.0,"plazo_anios":15,"exclusiones":"Consultar contrato"},
      {"aseguradora":"Ejemplo B","poliza":"Vida temporal","monto":75000000.0,"prima_mensual":16000.0,"plazo_anios":10,"exclusiones":"Consultar contrato"}
    ]),num_rows="dynamic",hide_index=True,key="cotizaciones")
    try:
        comparacion=comparar_polizas(ofertas.to_dict("records"),necesidad["brecha_cobertura"],plazo)
        st.dataframe(pd.DataFrame(comparacion),hide_index=True,use_container_width=True)
    except (ValueError,TypeError,KeyError) as e:
        st.error(f"Corrige las cotizaciones: {e}")
    st.caption("La aseguradora debe verificar póliza, prima, vigencia y términos; esta aplicación no determina elegibilidad.")

"""Análisis de brechas de protección, sin decisiones de suscripción.

Las reglas relacionan necesidades declaradas con tipos de productos. No usan
datos clínicos para negar, tarifar o condicionar seguros.
"""
CATALOGO = {
 "Vida temporal": "Protección económica a beneficiarios por fallecimiento durante un plazo.",
 "Vida permanente": "Protección de larga duración con condiciones y costos distintos.",
 "Accidentes personales": "Prestaciones contractuales por lesiones accidentales.",
 "Incapacidad temporal": "Sustitución parcial de ingresos durante incapacidad cubierta.",
 "Invalidez permanente": "Capital o renta por invalidez cubierta.",
 "Enfermedades graves": "Pago condicionado a diagnósticos y definiciones de la póliza.",
 "Gastos médicos": "Cobertura de gastos médicos elegibles, límites y red.",
 "Responsabilidad civil": "Protección frente a daños a terceros según contrato.",
 "Seguro vehicular": "Protección para vehículo, ocupantes y daños según póliza.",
 "Riesgos del trabajo": "Cobertura ocupacional aplicable conforme al régimen legal.",
 "Asistencia en viajes": "Asistencia médica, logística y contingencias de viaje.",
 "Protección de vivienda": "Daños a la vivienda por riesgos contratados.",
 "Protección de ingresos": "Prestaciones según condiciones de desempleo o incapacidad.",
}
def analizar_coberturas(p: dict, vigentes: set[str]) -> list[dict]:
    """Clasifica necesidades de revisión; nunca elegibilidad ni exclusiones."""
    filas=[]
    def agregar(nombre, motivo, relevancia):
        if nombre in vigentes:
            estado="Verificar cobertura existente y posibles duplicidades"
        elif relevancia=="considerar":
            estado="Conviene cotizar y comparar"
        elif relevancia=="revisar":
            estado="Revisar utilidad y condiciones"
        else:
            estado="Información insuficiente"
        filas.append({"cobertura":nombre,"estado":estado,"justificacion":motivo,
                     "descripcion":CATALOGO[nombre]})
    dependientes=p["dependientes"]; deuda=p["deudas"]; viajes=p["viajes_anuales"]
    if dependientes or deuda:
        agregar("Vida temporal","Dependientes económicos o deudas pendientes; comparar suma y plazo.", "considerar")
    else:
        agregar("Vida temporal","Sin dependientes ni deudas declarados; confirmar otras obligaciones.", "revisar")
    agregar("Vida permanente","Comparar objetivos patrimoniales y primas a largo plazo; no es sustituto automático de vida temporal.","revisar")
    agregar("Accidentes personales","Comparar protección ante accidentes con pólizas existentes y protección laboral.","considerar" if p["movilidad"] or p["exposicion_laboral"]!="Baja" else "revisar")
    agregar("Incapacidad temporal","Dependencia del ingreso laboral y capacidad de sostener gastos durante una incapacidad.","considerar" if p["trabaja"] and p["meses_emergencia"]<6 else "revisar")
    agregar("Invalidez permanente","Evaluar pérdida prolongada de capacidad de generar ingresos.","considerar" if p["trabaja"] else "revisar")
    agregar("Enfermedades graves","Comparar indemnización, definiciones, carencias y exclusiones; no inferir riesgo clínico individual.","revisar")
    agregar("Gastos médicos","Verificar protección sanitaria existente, deducibles, copagos y redes.","considerar" if not p["cobertura_medica"] else "revisar")
    agregar("Responsabilidad civil","Examinar responsabilidad frente a terceros por actividades y bienes.","considerar" if p["conduce"] or p["vivienda_propietario"] else "revisar")
    agregar("Seguro vehicular","Conduce o posee vehículo: revisar coberturas y obligaciones legales.","considerar" if p["conduce"] else "revisar")
    agregar("Riesgos del trabajo","Comprobar protección obligatoria o régimen correspondiente; evitar duplicidades.","considerar" if p["trabaja"] else "revisar")
    agregar("Asistencia en viajes","Frecuencia de viajes declarada y coberturas de tarjetas o pólizas actuales.","considerar" if viajes>=2 else "revisar")
    agregar("Protección de vivienda","Titularidad y exposición patrimonial; revisar protección contra daños.","considerar" if p["vivienda_propietario"] else "revisar")
    agregar("Protección de ingresos","Comparar periodos de espera, duración de beneficios y exclusiones.","considerar" if p["trabaja"] and p["meses_emergencia"]<3 else "revisar")
    return filas

# PRISMA AI

**Plataforma de Riesgos Inteligentes, Simulación y Modelado Analítico**.

Proyecto de investigación y desarrollo para identificar patrones y estimar riesgos en distintos ámbitos, empezando por riesgos operativos.

## Objetivo inicial

Crear un prototipo reproducible que genere datos **sintéticos** de operaciones empresariales, entrene un modelo de clasificación y evalúe su capacidad de estimar eventos de interrupción operativa.

## Etapas

1. Preparación del entorno Python en GitHub Codespaces.
2. Generación de datos sintéticos y exploración.
3. Entrenamiento de un modelo de referencia y evaluación con datos separados.
4. API y panel web.
5. Explicabilidad, pruebas, documentación y controles de privacidad.

## Principios

- No utilizar información personal, clínica o institucional confidencial.
- Interpretar los resultados como estimaciones, no certezas.
- Evaluar sesgos, calidad de los datos y desempeño antes de cualquier uso real.
- Mantener supervisión humana sobre las decisiones importantes.

## Primeros pasos

Abre este repositorio, selecciona **Code → Codespaces → Create codespace on main** y espera a que se abra el editor en el navegador.

> Estado: configuración inicial. Todavía no existe un modelo predictivo entrenado.


## PRISMA AI 1.0 — aplicación integral

La entrada principal es `app_prisma.py`. Las aplicaciones anteriores
(`app_personas.py`, `app_salud.py`, `app_seguros.py`, `app_integral.py`)
se conservan como prototipos históricos.

### Ejecutar en GitHub Codespaces

```bash
git pull --ff-only origin main
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python -m streamlit run app_prisma.py --server.address 0.0.0.0 --server.port 8501
```

Abrir el puerto 8501 desde la pestaña PORTS del Codespace.

### Flujo

1. Introducir exclusivamente un perfil ficticio (no nombres ni datos clínicos reales).
2. Registrar contexto personal, laboral, movilidad, finanzas y protección existente.
3. Autorizar por separado simulaciones de incidentes y revisión descriptiva de salud.
4. Generar el informe y explorar sus pestañas: riesgos, consecuencias, salud,
   coberturas y exportación.
5. Comparar cotizaciones de una misma moneda; verificar condiciones de cada póliza.

### Limitaciones y protección de datos

- Los porcentajes de incidentes son **simulaciones matemáticas con tasas hipotéticas inventadas**.
  No están calibrados ni validados contra siniestros observados.
- El módulo de salud solo revisa disponibilidad de variables; no diagnostica,
  no estima cáncer ni mortalidad y no calcula elegibilidad para seguros.
- La matriz de seguros identifica necesidades financieras y posibles duplicidades;
  no determina aceptación, rechazo, prima ni exclusiones individuales.
- Los cálculos de protección financiera no consideran inflación, impuestos,
  rendimiento, cambios de ingresos ni todas las prestaciones disponibles.
- No existe almacenamiento persistente de expedientes; los datos ingresados
  pueden permanecer en la sesión mientras esté activa. No usar datos sensibles.
- No se consultan cotizaciones reales automáticamente.
- El informe HTML puede imprimirse a PDF desde el navegador.

### Próximas etapas

Autenticación y seguridad, controles de privacidad y retención, modelos
especializados validados con datos apropiados, calibración, auditoría de sesgos,
validación externa, integración de cotizaciones verificables y reportes PDF
profesionales. Ningún modelo clínico debe usarse para denegar coberturas.

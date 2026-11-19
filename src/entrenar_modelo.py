
# PRISMA AI - Motor predictivo v0.3
# Entrenamiento con datos sinteticos

from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    roc_auc_score,
)

BASE = Path(__file__).resolve().parent.parent
MODELOS = BASE / "models"
MODELOS.mkdir(exist_ok=True)

COLUMNAS = [
    "fallas",
    "retrasos",
    "mantenimiento",
    "incidentes",
]

print("=" * 55)
print("PRISMA AI - ENTRENAMIENTO DE INTELIGENCIA ARTIFICIAL")
print("=" * 55)

# 1. Crear datos ficticios reproducibles
rng = np.random.default_rng(42)
n = 5000

datos = pd.DataFrame({
    "fallas": rng.integers(0, 13, n),
    "retrasos": rng.integers(0, 31, n),
    "mantenimiento": rng.integers(30, 101, n),
    "incidentes": rng.integers(0, 9, n),
})

# 2. Simular eventos de interrupcion operativa
# Esta formula solo genera etiquetas ficticias.
puntaje = (
    -4.0
    + 0.23 * datos["fallas"]
    + 0.09 * datos["retrasos"]
    - 0.025 * (datos["mantenimiento"] - 65)
    + 0.32 * datos["incidentes"]
)

probabilidad = 1 / (1 + np.exp(-puntaje))

datos["interrupcion"] = rng.binomial(
    1, probabilidad
)

print(f"\nRegistros generados: {len(datos)}")
print("\nDistribucion de eventos:")
print(datos["interrupcion"].value_counts())

# 3. Separar entrenamiento y prueba
X = datos[COLUMNAS]
y = datos["interrupcion"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y,
)

# 4. Entrenar el modelo
modelo = RandomForestClassifier(
    n_estimators=200,
    max_depth=8,
    min_samples_leaf=10,
    random_state=42,
    n_jobs=-1,
)

print("\nEntrenando Random Forest...")
modelo.fit(X_train, y_train)

# 5. Evaluar con registros no usados en entrenamiento
predicciones = modelo.predict(X_test)
probabilidades = modelo.predict_proba(X_test)[:, 1]

print("\n--- EVALUACION ---")
print(f"Exactitud: {accuracy_score(y_test, predicciones):.2%}")
print(f"ROC AUC: {roc_auc_score(y_test, probabilidades):.3f}")

print("\nReporte de clasificacion:")
print(classification_report(
    y_test,
    predicciones,
    zero_division=0
))

print("Matriz de confusion:")
print(confusion_matrix(y_test, predicciones))

# 6. Importancia de variables
print("\n--- VARIABLES MAS INFLUYENTES ---")
importancias = sorted(
    zip(COLUMNAS, modelo.feature_importances_),
    key=lambda x: x[1],
    reverse=True,
)

for variable, importancia in importancias:
    print(f"{variable}: {importancia:.2%}")

# 7. Guardar modelo
ruta = MODELOS / "prisma_riesgos_v03.joblib"

joblib.dump({
    "modelo": modelo,
    "columnas": COLUMNAS,
    "version": "0.3.0",
}, ruta)

print(f"\nModelo guardado en: {ruta}")

# 8. Evaluar un nuevo escenario ficticio
nuevo = pd.DataFrame([{
    "fallas": 6,
    "retrasos": 8,
    "mantenimiento": 65,
    "incidentes": 3,
}])

riesgo = modelo.predict_proba(nuevo[COLUMNAS])[0, 1]

print("\n--- NUEVA PREDICCION ---")
print(f"Probabilidad estimada: {riesgo:.2%}")
print("PRISMA AI - Analisis completado")

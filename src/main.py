
from datetime import datetime

def iniciar_prisma():
    print("=" * 50)
    print("PRISMA AI - Plataforma de Analisis de Riesgos")
    print("=" * 50)

    print("Estado: Sistema iniciado correctamente")
    print("Version: 0.1.0")
    print(f"Fecha: {datetime.now():%Y-%m-%d %H:%M:%S}")

    print("\nModulos planificados:")
    print("1. Analisis de datos")
    print("2. Deteccion de patrones")
    print("3. Prediccion de riesgos")
    print("4. Generacion de alertas")

    print("\nPRISMA AI esta listo para comenzar.")


if __name__ == "__main__":
    iniciar_prisma()



# PRISMA AI - Motor de analisis de riesgos
# Version 0.2.0 - Prototipo basado en reglas

def calcular_riesgo(fallas, retrasos, mantenimiento, incidentes):
    if not 0 <= mantenimiento <= 100:
        raise ValueError("El mantenimiento debe estar entre 0 y 100")

    if min(fallas, retrasos, incidentes) < 0:
        raise ValueError("Los valores no pueden ser negativos")

    puntuacion = (
        fallas * 5
        + retrasos * 2
        + (100 - mantenimiento) * 0.3
        + incidentes * 8
    )

    puntuacion = min(100, round(puntuacion, 2))

    if puntuacion >= 70:
        nivel = "ALTO"
        recomendacion = "Requiere revision prioritaria"
    elif puntuacion >= 40:
        nivel = "MODERADO"
        recomendacion = "Reforzar medidas preventivas"
    else:
        nivel = "BAJO"
        recomendacion = "Mantener controles y seguimiento"

    return puntuacion, nivel, recomendacion


def main():
    print("=" * 50)
    print("PRISMA AI - ANALISIS DE RIESGOS")
    print("=" * 50)

    empresa = "Empresa de prueba"

    fallas = 6
    retrasos = 8
    mantenimiento = 65
    incidentes = 3

    puntuacion, nivel, recomendacion = calcular_riesgo(
        fallas, retrasos, mantenimiento, incidentes
    )

    print(f"\nEmpresa: {empresa}")
    print(f"Fallas registradas: {fallas}")
    print(f"Dias de retraso: {retrasos}")
    print(f"Cumplimiento mantenimiento: {mantenimiento}%")
    print(f"Incidentes anteriores: {incidentes}")

    print("\n--- RESULTADOS ---")
    print(f"Indice de riesgo: {puntuacion}/100")
    print(f"Clasificacion: {nivel}")
    print(f"Recomendacion: {recomendacion}")

    print("\nAnalisis completado.")


if __name__ == "__main__":
    main()


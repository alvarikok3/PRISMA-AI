"""Herramientas de análisis de necesidades de seguros de vida.

No realiza suscripción, tarificación actuarial ni decisiones de elegibilidad.
Los montos son estimaciones de planificación financiera, no sumas recomendadas
por una aseguradora.
"""


def necesidad_proteccion(
    ingreso_mensual: float,
    proporcion_reemplazo: float,
    anios: int,
    deudas: float,
    gastos_finales: float,
    ahorros: float,
    cobertura_existente: float,
) -> dict:
    if any(x < 0 for x in (ingreso_mensual, deudas, gastos_finales, ahorros, cobertura_existente)):
        raise ValueError("No se admiten montos negativos")
    if not (0 <= proporcion_reemplazo <= 1) or not (0 <= anios <= 60):
        raise ValueError("Proporción o plazo fuera de rango")
    reemplazo = ingreso_mensual * 12 * proporcion_reemplazo * anios
    objetivo = reemplazo + deudas + gastos_finales
    brecha = max(0, objetivo - ahorros - cobertura_existente)
    return {
        "reemplazo_ingresos": round(reemplazo, 2),
        "objetivo_bruto": round(objetivo, 2),
        "brecha_cobertura": round(brecha, 2),
        "horizonte_anios": anios,
    }


def revisar_coberturas(
    dependientes: int, deuda: float, cobertura_existente: float,
    plazo: int, necesidad: dict,
) -> tuple[list[str], list[str]]:
    considerar = []
    revisar = []
    if dependientes > 0 or deuda > 0:
        considerar.append(
            f"Seguro de vida temporal por aproximadamente {plazo} años: comparar "
            "suma asegurada, primas, renovación y exclusiones contractuales."
        )
    else:
        revisar.append(
            "Seguro de vida elevado por reemplazo de ingresos: comprobar si hay "
            "beneficiarios u obligaciones que realmente lo justifiquen."
        )
    if necesidad["brecha_cobertura"] > 0:
        considerar.append(
            "Evaluar protección adicional para la brecha financiera calculada; "
            "no es una oferta ni una suma asegurable garantizada."
        )
    else:
        revisar.append(
            "Cobertura adicional de fallecimiento: verificar duplicidades y "
            "si los recursos existentes ya cubren las necesidades declaradas."
        )
    if cobertura_existente > 0:
        revisar.append(
            "Pólizas duplicadas: contrastar beneficiarios, plazos, exclusiones "
            "y sumas aseguradas antes de comprar complementos."
        )
    revisar.append(
        "Riders o adicionales (accidental, exoneración de primas, enfermedades graves): "
        "revisar su utilidad, límites, exclusiones y costo; no excluir por salud."
    )
    return considerar, revisar


def comparar_polizas(polizas: list[dict], brecha: float, plazo: int) -> list[dict]:
    """Compara ofertas introducidas manualmente, sin decidir elegibilidad."""
    resultados = []
    for p in polizas:
        monto = float(p["monto"])
        prima = float(p["prima_mensual"])
        anios = int(p["plazo_anios"])
        if monto < 0 or prima < 0 or anios < 0:
            raise ValueError("Valores de póliza negativos")
        resultados.append({
            "aseguradora": str(p["aseguradora"]),
            "poliza": str(p["poliza"]),
            "suma_asegurada": monto,
            "prima_mensual": prima,
            "costo_nominal_plazo": round(prima * 12 * anios, 2),
            "cubre_brecha_estimativa": monto >= brecha,
            "cubre_plazo_deseado": anios >= plazo,
            "exclusiones_declaradas": str(p.get("exclusiones", "No informado")),
        })
    return resultados

import unittest

from src.personas.evaluador import evaluar_perfil


class EvaluadorPersonasTest(unittest.TestCase):
    def test_sin_autorizacion(self):
        resultados = evaluar_perfil({}, {})
        self.assertTrue(all(r["estado"] == "Sin autorización" for r in resultados))

    def test_faltantes(self):
        resultados = evaluar_perfil({}, {"Movilidad": True})
        movilidad = next(r for r in resultados if r["categoria"] == "Movilidad")
        self.assertIn("km_semana", movilidad["faltantes"])
        self.assertIsNone(movilidad["prediccion"])

    def test_datos_completos_sin_prediccion(self):
        perfil = {
            "transporte": "Automóvil", "viajes_semana": 10,
            "km_semana": 100, "incidentes_viales": 0,
        }
        resultados = evaluar_perfil(perfil, {"Movilidad": True})
        movilidad = next(r for r in resultados if r["categoria"] == "Movilidad")
        self.assertEqual(movilidad["estado"], "Datos completos; modelo pendiente")
        self.assertIsNone(movilidad["prediccion"])


if __name__ == "__main__":
    unittest.main()

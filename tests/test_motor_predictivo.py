import unittest
from src.personas.motor_predictivo import (
    probabilidad_evento, simular_riesgos, orientacion_coberturas,
)


class MotorPredictivoTest(unittest.TestCase):
    def setUp(self):
        self.perfil = {
            "ocupacion": "Oficina", "horas_semana": 40,
            "exposicion_laboral": "Baja", "incidentes_laborales": 0,
            "transporte": "Automóvil", "km_semana": 100,
            "viajes_semana": 10, "incidentes_viales": 0,
        }

    def test_probabilidad_limites(self):
        self.assertEqual(probabilidad_evento(0, 12), 0)
        self.assertGreater(probabilidad_evento(0.03, 24), probabilidad_evento(0.03, 12))

    def test_solo_categorias_autorizadas(self):
        r = simular_riesgos(self.perfil, 12, {"Movilidad": True})
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0]["categoria"], "Movilidad")
        self.assertGreater(r[0]["porcentaje"], 0)

    def test_exposicion_cambia_escenario(self):
        base = simular_riesgos(self.perfil, 12, {"Seguridad laboral": True})[0]["porcentaje"]
        self.perfil["exposicion_laboral"] = "Alta"
        alto = simular_riesgos(self.perfil, 12, {"Seguridad laboral": True})[0]["porcentaje"]
        self.assertGreater(alto, base)

    def test_no_exclusion_de_cobertura(self):
        _, revisar = orientacion_coberturas(self.perfil, {"Movilidad": True})
        self.assertTrue(revisar)
        self.assertFalse(any("denegar" in x for x in revisar))


if __name__ == "__main__":
    unittest.main()

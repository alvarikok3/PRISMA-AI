import unittest
from src.seguros.vida import necesidad_proteccion
from src.seguros.integral import analizar_coberturas
from src.salud.catalogo import revisar_disponibilidad

class PlataformaIntegralTest(unittest.TestCase):
    def test_caso_financiero(self):
        n = necesidad_proteccion(450000, .25, 5, 3000000, 4000000, 1000000, 0)
        self.assertEqual(n["reemplazo_ingresos"], 6750000)
        self.assertEqual(n["objetivo_bruto"], 13750000)
        self.assertEqual(n["brecha_cobertura"], 12750000)

    def test_clinico_no_predice(self):
        r = revisar_disponibilidad({"edad":35}, ["Cáncer colorrectal"])
        self.assertIsNone(r[0]["probabilidad"])

    def test_coberturas_no_excluyen(self):
        p = {"dependientes": 2, "deudas": 100, "viajes_anuales": 1,
             "movilidad": True, "exposicion_laboral": "Baja", "trabaja": True,
             "meses_emergencia": 2, "cobertura_medica": True, "conduce": True,
             "vivienda_propietario": False}
        r = analizar_coberturas(p, set())
        self.assertGreaterEqual(len(r), 12)
        self.assertTrue(all("denegar" not in x["estado"].lower() for x in r))

if __name__ == "__main__":
    unittest.main()

import unittest
from src.seguros.vida import necesidad_proteccion, comparar_polizas, revisar_coberturas

class SegurosVidaTest(unittest.TestCase):
    def test_brecha(self):
        r = necesidad_proteccion(1000, 0.5, 10, 1000, 500, 1000, 500)
        self.assertEqual(r["brecha_cobertura"], 60000)

    def test_sin_brecha_negativa(self):
        r = necesidad_proteccion(0, 0, 1, 0, 0, 500, 100)
        self.assertEqual(r["brecha_cobertura"], 0)

    def test_comparar(self):
        r = comparar_polizas([{"aseguradora": "Ejemplo", "poliza": "Vida",
            "monto": 100000, "prima_mensual": 100, "plazo_anios": 10}], 90000, 10)
        self.assertTrue(r[0]["cubre_brecha_estimativa"])
        self.assertEqual(r[0]["costo_nominal_plazo"], 12000)

    def test_orientacion_no_denegacion(self):
        n = necesidad_proteccion(1000, 0.5, 10, 0, 0, 0, 0)
        considerar, revisar = revisar_coberturas(2, 0, 0, 10, n)
        self.assertTrue(considerar)
        self.assertTrue(revisar)

if __name__ == "__main__":
    unittest.main()

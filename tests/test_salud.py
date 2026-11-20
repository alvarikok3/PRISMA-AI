import unittest
from src.salud.catalogo import EVALUACIONES, revisar_disponibilidad

class SaludTest(unittest.TestCase):
    def test_categorias(self):
        self.assertIn("Cáncer de pulmón", EVALUACIONES)
        self.assertIn("Mortalidad por causas específicas", EVALUACIONES)

    def test_no_prediccion(self):
        r = revisar_disponibilidad({"edad": 35}, ["Cáncer de pulmón"])
        self.assertIsNone(r[0]["probabilidad"])
        self.assertIn("paquetes_anio", r[0]["faltantes"])

    def test_sin_categorias(self):
        self.assertEqual(revisar_disponibilidad({}, []), [])

if __name__ == "__main__":
    unittest.main()

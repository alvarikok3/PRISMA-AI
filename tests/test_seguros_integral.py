import unittest
from src.seguros.integral import CATALOGO, analizar_coberturas

class CoberturasIntegralesTest(unittest.TestCase):
    def test_categorias(self):
        self.assertGreaterEqual(len(CATALOGO),12)
    def test_cobertura_existente(self):
        p={"dependientes":2,"deudas":0,"viajes_anuales":0,"movilidad":True,
           "exposicion_laboral":"Baja","trabaja":True,"meses_emergencia":2,
           "cobertura_medica":True,"conduce":False,"vivienda_propietario":False}
        r=analizar_coberturas(p,{"Vida temporal"})
        vida=next(x for x in r if x["cobertura"]=="Vida temporal")
        self.assertIn("duplicidades",vida["estado"])
        self.assertTrue(all("denegar" not in x["estado"] for x in r))

if __name__=="__main__":
    unittest.main()

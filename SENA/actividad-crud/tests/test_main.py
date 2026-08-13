import os
import tempfile
import unittest
from unittest.mock import patch

import main


class SistemaAprendicesTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.archivo = os.path.join(self.temp_dir.name, "aprendices.json")

    def test_guardar_y_cargar_aprendices(self):
        aprendices = []
        main.save_aprendices(self.archivo, aprendices)
        self.assertEqual(main.load_aprendices(self.archivo), [])

    def test_registrar_aprendiz_y_evitar_duplicados(self):
        aprendices = []
        with patch("builtins.input", side_effect=["CC", "1001", "Ana Gómez", "2671234", "ADSO - Análisis y Desarrollo de Software"]):
            resultado = main.registrar_aprendiz(aprendices, self.archivo)

        self.assertTrue(resultado)
        self.assertEqual(len(aprendices), 1)
        self.assertEqual(aprendices[0]["numero_documento"], "1001")

        with patch("builtins.input", side_effect=["CC", "1001", "Ana Gómez", "2671234", "ADSO - Análisis y Desarrollo de Software"]):
            resultado_duplicado = main.registrar_aprendiz(aprendices, self.archivo)

        self.assertFalse(resultado_duplicado)
        self.assertEqual(len(aprendices), 1)


if __name__ == "__main__":
    unittest.main()

import unittest
from engine.fuel_calculator import calculate_module_fuel


class FuelCalculatorTests(unittest.TestCase):
    def test_calculates_weightless(self):
        self.assertEqual(0, calculate_module_fuel(0))

    def test_calculates_module1(self):
        self.assertEqual(0, calculate_module_fuel(1))

    def test_calculates_module2(self):
        self.assertEqual(0, calculate_module_fuel(2))

    def test_calculates_module4(self):
        self.assertEqual(0, calculate_module_fuel(4))

    def test_calculates_module6(self):
        self.assertEqual(0, calculate_module_fuel(6))

    def test_calculates_module8(self):
        self.assertEqual(0, calculate_module_fuel(8))

    def test_calculates_module14(self):
        self.assertEqual(2, calculate_module_fuel(14))

    def test_calculates_module56(self):
        self.assertEqual(16+3, calculate_module_fuel(56))

    def test_calculates_module124(self):
        self.assertEqual(39+11+1, calculate_module_fuel(124))


if __name__ == '__main__':
    unittest.main()

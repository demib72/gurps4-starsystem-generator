import unittest
from stargen.data import tables

class TestTables(unittest.TestCase):
    def test_find_solar_mass(self):
        mass = tables.find_solar_mass(5, 10)
        self.assertEqual(mass, 1.45)

    def test_world_climate(self):
        self.assertEqual(tables.world_climate(330), 'Hot')
        self.assertEqual(tables.world_climate(280), 'Cool')

    def test_pressure_category(self):
        self.assertEqual(tables.pressure_category(1.0), 'Standard')
        self.assertEqual(tables.pressure_category(0.4), 'Very Thin')

if __name__ == '__main__':
    unittest.main()

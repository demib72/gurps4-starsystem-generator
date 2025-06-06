import unittest
from unittest.mock import patch
from stargen.gasgiant import GasGiant

class DummyStar:
    def get_luminosity(self):
        return 1.0
    def get_mass(self):
        return 1.0
    def get_age(self):
        return 5.0

class TestGasGiant(unittest.TestCase):
    @patch('stargen.orbitcontents.DiceRoller.roll_dice', return_value=10)
    def test_gasgiant_creation(self, roll):
        gg = GasGiant(DummyStar(), 5.0)
        self.assertIn(gg.get_density(), [0.17, 0.19, 0.26])  # from table choices
        self.assertTrue(gg.get_diameter() > 0)
        self.assertTrue(gg.get_gravity() > 0)

if __name__ == '__main__':
    unittest.main()

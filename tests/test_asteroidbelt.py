import unittest
from unittest.mock import patch
from stargen.asteroidbelt import AsteroidBelt

class DummyStar:
    def get_luminosity(self):
        return 1.0
    def get_mass(self):
        return 1.0

class TestAsteroidBelt(unittest.TestCase):
    @patch('stargen.orbitcontents.DiceRoller.roll_dice', return_value=10)
    def test_asteroidbelt_properties(self, roll):
        ab = AsteroidBelt(DummyStar(), 2.0)
        self.assertEqual(ab.get_rvm(), 0)
        self.assertEqual(ab.get_resources(), 'Average')
        self.assertEqual(ab.get_climate(), 'Frozen')

if __name__ == '__main__':
    unittest.main()

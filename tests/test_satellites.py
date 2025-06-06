import unittest
from unittest.mock import patch
from stargen.satellites import Moon, Moonlet

class DummyPlanet:
    def __init__(self):
        self.size = 'Standard'
        self.mass = 1.0
        self.diameter = 1.0
        self.period = 1.0
    def type(self):
        return 'Terrestrial'
    def get_size(self):
        return self.size
    def get_diameter(self):
        return self.diameter
    def get_mass(self):
        return self.mass
    def get_period(self):
        return self.period
    def get_blackbody_temp(self):
        return 300

class DummyStar:
    def get_age(self):
        return 5.0
    def get_mass(self):
        return 1.0

class TestSatellites(unittest.TestCase):
    @patch('stargen.satellites.DiceRoller.roll_dice', return_value=10)
    def test_moon_creation(self, roll):
        moon = Moon(DummyPlanet(), DummyStar())
        self.assertIsNotNone(moon.get_orbit())
        self.assertIsNotNone(moon.get_rotation())

    @patch('stargen.satellites.DiceRoller.roll_dice', return_value=4)
    def test_moonlet_creation(self, roll):
        ml = Moonlet(DummyPlanet())
        self.assertIsNotNone(ml.get_orbit())
        self.assertIsNotNone(ml.get_period())

if __name__ == '__main__':
    unittest.main()

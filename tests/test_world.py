import unittest
from unittest.mock import patch
from stargen.world import World

class DummyStar:
    def __init__(self, mass=1.0, age=5.0):
        self.mass = mass
        self.age = age
    def get_mass(self):
        return self.mass
    def get_luminosity(self):
        return 1.0
    def get_age(self):
        return self.age

class TestWorld(unittest.TestCase):
    def setUp(self):
        self.star = DummyStar()

    @patch('stargen.utils.dice.DiceRoller.roll_dice', return_value=10)
    def test_world_creation(self, roll):
        world = World(self.star, 1.0, 'Standard')
        self.assertIsNotNone(world.get_type())
        self.assertIsInstance(world.get_mass(), (int, float))
        self.assertIsInstance(world.get_gravity(), (int, float))

if __name__ == '__main__':
    unittest.main()

import unittest
from stargen.utils.serializer import serialize_star_system

class DummyOrbitContent:
    def __init__(self):
        self.name = 'A1'
    def get_orbit(self):
        return 1.0
    def get_period(self):
        return 1.0
    def get_eccentricity(self):
        return 0.0
    def get_type(self):
        return 'Rock'
    def get_size(self):
        return 'Small'
    def num_moons(self):
        return 0
    def num_moonlets(self):
        return 0
    def get_hydrographic_cover(self):
        return 0

class DummyPlanetSystem:
    def __init__(self):
        self.gasarrangement = 'None'
        self.firstgasorbit = None
        self.orbitarray = [1.0]
        self.orbitcontents = {1.0: DummyOrbitContent()}
    def get_orbitcontents(self):
        return self.orbitcontents

class DummyStar:
    def __init__(self):
        self.planetsystem = DummyPlanetSystem()
    def get_letter(self):
        return 'A'
    def get_mass(self):
        return 1.0
    def get_sequence(self):
        return 'G'
    def get_temp(self):
        return 5800
    def get_luminosity(self):
        return 1.0
    def get_radius(self):
        return 1.0
    def get_age(self):
        return 5
    def get_orbit_limits(self):
        return (0.1, 40.0)
    def get_snowline(self):
        return 1.0
    def has_forbidden_zone(self):
        return False

class DummySystem:
    def __init__(self):
        self.stars = [DummyStar()]
        self.age = 5
        self.open_cluster = False
        self.orbits = []
        self.periods = []
    def get_age(self):
        return self.age
    def is_open_cluster(self):
        return self.open_cluster
    def get_orbits(self):
        return self.orbits
    def get_period(self):
        return self.periods

class TestSerializer(unittest.TestCase):
    def test_serialize_simple_system(self):
        system = DummySystem()
        data = serialize_star_system(system)
        self.assertEqual(data['age'], 5)
        self.assertEqual(len(data['stars']), 1)
        star = data['stars'][0]
        self.assertEqual(star['letter'], 'A')
        self.assertIn('planetsystem', star)
        ps = star['planetsystem']
        self.assertIn('orbitcontents', ps)
        self.assertEqual(list(ps['orbitcontents'].keys()), ['1.0'])

if __name__ == '__main__':
    unittest.main()

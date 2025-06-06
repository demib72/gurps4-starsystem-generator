import unittest
from stargen.orbitcontents import OrbitContent

class DummyStar:
    def __init__(self, mass=1.0, luminosity=1.0):
        self.mass = mass
        self.luminosity = luminosity
    def get_mass(self):
        return self.mass
    def get_luminosity(self):
        return self.luminosity

class TestOrbitContent(unittest.TestCase):
    def test_basic_properties(self):
        star = DummyStar()
        oc = OrbitContent(star, 1.0)
        self.assertAlmostEqual(oc.get_blackbody_temp(), 278.0)
        self.assertAlmostEqual(oc.get_period(), 1.0)

    def test_eccentricity_and_minmax(self):
        star = DummyStar()
        oc = OrbitContent(star, 1.0)
        oc.eccentricity = oc.make_eccentricity(12)
        oc.min_max = oc.make_min_max()
        self.assertEqual(oc.eccentricity, 0.2)
        self.assertAlmostEqual(oc.min_max[0], 0.8)
        self.assertAlmostEqual(oc.min_max[1], 1.2)

if __name__ == '__main__':
    unittest.main()

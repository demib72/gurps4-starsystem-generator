import unittest
from stargen.stargen import StarSystem

class DummyStar:
    def __init__(self, mass=1):
        self.mass = mass
        self.fz = None
    def get_mass(self):
        return self.mass
    def set_forbidden_zone(self, start, end):
        self.fz = (start, end)
    def get_forbidden_zone(self):
        return self.fz

class TestStarSystemHelpers(unittest.TestCase):
    def test_find_orbital_separation_index(self):
        ss = StarSystem.__new__(StarSystem)
        self.assertEqual(ss.find_orbital_separation_index(5), 0)
        self.assertEqual(ss.find_orbital_separation_index(12), 3)
        self.assertEqual(ss.find_orbital_separation_index(17), 4)

    def test_make_min_max_separations(self):
        ss = StarSystem.__new__(StarSystem)
        res = ss.make_min_max_separations([(1,0.1)])
        self.assertEqual(res, [(0.9, 1.1)])

    def test_calc_forbidden_zones(self):
        ss = StarSystem.__new__(StarSystem)
        res = ss.calc_forbidden_zones([(0.5, 1.5)])
        self.assertEqual(res, [(0.16666666666666666, 4.5)])

    def test_propagate_forbidden_zones(self):
        ss = StarSystem.__new__(StarSystem)
        stars = [DummyStar(), DummyStar(), DummyStar()]
        zones = [(0.1,0.2),(0.3,0.4)]
        stars = ss.propagate_forbidden_zones(stars, zones)
        self.assertEqual(stars[0].fz, (0.1,0.2))
        self.assertEqual(stars[1].fz, (0.1,0.2))
        self.assertEqual(stars[2].fz, (0.3,0.4))

if __name__ == '__main__':
    unittest.main()

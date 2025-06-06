import unittest
from unittest.mock import patch
from stargen.star import Star

class TestStar(unittest.TestCase):
    def test_orbit_limits_and_snow_line(self):
        with patch.object(Star, 'generate_star', return_value=(0,1.0,'G2',5800,1.0,1.0)):
            star = Star(age=5)
            self.assertAlmostEqual(star.get_orbit_limits()[0], 0.1)
            self.assertAlmostEqual(star.get_orbit_limits()[1], 40.0)
            self.assertAlmostEqual(star.get_snowline(), 0.1680089, places=6)

    def test_set_forbidden_zone(self):
        with patch.object(Star, 'generate_star', return_value=(0,1.0,'G2',5800,1.0,1.0)):
            star = Star(age=1)
            star.set_forbidden_zone(0.5, 2.0)
            self.assertTrue(star.has_forbidden_zone)
            self.assertEqual(star.get_forbidden_zone(), (0.5, 2.0))

if __name__ == '__main__':
    unittest.main()

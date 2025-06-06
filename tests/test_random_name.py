import unittest
from stargen.utils import random_name

class TestRandomName(unittest.TestCase):
    def test_generate_random_name_length(self):
        name = random_name.generate_random_name()
        self.assertTrue(8 <= len(name) <= 16)
        self.assertTrue(name.isalnum())

if __name__ == '__main__':
    unittest.main()

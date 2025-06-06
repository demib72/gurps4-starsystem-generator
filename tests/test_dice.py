import unittest
from stargen.utils.dice import DiceRoller

class TestDiceRoller(unittest.TestCase):
    def test_roll_dice_basic(self):
        roller = DiceRoller()
        result = roller.roll_dice(1, 0, 6)
        self.assertTrue(1 <= result <= 6)

    def test_roll_dice_modifier(self):
        roller = DiceRoller()
        result = roller.roll_dice(2, 3, 6)
        self.assertTrue(result >= 5)  # minimal 2d6 is 2, plus 3 = 5

if __name__ == '__main__':
    unittest.main()

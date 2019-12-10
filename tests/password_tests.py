import unittest

from security.password import PasswordGuesser


class PasswordTests(unittest.TestCase):
    def test_is_integer(self):
        guesser = PasswordGuesser()

        self.assertFalse(guesser.is_valid_password('Wrongs'))
        self.assertFalse(guesser.is_valid_password('3467.8'))

    def test_is_in_range(self):
        guesser = PasswordGuesser(135667, 135667)

        self.assertFalse(guesser.is_valid_password('135666'))
        self.assertTrue(guesser.is_valid_password('135667'))
        self.assertFalse(guesser.is_valid_password('135668'))

    def test_has_once_repeating_digit(self):
        self.assertTrue(PasswordGuesser.has_once_repeating_digit('12334'))

    def test_two_adjacent_digits_are_same(self):
        guesser = PasswordGuesser()

        self.assertFalse(guesser.is_valid_password('123456'))
        self.assertTrue(guesser.is_valid_password('123556'))
        self.assertFalse(guesser.is_valid_password('123555'))

    def test_count_valid_passwords_between_10_and_20(self):
        guesser = PasswordGuesser(10, 20)

        self.assertEqual(1, guesser.count_valid_passwords())

    def test_count_valid_passwords_between_110_and_120(self):
        guesser = PasswordGuesser(110, 120)

        self.assertEqual(8, guesser.count_valid_passwords())

    def test_count_valid_passwords_between_1220_and_1230(self):
        guesser = PasswordGuesser(1220, 1230)

        self.assertEqual(7, guesser.count_valid_passwords())


if __name__ == '__main__':
    unittest.main()

import sys


class PasswordGuesser:
    range = [0, sys.maxsize]

    def __init__(self, minimum=0, maximum=sys.maxsize):
        self.range = [minimum, maximum]

    def get_range_size(self):
        range_size = self.range[1] - self.range[0] + 1
        return range_size if range_size >= 0 else 0

    def is_within_range(self, passcode):
        return self.range[0] <= passcode <= self.range[1]

    @staticmethod
    def has_decreasing_digits(password):
        for i in range(0, len(password)-1):
            if password[i] > password[i+1]:
                return True
        return False

    @staticmethod
    def has_once_repeating_digit(password):
        last_digit = None
        last_digit_count = 0
        for digit in password:
            if digit == last_digit:
                last_digit_count += 1
            else:
                if last_digit_count == 2:
                    return True
                last_digit = digit
                last_digit_count = 1
        return last_digit_count == 2

    def is_valid_password(self, password):
        if not password.isdigit():
            return False
        if not self.is_within_range(int(password)):
            return False
        if self.has_decreasing_digits(password):
            return False
        return self.has_once_repeating_digit(password)

    def count_valid_passwords(self):
        count = 0
        for guess in range(self.range[0], self.range[1]+1):
            password = str(guess)
            if self.is_valid_password(password):
                count += 1
        return count

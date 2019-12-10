from security.password import PasswordGuesser

guesser = PasswordGuesser(108457, 562041)
count = guesser.count_valid_passwords()

print("Number of possible passwords: {}".format(count))

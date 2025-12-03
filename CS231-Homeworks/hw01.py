# MVR, Iteration homework
# I believe a palindrome is a String of any positive length
# that reads the same forward and backward.
# Since there are no explicit instructions indicating case-sensitivity,
# Racecar is a palindrome by standard definition.

print(sum(map(
    lambda original_word: (clean_word := original_word.strip().lower()) == clean_word[::-1],
    open("/users/abrick/resources/english")
)))
def count_odds(num):
    odds = 0
    for i in num:
        if i% 2 != 0:
            odds += 1
    return odds

# write count_odds in functional way
odds = lambda nums: sum(map(lambda x: x % 2, nums))

"""
lambda nums: ...
This defines a function that takes one argument, nums.

map(lambda x: x % 2, nums)
The inner lambda x: x % 2 takes each element x and computes its remainder when divided by 2.
For even numbers, x % 2 → 0.
For odd numbers, x % 2 → 1.

sum(...)
Now you sum those results:
1 + 0 + 1 + 0 + 1 = 3
"""

ones_zeros = lambda nums: map(lambda x: x% 2, nums) # obtain the mapped

print("count_odds: ", count_odds(range(10)))
print("odds: ", odds(range(10)))

print("ones_zeros using * unpacking and sep=\", \" ", *ones_zeros(range(10)), sep=", ")

print("using list():", list(ones_zeros(range(10))))
print(type(list(ones_zeros(range(10)))))


'''cube = lambda x: x ** 3
print(cube(10))
'''

from functools import reduce  # this came from the map / reduce examples in the notes

path = '/users/abrick/resources/english'


with open(path, encoding='utf-8') as f: # (From the 7.2 Reading and Writing Files  "with open(...) as f")

 term = map(lambda s: s.strip(), f) # taking lines from file and using map because it said not to loop?
 palindromw = map(lambda w: w == w[::-1], term) #checking to see if it is same as reverse// true or falsing.
# I had trouble but they do have a lot of information  on stack overflow ex: "str(int(a[::-1]))" there's a whole thread explaining,
# incase anyone else had trouble/and its a totally different problem... I was just looking at the reversing
 amount = reduce(lambda a, x: a + (1 if x else 0), palindromw, 0)
#it looks through every single word one by one. and asks if it is a palindrome and assigns 1 or 0 and just goes through list
print(amount)

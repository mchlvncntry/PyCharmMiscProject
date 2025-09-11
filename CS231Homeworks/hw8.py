'''
Decorate print() such that (A) it refuses to print anything under ten characters
long and (B) only five calls are allowed, and demonstrate these restrictions when
the program is run
'''

import builtins

orig_print = builtins.print

class Function_Print:
    def __init__(self, func):
        self.function = func
        # The counter to keep track of the number of function calls.
        self.call_counter = 0

    def __call__(self, *args, **kwargs):
        if self.call_counter >= 5:
          return self.function("Print is limited to 5 calls. You are over limit.")
        self.call_counter += 1
        total_len = 0
        # Accumulating the length of all arguments.
        for arg in args:
          total_len += len(arg)
        if total_len >= 10:
          return self.function(*args, **kwargs)
        else:
          return self.function("Too short to print. Please specify text that is longer than 10 charaters.")

@Function_Print
def print(*args, **kwargs):
    return orig_print(*args, **kwargs)

print("Hello World")
print("Hello", "World")
print("Hello")
print("one", "two", "three")
print("one, two, three")
print("one, two, three")
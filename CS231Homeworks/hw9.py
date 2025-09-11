'''
Implement two algorithms which demonstrably reach the same conclusion and
use profile or cProfile to time them both
'''

# profile_test.py
import math


def slow_factorial(n=100):
    if n == 0:
        return 1
    else:
        return n * slow_factorial(n - 1)


def pythonic_factorial(n=100):
    return math.factorial(n)


if __name__ == '__main__':
    import time

    start = time.time()
    result = slow_factorial()
    end = time.time()
    print("slow_factorial(): %f" % (end - start))
    start = time.time()
    result = pythonic_factorial()
    end = time.time()
    print("pythonic_factorial(): %f" % (end - start))
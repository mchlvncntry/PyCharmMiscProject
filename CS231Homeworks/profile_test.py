# profile_test.py
def slow(N=1000000):
    total = 0
    for i in range(N):
        total += i
    return total


def pythonic(N=1000000):
    total = sum(range(N))
    return total


if __name__ == '__main__':
    import time

    t0 = time.time()
    result = slow()
    t1 = time.time()
    print("slow(): %f" % (t1 - t0))
    t0 = time.time()
    result = pythonic()
    t1 = time.time()
    print("pythonic(): %f" % (t1 - t0))
#!/usr/bin/env python3
"""
profile_test_functional.py

Implements two factorial algorithms that reach the same result,
and compares their performance in a more functional, composable style.
"""

import math, time, cProfile

# ------------------------------
# Functional definitions
# ------------------------------
slow_factorial = lambda n=100: 1 if n == 0 else n * slow_factorial(n - 1)
pythonic_factorial = math.factorial  # direct reference

# ------------------------------
# Generic functional profiler
# ------------------------------
def profile_func(func, *args, **kwargs):
    """Return elapsed time for a single function call."""
    t0 = time.perf_counter()
    result = func(*args, **kwargs)
    t1 = time.perf_counter()
    return {"func": func.__name__, "result": result, "elapsed": t1 - t0}

# ------------------------------
# Comparison runner
# ------------------------------
def run_comparison(n=100):
    funcs = [slow_factorial, pythonic_factorial]
    results = list(map(lambda f: profile_func(f, n), funcs))
    for r in results:
        print(f"{r['func']:>20} → {r['elapsed']:.6f} sec")
    return results

# ------------------------------
# Entry point
# ------------------------------
if __name__ == "__main__":
    print("\nTiming comparison (functional style):")
    run_comparison(100)

    print("\nDetailed profiling (cProfile):")
    cProfile.run("run_comparison(100)")

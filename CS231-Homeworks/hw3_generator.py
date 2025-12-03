
# HW3 - Generators
# Prints all 1000 terms of the Leibniz formula until margin of error is ~0.001
# -----
# If you want to view the first 10 terms and every 100th term after,
# uncomment run_leibniz(display_choice=lambda n: n <= 10 or n % 100 == 0)

import math

def ordinal(n: int) -> str:
    """Return numeric ordinal string (1 -> '1st', 2 -> '2nd', 3 -> '3rd', etc.)."""
    suffixes = {1: "st", 2: "nd", 3: "rd"}
    if 10 <= n % 100 <= 20:
        suffix = "th"
    else:
        suffix = suffixes.get(n % 10, "th")
    return f"{n}{suffix}"

def leibniz_pi_generator():
    """Generates successive approximations of pi using the Leibniz formula."""
    running_sum = 0.0          # partial sum of 1 - 1/3 + 1/5 - ...
    term_count = 0             # number of terms used so far
    alternating_sign = 1.0     # +1, -1, +1, -1, ...

    while True:
        running_sum += alternating_sign / (2 * term_count + 1)
        yield 4.0 * running_sum, term_count + 1
        alternating_sign = -alternating_sign
        term_count += 1


def run_leibniz(target_accuracy=0.001, output_filter=None):
    """Run Leibniz approximation with flexible output print options."""
    pi_generator = leibniz_pi_generator()
    for pi_approx, num_terms in pi_generator:
        error = abs(math.pi - pi_approx)

        if output_filter is None or output_filter(num_terms):
            label = ordinal(num_terms)
            print(f"{label:>6} term: π approximately. {pi_approx:.10f} (error {error:.6f})")

        if error <= target_accuracy:
            print(f"\nReached target accuracy. End of program\n")
            break

if __name__ == "__main__":
    # Prints first 10, then every 100th term
    run_leibniz(output_filter=lambda n: n <= 10 or n % 100 == 0)

    # run_leibniz() # default: prints all terms

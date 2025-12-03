#!/usr/bin/env python3
"""
This program is extensively commented to ensure clarity.
It compares two π estimation methods: Leibniz and Monte Carlo.
It runs 1,000 trials, and in each trial both generators run
once until the default tolerance (0.001) is met.

METHODOLOGY:
Leibniz generator: Uses the alternating series π/4 = 1 - 1/3 + 1/5 - ...
Monte Carlo generator: Randomly samples points in a unit square and counts
the fraction falling inside a quarter circle (hit-or-miss method).
(Source: RPubs tutorial on Monte Carlo π estimation:
https://rpubs.com/cjp0803/montecarlo)

STOPPING CRITERION (Generators requirement extended to Profiling assignment):
Both methods stop when |pi_estimate - math.pi| ≤ tolerance (default: 0.001).
This ensures a fair, apples-to-apples speed comparison.

CLI ARGUMENTS:
The program accepts optional arguments to customize behavior:
  --trials: Number of time trials to run (default: 1000)
  --tolerance: Maximum acceptable error from math.pi (default: 0.001)
  --montecarlo_batch: Number of random samples per Monte Carlo iteration (default: 8)
  --profile: cProfile was mentioned in the Professor's Notes.
             Enable cProfile to analyze performance bottlenecks

USAGE EXAMPLES:
    # Run with defaults (1000 trials, tolerance=0.001)
    python3 FILENAME.py

    # Run 500 trials with tolerance 0.001
    python3 FILENAME.py --trials 500 --tolerance 0.001

    # Adjust Monte Carlo batch size
    python3 FILENAME.py --montecarlo_batch 50

    # Enable profiling to see performance statistics
    python3 FILENAME.py --profile
"""

import argparse, cProfile, pstats, random, textwrap, time, statistics as stats, math
from datetime import datetime
from io import StringIO
from itertools import count

DEFAULT_TOLERANCE = 0.001
DEFAULT_TRIALS = 1000
DEFAULT_MONTECARLO_BATCH = 5


# ---------------------------------
# Generators - infinite generators
# ---------------------------------

def leibniz_pi_generator():
    """
    Yield (pi_estimate, terms_used) via the Leibniz series.
    The Leibniz formula: π/4 = 1 - 1/3 + 1/5 - 1/7 + 1/9 - ...
    """
    running_sum = 0.0
    # simpler than using (-1)**k; exponentiation is unnecessary
    # since 1 raised to even or odd power will always be base 1
    sign = 1.0
    denominator = 1.0  # arithmetic sequence: 1, 3, 5, 7, ...

    for k in count(0):
        running_sum += sign / denominator
        pi_hat = 4.0 * running_sum
        terms_used = k + 1
        yield pi_hat, terms_used

        # update for next term
        sign = -sign
        denominator += 2.0


def monte_carlo_pi_generator(batch_size: int = DEFAULT_MONTECARLO_BATCH):
    """
    Yield (pi_estimate, samples_used, hits) using quarter-circle
    Monte Carlo.

    The method: randomly sample points (x,y) in [0,1] x [0,1].
    If x² + y² ≤ 1, the point is inside the quarter circle.
    π ≈ 4 * (hits / total_samples)

    Returns:
        tuple[float, int, int]: (pi_hat, samples_used, hits)
    """
    hits = 0
    samples_used = 0
    rand = random.random
    while True:
        local_hits = 0
        for _ in range(batch_size):
            x = rand()
            y = rand()
            if x * x + y * y <= 1.0:
                local_hits += 1
        hits += local_hits
        samples_used += batch_size
        p_hat = hits / samples_used
        pi_hat = 4.0 * p_hat
        yield pi_hat, samples_used, hits


# ------------------------------------------------------------------
# Wrapper functions that run the generators, and apply the
# stopping condition (within tolerance of math.pi).
# This explicitly satisfies the Profiling assignment instructions
# run_leibniz() does not use theoretical series bound (4.0/(2k+1)+1
# run_montecarlo() does not use CI half-width
# ------------------------------------------------------------------

def run_leibniz(*, tolerance: float, max_terms: int = 10_000_000):
    """
    Run the Leibniz series generator until the error from math.pi
    is within the specified tolerance.

    Stopping condition: |pi_estimate - math.pi| ≤ tolerance
    (Assignment #3 requirement: "error is within one thousandth of math.pi")

    Args:
        tolerance: Maximum acceptable absolute error from math.pi
        max_terms: Safety limit to prevent infinite loops (default: 10 million)

    Returns:
        tuple[float, int, float, float]:
        (pi_estimate, terms_used, elapsed_seconds, final_error)
    """
    time_at_zero = time.perf_counter()
    for pi_hat, terms_used in leibniz_pi_generator():
        error = abs(pi_hat - math.pi)
        elapsed = time.perf_counter() - time_at_zero

        if error <= tolerance or terms_used >= max_terms:
            return pi_hat, terms_used, elapsed, error

    raise RuntimeError(
        f"Leibniz failed to reach tolerance={tolerance} "
        f"before max_terms={max_terms}"
    )


def run_montecarlo(*, tolerance: float, batch_size: int = DEFAULT_MONTECARLO_BATCH,
                   max_samples: int = 20_000_000):
    """
    Run Monte Carlo until |pi_hat - math.pi| <= tolerance
    (or max_samples is reached).

    Returns:
        tuple[float, int, float, float]:
        (pi_hat, samples_used, elapsed_seconds, error)
    """
    time_at_zero = time.perf_counter()

    for pi_hat, samples_used, hits in monte_carlo_pi_generator(batch_size=batch_size):
        error = abs(pi_hat - math.pi)
        elapsed = time.perf_counter() - time_at_zero

        if error <= tolerance or samples_used >= max_samples:
            return pi_hat, samples_used, elapsed, error

    raise RuntimeError(
        f"Monte Carlo failed to reach tolerance={tolerance} "
        f"before max_samples={max_samples}"
    )


# -----------------------------------------------------------
# Profiling section
# Runs one Leibniz and one Monte Carlo trial under cProfile,
# then prints the top functions ranked by total time spent.
# -----------------------------------------------------------

def run_profile_once(tolerance: float = DEFAULT_TOLERANCE,
                     montecarlo_batch: int = DEFAULT_MONTECARLO_BATCH):
    """
    Run profiling for one Leibniz and one Monte Carlo then
    print the top functions by tottime.
    """
    pr = cProfile.Profile()
    pr.enable()
    _ = run_leibniz(tolerance=tolerance)
    _ = run_montecarlo(tolerance=tolerance, batch_size=montecarlo_batch)
    pr.disable()

    s = StringIO()
    pstats.Stats(pr, stream=s).strip_dirs().sort_stats(
        "tottime"
    ).print_stats(20)
    print("\n[PROFILE: top functions by tottime]\n" + s.getvalue())


# ------------------
# Run 1,000 trials
# ------------------

def run_trials(*, trials: int, tolerance: float, montecarlo_batch: int,
               profile: bool = False):
    if profile:
        run_profile_once(
            tolerance=tolerance, montecarlo_batch=montecarlo_batch
        )

    leibniz_times, montecarlo_times = [], []
    montecarlo_faster_count = 0  # "usually not always" count
    last_pi_lei = None
    last_pi_mc = None

    for _ in range(trials):
        # t_lei, t_mc: runtime duration of one trial
        pi_hat_lei, _, t_lei, _ = run_leibniz(tolerance=tolerance)
        pi_hat_mc, _, t_mc, _ = run_montecarlo(
            tolerance=tolerance, batch_size=montecarlo_batch
        )

        leibniz_times.append(t_lei)
        montecarlo_times.append(t_mc)
        if t_mc < t_lei:
            montecarlo_faster_count += 1
        last_pi_lei = pi_hat_lei
        last_pi_mc = pi_hat_mc

    median_leib = stats.median(leibniz_times)
    median_montecarlo = stats.median(montecarlo_times)

    _print_results(
        trials, tolerance, montecarlo_batch,
        median_leib, median_montecarlo,
        montecarlo_faster_count, last_pi_lei, last_pi_mc
    )


# -----------------------
# Display output helpers
# -----------------------

def _print_banner_start(start_time, profiling_on, args):
    print(
        f"\n{'+' * 60}\n"
        f"Program started on: "
        f"{start_time.strftime('%m-%d-%Y %I:%M:%S %p')}\n"
        f"Running with profiling={'ON' if args.profile else 'OFF'}\n"
        f"{'+' * 60}", flush=True
    )


def _print_banner_end(end_time, total_elapsed):
    print(
        f"\n{'+' * 60}\n"
        "Peer review: Please read the comment block at the top.\n"
        f"Total execution time: {total_elapsed:.2f} seconds\n"
        f"Program ended on: {end_time.strftime('%m-%d-%Y %I:%M:%S %p')}\n"
        f"{'+' * 60}\n", flush=True
    )


def _print_results(trials, tolerance, mc_batch, med_leib, med_mc,
                   mc_wins, last_pi_lei, last_pi_mc, width: int = 60):
    lei_wins = trials - mc_wins
    mc_pct_wins = 100.0 * mc_wins / trials
    lei_pct_wins = 100.0 * lei_wins / trials
    usual_winner = (
        "Monte Carlo" if mc_wins > lei_wins
        else "Leibniz" if mc_wins < lei_wins
        else "Tie"
    )
    faster_method = "Monte Carlo" if med_mc < med_leib else "Leibniz"
    factor = (med_leib / max(med_mc, 1e-15)) if med_mc < med_leib else (med_mc / max(med_leib, 1e-15))

    to_us = lambda s: s * 1_000_000  # seconds → microseconds

    def pl(label, value):
        print(f"{label:<35} {str(value):>{24}}")

    seps = "-" * width

    print("\nRESULTS")
    print(seps)
    pl(
        f"Trials {'(default)' if trials == DEFAULT_TRIALS else '[user input]'}",
        f"{trials:,}"
    )
    pl(
        f"Tolerance {'(default)' if tolerance == DEFAULT_TOLERANCE else '[user input]'}",
        f"{tolerance:g}"
    )
    pl(
        f"Monte Carlo batch size "
        f"{'(default)' if mc_batch == DEFAULT_MONTECARLO_BATCH else '[user input]'}",
        f"{mc_batch}"
    )
    pl("Avg Leibniz time (microseconds)", f"{to_us(med_leib):.2f}")
    pl("Avg Monte Carlo time (microseconds)", f"{to_us(med_mc):.2f}")
    pl("% Monte Carlo wins", f"{mc_pct_wins:.2f}%")
    pl("% Leibniz wins", f"{lei_pct_wins:.2f}%")
    pl("Final pi estimate (Leibniz)", f"{last_pi_lei:.9f}")
    pl("Final pi estimate (Monte Carlo)", f"{last_pi_mc:.9f}")
    print(seps)

    conclusion = (
        f"Monte Carlo won {mc_wins}/{trials} trials.\n"
        f"Leibniz won {lei_wins}/{trials} trials.\n"
        f"{faster_method} is {factor:.2f} times faster.\n")

    print(textwrap.fill(conclusion, width=width))


def main():
    parser = argparse.ArgumentParser(
        description="Compare Leibniz & Monte Carlo Pi generators",
        allow_abbrev=False)
    parser.add_argument(
        "--trials", type=int, default=DEFAULT_TRIALS,
        help="Number of trials to run")
    parser.add_argument(
        "--tol", "--tolerance", dest="tolerance",
        type=float, default=DEFAULT_TOLERANCE,
        help="Target tolerance")
    parser.add_argument(
        "--mc-batch", "--montecarlo_batch",
        dest="montecarlo_batch",
        type=int, default=DEFAULT_MONTECARLO_BATCH,
        help="Target Monte Carlo batch size")
    parser.add_argument(
        "--profile", action="store_true",
        help="Run cProfile before trials (default: off)")
    args = parser.parse_args()

    # Edge cases, validation
    if args.montecarlo_batch <= 0:
        raise ValueError("--mc-batch or --montecarlo_batch must be > 0")
    if args.tolerance <= 0:
        raise ValueError("--tolerance must be > 0")
    if args.trials <= 0:
        raise ValueError("--trials must be > 0")

    # Capture start time
    start_time = datetime.now()
    start_perf = time.perf_counter()
    _print_banner_start(start_time, args.profile, args)

    run_trials(trials=args.trials, tolerance=args.tolerance,
               montecarlo_batch=args.montecarlo_batch, profile=args.profile)

    # Capture end time
    end_time = datetime.now()
    total_elapsed = time.perf_counter() - start_perf
    _print_banner_end(end_time, total_elapsed)


if __name__ == "__main__":
    main()
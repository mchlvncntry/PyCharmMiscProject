#!/usr/bin/env python3
"""
This program is extensively commented to ensure clarity.
It compares two Pi generators: Leibniz and Monte Carlo.

It runs 1,000 trials, and in each trial both generators run
once until the tolerance (0.005) is met.

Unlike the Leibniz generator, which advances successive terms
through its alternating series, the Monte Carlo generator
estimates π by randomly sampling points in a unit square and
counting the fraction that fall inside the quarter circle
(hit-or-miss), using confidence intervals (CI) to decide
convergence. The accuracy and speed of Monte Carlo are
influenced by its batch size, which controls how many random
samples are drawn per iteration.
(Source: RPubs tutorial on Monte Carlo π estimation:
https://rpubs.com/cjp0803/montecarlo)

This program also accepts CLI arguments to adjust tolerance,
Monte Carlo batch size, number of trials, and to toggle profiling
on or off.

An optional --profile flag can run a single trial of each
generator under cProfile, printing the top functions by time
usage. cProfile was mentioned in the Professor's Notes.

Other ways to run this program: run each line in the command
line to see different results:

    # run 500 trials and set tolerance to 0.005
    python3 FILENAME.py --trials 500 --tolerance 0.005

    # set tolerance=0.005, montecarlo_batch=8
    python3 FILENAME.py --tolerance 0.005 --montecarlo_batch 8

    # run the code with profiling turned on
    python3 FILENAME.py --profile

    # run with defaults
    python3 FILENAME.py
"""

import argparse, cProfile, pstats, random, textwrap, time, statistics as stats
from datetime import datetime
from io import StringIO; from itertools import count

DEFAULT_TOLERANCE, DEFAULT_TRIALS, DEFAULT_MONTECARLO_BATCH = 0.005, 1000, 24

# -----------
# Generators
# -----------

def leibniz_pi_generator():
    """
    Yield (pi_estimate, terms_used) via the Leibniz series.
    Leibniz generator stops when the alternating-series error
    bound ≤ tolerance (bound = 4/(2k+3)) instead of using
    math.pi.
    """
    running_sum, sign = 0.0, 1
    for k in count(0):
        running_sum += sign / (2 * k + 1)
        pi_hat = 4.0 * running_sum
        terms_used = k + 1
        yield pi_hat, terms_used
        sign = -sign


def monte_carlo_pi_generator(batch_size: int = DEFAULT_MONTECARLO_BATCH):
    """
    Yield (pi_estimate, samples_used, hits) using quarter-circle
    Monte Carlo.

    Monte Carlo generator stops when the 95% CI (confidence
    interval) half-width for pi_estimate meets the tolerance
    bound rather than comparing |pi_hat - pi|.

    Returns:
        tuple[float, int, float, float]:
        (pi_hat, n_terms, elapsed_seconds, bound_used)
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


def run_leibniz(*, tolerance: float, max_terms: int = 10_000_000):
    """
    Run the Gregory–Leibniz series until the next-term error
    bound <= tolerance (or max_terms).

    For an alternating series: remainder after k terms <=
    magnitude of the next term. Error bound for π after k
    terms: 4 / (2k + 3).
    """
    time_at_zero = time.perf_counter()
    for k, (pi_hat, terms_used) in enumerate(leibniz_pi_generator()):
        # Next term for π/4 is 1/(2(k+1)+1); multiply by 4 for
        # π → 4/(2k+3)
        bound = 4.0 / (2 * (k + 1) + 1)  # = 4/(2k+3)
        elapsed = time.perf_counter() - time_at_zero
        if bound <= tolerance or terms_used >= max_terms:
            return pi_hat, terms_used, elapsed, bound
    raise RuntimeError(
        f"Leibniz failed to reach tolerance={tolerance} "
        f"before max_terms={max_terms}"
    )


def run_montecarlo(*, tolerance: float,batch_size: int = DEFAULT_MONTECARLO_BATCH,
    max_samples: int = 20_000_000):
    """
    Run Monte Carlo until the 95% CI half-width for pi_hat is
    <= tolerance (or max_samples).

    Using p_hat = hits / n and pi_hat = 4 * p_hat:
        Var(pi_hat) ≈ 16 * p_hat * (1 - p_hat) / n
        95% CI half-width ≈ 1.96 * sqrt(Var(pi_hat))

    Returns:
        tuple[float, int, float, float]:
        (pi_hat, samples_used, elapsed_seconds, half_width)
    """
    confidence_zscore = 1.96
    time_at_zero = time.perf_counter()

    for pi_hat, samples_used, hits in monte_carlo_pi_generator(
        batch_size=batch_size
    ):
        p_hat = hits / samples_used
        p_hat = min(max(p_hat, 1e-6), 1 - 1e-6)
        var_pi = 16.0 * p_hat * (1.0 - p_hat) / samples_used
        half_width = confidence_zscore * (var_pi ** 0.5)

        elapsed = time.perf_counter() - time_at_zero
        if half_width <= tolerance or samples_used >= max_samples:
            return pi_hat, samples_used, elapsed, half_width

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
    _ = run_montecarlo(
        tolerance=tolerance, batch_size=montecarlo_batch
    )
    pr.disable()

    s = StringIO()
    pstats.Stats(pr, stream=s).strip_dirs().sort_stats(
        "tottime"
    ).print_stats(20)
    print("\n[PROFILE: top functions by tottime]\n" + s.getvalue())

# -----------------
# Run 1,000 trials
# ------------------

def run_trials(*, trials: int, tolerance: float,montecarlo_batch: int,
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
        f"Please be patient and wait for the program to finish.\n"
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
    win_pct = 100.0 * max(mc_wins, lei_wins) / trials
    factor = max(med_mc, med_leib) / max(min(med_mc, med_leib), 1e-15)

    def pl(label, value):  # aligned key:value lines
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
    pl("Median Leibniz time (seconds)", f"{med_leib:.6f}")
    pl("Median Monte Carlo time (seconds)", f"{med_mc:.6f}")
    pl("% Monte Carlo wins", f"{mc_pct_wins:.2f}%")
    pl("% Leibniz wins", f"{lei_pct_wins:.2f}%")
    pl("Final pi estimate (Leibniz)", f"{last_pi_lei:.9f}")
    pl("Final pi estimate (Monte Carlo)", f"{last_pi_mc:.9f}")
    print(seps)

    conclusion = (
        f"{usual_winner} won {max(mc_wins, lei_wins)} runs out of "
        f"{trials:,} trials, roughly ({win_pct:.1f}%).\n"
        f"{'Monte Carlo' if med_mc < med_leib else 'Leibniz'} is "
        f"{factor:.0f} times faster."
    )

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
        montecarlo_batch=args.montecarlo_batch,profile=args.profile)

    # Capture end time
    end_time = datetime.now()
    total_elapsed = time.perf_counter() - start_perf
    _print_banner_end(end_time, total_elapsed)


if __name__ == "__main__":
    main()

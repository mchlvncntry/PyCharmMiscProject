#!/usr/bin/env python3
"""
This is a long code so comments are not sparse and are essential.
This program compares two Pi generators: Leibniz and Monte Carlo.
It runs 1,000 trials, and in each trial:
    • The Leibniz generator runs once until the tolerance is met.
    • The Monte Carlo generator runs once until the tolerance is met.
The elapsed times are compared to show that the Monte Carlo approach
is usually, but not always, faster.

The program also accepts CLI arguments to adjust tolerance, Monte Carlo
batch size, number of trials, and to toggle profiling on or off.

An optional --profile flag can run a single trial of each generator
under cProfile, printing the top functions by time usage. cProfile was
mentioned in the Professor's Notes.

Other ways to run this program: run each line in the command line to see different results:
    # run 500 trials and set tolerance to 0.005
    python FILENAME.py --trials 500 --tolerance 0.005

    # set tolerance=0.005, montecarlo_batch=8
    python3 FILENAME.py --tolerance 0.005 --montecarlo_batch 8

    python FILENAME.py --profile      # run the code with profiling turned on
    python FILENAME.py                # run with defaults
"""
from datetime import datetime
import random, time, argparse, statistics as stats
import cProfile, pstats
from io import StringIO
from itertools import count

DEFAULT_TOLERANCE = 0.005
DEFAULT_TRIALS = 1000
DEFAULT_MONTECARLO_BATCH = 16

# ----------------------
# Generators
# ----------------------

def leibniz_pi_generator():
    """
    Yield (pi_estimate, terms_used) via the Leibniz series.
    Leibniz generator stops when the alternating-series error bound ≤ tolerance (bound = 4/(2k+3))
    instead of using math.pi
    """
    running_sum, sign = 0.0, 1
    for k in count(0):
        running_sum += sign / (2*k + 1)
        pi_hat = 4.0 * running_sum
        terms_used = k + 1
        yield pi_hat, terms_used
        sign = -sign

def monte_carlo_pi_generator(batch_size: int = DEFAULT_MONTECARLO_BATCH):
    """
    Yield (pi_estimate, samples_used, hits) using quarter-circle Monte Carlo.
    Monte Carlo generator stops when the 95% CI (confidence interval) half-width for
    pi_estimate meets the tolerance bound rather than comparing |pi_hat - pi|.
    """
    hits = 0
    samples_used = 0
    rand = random.random  # local binding for speed
    while True:
        local_hits = 0
        for _ in range(batch_size):
            x = rand(); y = rand()
            if x*x + y*y <= 1.0:
                local_hits += 1
        hits += local_hits
        samples_used += batch_size
        p_hat = hits /samples_used
        pi_hat = 4.0 * p_hat
        yield pi_hat, samples_used, hits

def run_leibniz(*, tolerance: float, max_terms: int = 10_000_000):
    """
    Run the Gregory–Leibniz series until the next-term error bound <= tolerance (or max_terms).
    For an alternating series: remainder after k terms <= magnitude of the next term.
    Error bound for π after k terms: 4 / (2k + 3).

    Returns:
        tuple[float, int, float, float]: (pi_hat, n_terms, elapsed_seconds, bound_used)
    """
    time_at_zero = time.perf_counter()
    for k, (pi_hat, terms_used) in enumerate(leibniz_pi_generator()):
        # Next term for π/4 is 1/(2(k+1)+1); multiply by 4 for π → 4/(2k+3)
        bound = 4.0 / (2 * (k + 1) + 1)  # = 4/(2k+3)
        elapsed = time.perf_counter() - time_at_zero
        if bound <= tolerance or terms_used >= max_terms:
            return pi_hat, terms_used, elapsed, bound
    raise RuntimeError(f"Leibniz failed to reach tolerance={tolerance} before max_terms={max_terms}")


def run_montecarlo(*, tolerance: float, batch_size: int = DEFAULT_MONTECARLO_BATCH,
                   max_samples: int = 20_000_000):
    """
    Run Monte Carlo until the 95% CI half-width for pi_hat is <= tolerance (or max_samples).

    Using p_hat = hits / n and pi_hat = 4 * p_hat:
        Var(pi_hat) ≈ 16 * p_hat * (1 - p_hat) / n
        95% CI half-width ≈ 1.96 * sqrt(Var(pi_hat))

    Returns:
        tuple[float, int, float, float]: (pi_hat, samples_used, elapsed_seconds, half_width)
    """
    confidence_zscore = 1.96
    time_at_zero = time.perf_counter()

    for pi_hat, samples_used, hits in monte_carlo_pi_generator(batch_size=batch_size):
        p_hat = hits / samples_used
        var_pi = 16.0 * p_hat * (1.0 - p_hat) / samples_used
        half_width = confidence_zscore * (var_pi ** 0.5)

        elapsed = time.perf_counter() - time_at_zero
        if half_width <= tolerance or samples_used >= max_samples:
            return pi_hat, samples_used, elapsed, half_width

    raise RuntimeError(f"Monte Carlo failed to reach tolerance={tolerance} before max_samples={max_samples}")


# ----------------------------------------------------------------------
# For profiling
# Runs one Leibniz and one Monte Carlo trial under cProfile,
# then prints the top functions
# ranked by total time spent (tottime).
# ----------------------------------------------------------------------

def run_profile_once(tolerance: float = DEFAULT_TOLERANCE, montecarlo_batch: int = DEFAULT_MONTECARLO_BATCH):
    """
    Run profiling for one Leibniz and one Monte Carlo then print the top functions by tottime.
    """
    pr = cProfile.Profile()
    pr.enable()
    _ = run_leibniz(tolerance=tolerance)
    _ = run_montecarlo(tolerance=tolerance, batch_size=montecarlo_batch)
    pr.disable()

    s = StringIO()
    pstats.Stats(pr, stream=s).strip_dirs().sort_stats("tottime").print_stats(20)
    print("\n[PROFILE: top functions by tottime]\n" + s.getvalue())

# ----------------------------------------
# table output helper function
# ----------------------------------------

def _print_table(headers, rows, footer: str | None = None):
    headers = [str(h) for h in headers]
    rows = [[str(c) for c in r] for r in rows]

    # Column count
    num_cols = max(len(headers), *(len(r) for r in rows)) if rows else len(headers)
    headers += [""] * (num_cols - len(headers))
    rows = [r + [""] * (num_cols - len(r)) for r in rows]

    # Pre-split header lines and find header height
    header_lines = [h.split("\n") for h in headers]
    header_height = max(len(hs) for hs in header_lines)

    # Compute column widths from:
    #  - the longest line in each header cell
    #  - every row cell
    col_widths = [0] * num_cols
    for i in range(num_cols):
        header_max = max((len(s) for s in header_lines[i]), default=0)
        row_max = max((len(r[i]) for r in rows), default=0)
        col_widths[i] = max(header_max, row_max)

    def fmt_row(vals):
        return " | ".join(str(vals[i]).ljust(col_widths[i]) for i in range(num_cols))

    separator = "-+-".join("-" * w for w in col_widths)

    # Print multi-line headers
    for line_index in range(header_height):
        line_values = []
        for i in range(num_cols):
            cell_lines = header_lines[i]
            text = cell_lines[line_index] if line_index < len(cell_lines) else ""
            line_values.append(text)
        print(fmt_row(line_values))
    print(separator)

    # Print rows
    for row in rows:
        print(fmt_row(row))
    print()

    if footer:
        import textwrap
        table_width = len(separator)
        print(textwrap.fill(footer, width=table_width))
        print()

def _get_headers():
    return [
        "Count of\nTrials","Tolerance\nSet","Monte Carlo\nBatch Size",
        "Median Leibniz\nTime (seconds)","Median Monte Carlo\nTime (seconds)",
        "% Monte Carlo\nis faster","WINNER"
    ]

def run_trials(*, trials: int, tolerance: float, montecarlo_batch: int,
               profile: bool = False):
    """
    Each trial runs Leibniz once and Monte Carlo once,
    until both reach the same tolerance.
    """
    if profile:
        run_profile_once(tolerance=tolerance, montecarlo_batch=montecarlo_batch)

    leibniz_times, montecarlo_times = [], []
    montecarlo_faster_count = 0 # "usually not always" count
    last_pi_lei = None
    last_pi_mc = None

    for i in range(trials):
        # t_lei, t_mc: runtime duration of one Leibniz or Monte Carlo trial until it meets the tolerance
        pi_hat_lei, _, t_lei, _ = run_leibniz(tolerance=tolerance)
        pi_hat_mc, _, t_mc, _ = run_montecarlo(tolerance=tolerance, batch_size=montecarlo_batch)

        leibniz_times.append(t_lei)
        montecarlo_times.append(t_mc)
        if t_mc < t_lei:
            montecarlo_faster_count += 1
        last_pi_lei = pi_hat_lei
        last_pi_mc = pi_hat_mc

    median_leib = stats.median(leibniz_times)
    median_montecarlo = stats.median(montecarlo_times)
    montecarlo_win_prcnt = 100.0 * (montecarlo_faster_count / trials)
    winner = ("Monte Carlo" if montecarlo_faster_count > trials / 2
              else "Leibniz" if montecarlo_faster_count < trials / 2
              else "Tie")

    headers = _get_headers()
    rows = [[
        f"{trials:,}", f"{tolerance:g}",montecarlo_batch,
        f"{median_leib:.9f}", f"{median_montecarlo:.9f}",
        f"{montecarlo_faster_count}/{trials} ({montecarlo_win_prcnt:.1f}%)",
        winner,
    ]]

    _footer = (
        f"Conclusion: Monte Carlo was faster in {montecarlo_faster_count} out of {trials:,} trials "
        f"{montecarlo_win_prcnt:.1f}%. "
        f"Leibniz pi estimate: {last_pi_lei:.9f}\n"
        f"Monte Carlo pi estimate: {last_pi_mc:.9f}\n"
        f"The median { 'Monte Carlo' if median_montecarlo < median_leib else 'Leibniz' } runtime was "
        f"{min(median_montecarlo, median_leib):.6f} seconds compared to {max(median_montecarlo, median_leib):.6f} seconds "
        f"for { 'Leibniz' if median_montecarlo < median_leib else 'Monte Carlo' }, "
        f"showing that { 'Monte Carlo' if median_montecarlo < median_leib else 'Leibniz' } is typically faster. "

        f"Leibniz won {trials - montecarlo_faster_count} out of {trials:,} trials "
        f"({100.0 * (trials - montecarlo_faster_count) / trials:.1f}%)."
    )

    _print_table(headers, rows, footer=_footer)

def main():
    parser = argparse.ArgumentParser(description="Compare Leibniz & Monte Carlo Pi generators",allow_abbrev=False)
    parser.add_argument("--trials", type=int, default=DEFAULT_TRIALS, help="Number of trials to run")
    parser.add_argument("--tolerance", type=float, default=DEFAULT_TOLERANCE, help="target tolerance")
    parser.add_argument("--mc-batch", "--montecarlo_batch", dest="montecarlo_batch",
                        type=int, default=DEFAULT_MONTECARLO_BATCH, help="Monte Carlo batch size")
    parser.add_argument("--profile", action="store_true",
                        help="Run cProfile before trials (default: off)")
    args = parser.parse_args()

    # Edge cases, validation
    if args.montecarlo_batch <= 0:
        raise ValueError("--montecarlo_batch must be > 0")
    if args.tolerance <= 0:
        raise ValueError("--tolerance must be > 0")
    if args.trials <= 0:
        raise ValueError("--trials must be > 0")

    # Capture start time
    start_time = datetime.now()
    start_perf = time.perf_counter()

    print(f"\n{'+' * 100}")
    print(f"Program started at: {start_time.strftime('%m-%d-%Y %H:%M:%S')}")
    print(
        f"Please be patient... running with profiling={'ON' if args.profile else 'OFF'} "
        f"and default values:\n"
        f"TRIALS = {args.trials}  "
        f"TOLERANCE = {args.tolerance}  "
        f"MONTE CARLO BATCH SIZE = {args.montecarlo_batch}",
        flush=True)
    print(f"{'+' * 100}\n")

    run_trials(trials=args.trials,tolerance=args.tolerance,
        montecarlo_batch=args.montecarlo_batch,profile=args.profile,)

    # Capture end time
    end_time = datetime.now()
    end_perf = time.perf_counter()
    total_elapsed = end_perf - start_perf

    print(f"{'+' * 100}")
    print('Before you peer review: Please read the comment block at the very top of this program.')
    print(f"Program ended at: {end_time.strftime('%m-%d-%Y %H:%M:%S')}")
    print(f"Total execution time: {total_elapsed:.2f} seconds")
    print(f"{'+' * 100}\n")

if __name__ == "__main__":
    main()
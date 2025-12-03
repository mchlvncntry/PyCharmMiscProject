#!/usr/bin/env python3
"""
Compare two π generators (Leibniz vs Monte Carlo) with perf_counter timings.
Optionally run a targeted cProfile
"""

import math, random, time, argparse
import cProfile, pstats
from io import StringIO
from itertools import count

DEFAULT_TOL = 0.001
DEFAULT_TRIALS = 1000
DEFAULT_MONTECARLO_BATCH = 32
DEFAULT_REPEATS = 1

# -----------
# Generators
# -----------

def leibniz_pi_generator():
    """Yield (pi_estimate, terms_used) via the Leibniz series."""
    running_sum = 0.0
    sign = 1
    for k in count(0):                  # k = 0, 1, 2, ...
        running_sum += sign / (2*k + 1)
        pi_estimate = 4.0 * running_sum
        terms_used = k + 1
        yield pi_estimate, terms_used
        sign = -sign

def monte_carlo_pi_generator(batch_size: int = DEFAULT_MONTECARLO_BATCH, seed: int | None = None):
    """Yield (pi_estimate, samples_used) using quarter-circle Monte Carlo."""
    if seed is not None:
        random.seed(seed)
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
        pi_estimate = 4.0 * (hits / samples_used)
        yield pi_estimate, samples_used

def run_leibniz(*, tol: float, max_terms: int = 10_000_000):
    """
    Run Leibniz until |estimate - pi| <= tol (or max_terms).
    Return (pi_estimate, n_terms, elapsed_seconds, abs_error).
    """
    t0 = time.perf_counter()
    for pi_estimate, terms_used in leibniz_pi_generator():
        elapsed = time.perf_counter() - t0
        err = abs(pi_estimate - math.pi)
        if err <= tol or terms_used >= max_terms:
            return pi_estimate, terms_used, elapsed, err
    raise RuntimeError(f"Leibniz failed to reach tol={tol} before max_terms={max_terms}")

def run_montecarlo(*, tol: float, batch_size: int = DEFAULT_MONTECARLO_BATCH,
                   seed: int | None = None, max_samples: int = 20_000_000):
    """
    Run Monte Carlo until |estimate - pi| <= tol (or max_samples).
    Return (pi_estimate, samples_used, elapsed_seconds, abs_error).
    """
    t0 = time.perf_counter()
    for pi_estimate, samples_used in monte_carlo_pi_generator(batch_size=batch_size, seed=seed):
        elapsed = time.perf_counter() - t0
        err = abs(pi_estimate - math.pi)
        if err <= tol or samples_used >= max_samples:
            return pi_estimate, samples_used, elapsed, err
    raise RuntimeError(f"Monte Carlo failed to reach tol={tol} before max_samples={max_samples}")

# -----------------------------------------------------------
# For profiling
# Runs one Leibniz and one Monte Carlo trial under cProfile,
# then prints the top functions
# ranked by total time spent (tottime).
# -----------------------------------------------------------

def profile_once(tol: float = DEFAULT_TOL, montecarlo_batch: int = DEFAULT_MONTECARLO_BATCH):
    """
    Run profiling for one Leibniz and one Monte Carlo then print the top functions by tottime.
    """
    pr = cProfile.Profile()
    pr.enable()
    _ = run_leibniz(tol=tol)
    _ = run_montecarlo(tol=tol, batch_size=montecarlo_batch)
    pr.disable()

    s = StringIO()
    pstats.Stats(pr, stream=s).strip_dirs().sort_stats("tottime").print_stats(20)
    print("\n[PROFILE: top functions by tottime]\n" + s.getvalue())

# -----------------------------
# table output helper function
# -----------------------------

def _print_table(headers, rows):
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

    sep = "-+-".join("-" * w for w in col_widths)

    # Print multi-line headers
    for line_idx in range(header_height):
        line_vals = []
        for i in range(num_cols):
            cell_lines = header_lines[i]
            text = cell_lines[line_idx] if line_idx < len(cell_lines) else ""
            line_vals.append(text)
        print(fmt_row(line_vals))
    print(sep)

    # Print rows
    for r in rows:
        print(fmt_row(r))
    print()

def _get_headers():
    return [
        "Repeats\nCount",
        "Trials",
        "Tolerance",
        "Best Leibniz\nTime (seconds)",
        "Best Monte Carlo\nTime (seconds)",
        "% Monte Carlo\nis faster",
        "Winner"
    ]


# -------------------------------------
# Best-of-N timing helpers
# Run each method N multiple times (N)
# and return the fastest result.
# -------------------------------------

def best_of_leibniz(n: int, tol: float):
    best, best_t = None, float("inf")
    for _ in range(max(1, n)):
        res = run_leibniz(tol=tol)
        if res[2] < best_t:
            best, best_t = res, res[2]
    return best

def best_of_mc(n: int, tol: float, montecarlo_batch: int):
    best, best_t = None, float("inf")
    for _ in range(max(1, n)):
        res = run_montecarlo(tol=tol, batch_size=montecarlo_batch)
        if res[2] < best_t:
            best, best_t = res, res[2]
    return best

def run_trials(*, trials: int, tol: float, montecarlo_batch: int,
               repeats: int, profile: bool = False, progress: bool = False):
    """
    Run the trials from 1 up to N times (inclusive)
    """
    if profile:
        profile_once(tol=tol, montecarlo_batch=montecarlo_batch)

    rows = []
    headers = _get_headers()

    # One RNG warmup up front
    for _ in range(5000):
        random.random()

    for r in range(1, repeats + 1):
        leib_times, mc_times = [], []
        mc_faster_count = 0

        for i in range(trials):
            # Best-of-r (explicit helpers)
            _, _, t_lei, _ = best_of_leibniz(r, tol)
            _, _, t_mc,  _ = best_of_mc(r, tol, montecarlo_batch)

            leib_times.append(t_lei)
            mc_times.append(t_mc)
            if t_mc < t_lei:
                mc_faster_count += 1

            if progress and (i + 1) % 100 == 0:
                print(f"[repeats={r}] Completed {i + 1}/{trials} trials...")
        best_lei = min(leib_times)
        best_mc  = min(mc_times)
        mc_win_pct = 100.0 * (mc_faster_count / trials)
        winner = "Monte Carlo" if mc_faster_count > (trials / 2) else (
            "Leibniz" if mc_faster_count < (trials / 2) else "Tie")

        rows.append([
            r, trials, f"{tol:g}",
            f"{best_lei:.9f}",
            f"{best_mc:.9f}",
            f"{mc_faster_count}/{trials} ({mc_win_pct:.2f}%)",
            winner
        ])

    _print_table(headers, rows)

def main():
    # Set up command-line arguments for controlling trial runs, tolerance, batch sizes,
    # repeat comparisons, and optional profiling.
    parser = argparse.ArgumentParser(description="Compare Leibniz & Monte Carlo Pi generators")
    parser.add_argument("--trials", type=int, default=DEFAULT_TRIALS, help="Number of trials to run")
    parser.add_argument("--tol", type=float, default=DEFAULT_TOL, help="target tolerance")
    parser.add_argument("--montecarlo_batch", type=int, default=DEFAULT_MONTECARLO_BATCH, help="Monte Carlo batch size")
    parser.add_argument("--repeats", type=int, default=DEFAULT_REPEATS)

    # profiling OFF by default; enable with --profile
    parser.add_argument("--profile", action="store_true",
                        help="Run a one-off cProfile before trials (default: off)")
    args = parser.parse_args()

    print(
        f"Please be patient... running with profiling={'ON' if args.profile else 'OFF'} "
        f"and values:\n"
        f"Tolerance = {args.tol}, Trials = {args.trials}, "
        f"montecarlo_batch = {args.montecarlo_batch}, Repeats = {args.repeats}\n",flush=True
    )

    run_trials(
        trials=args.trials,
        tol=args.tol,
        montecarlo_batch=args.montecarlo_batch,
        repeats=args.repeats,
        profile=args.profile
    )
    print("\t# Other ways to run this program: run each line in the command line to see different results:\n"
          "\t# run 500 trials and set tolerance to 0.005\n"
          "\tpython FILENAME.py --trials 500 --tol 0.005\n\n"
          "\t# set repeats to 30 and montecarlo_batch to 1000\n"
          "\tpython FILENAME.py --montecarlo_batch 10000 --repeats 30\n\n" 
          "\t# set repeats=3, tol=0.005, montecarlo_batch=8\n"
          "\tpython3 FILENAME.py --repeats 3 --tol 0.005 --montecarlo_batch 8\n\n"
          "\t# run the code with profiling turned on\n"
          "\tpython3 FILENAME.py --repeats 3 --tol 0.005 --montecarlo_batch 8 --profile\n")

if __name__ == "__main__":
    main()


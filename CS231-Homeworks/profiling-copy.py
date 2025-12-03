#!/usr/local/bin/python3

"""
A program comparing Monte Carlo and Leibniz methods for estimating Pi. It runs
 multiple trials to determine which method converges faster and prints
 performance metrics.
"""

import math
from random import uniform
import time


def monte_carlo_pi(batch_size=20000):
    """
    An implementation of the Monte Carlo method to estimate Pi using random
     points.

    Args:
        batch_size (int, optional): Number of random points generated per
         batch.
        Defaults to 20000.

    Returns:
        float: Estimated value of Pi.
    """

    inside_circle, num_samples = 0, 0

    while True:
        # Generate batch of random points
        x = [uniform(-1, 1) for _ in range(batch_size)]
        y = [uniform(-1, 1) for _ in range(batch_size)]

        # Count points inside the circle
        inside_circle += \
            sum(1 for i in range(batch_size) if x[i] ** 2 + y[i] ** 2 <= 1)
        num_samples += batch_size

        pi_estimate = inside_circle * 4 / num_samples
        if abs(pi_estimate - math.pi) <= 0.001:
            break

    return pi_estimate


def leibniz_pi():
    """
    An implementation of the Leibniz formula to estimate Pi using an
     infinite series.

    Args:
        None.

    Returns:
        float: Estimated value of Pi.
    """

    denominator, pi_estimate, sign = 1, 0, 1

    while True:
        pi_estimate += 4 * (sign / denominator)
        if abs(pi_estimate - math.pi) <= 0.001:
            break
        sign *= -1
        denominator += 2

    return pi_estimate

def print_trail_run(i, num_trials, monte_pi_val, leib_pi_val, monte_time,
                    leibniz_time):
    """
    Prints the results and performance comparison for a single trial run.

    Args:
        i (int): Current trial number.
        num_trials (int): Total number of trials.
        monte_pi_val (float): Monte Carlo Pi estimate for this trial.
        leib_pi_val (float): Leibniz Pi estimate for this trial.
        monte_time (float): Time taken by Monte Carlo method in seconds.
        leibniz_time (float): Time taken by Leibniz method in seconds.

    Returns:
        None.
    """

    # Print trail run information
    print(f"Trial {i + 1} of {num_trials}.")
    print(f"Monte Carlo Pi Estimate: {monte_pi_val}.")
    print(f"Leibniz Pi Estimate: {leib_pi_val}.")
    print(f"Monte Carlo time: {monte_time * 1_000} ms.")
    print(f"Leibniz time: {leibniz_time * 1_000} ms.")

    ratio = monte_time / leibniz_time
    if ratio > 1:
        factor = ratio
        time_saved = monte_time - leibniz_time
        percentage_saving = (time_saved / monte_time) * 100
        print(
            f"Leibniz was faster by a factor of {factor:.0f}x.")
    else:
        factor = 1 / ratio
        time_saved = leibniz_time - monte_time
        percentage_saving = (time_saved / leibniz_time) * 100
        print(
            f"Monte Carlo was faster by a factor of {factor:.0f}x.")

    print('\n')


def main(num_trials: int):
    """
    Main function to run and compare Monte Carlo and Leibniz Pi
     estimation methods.

    Args:
        num_trials (int): Number of trials to run for comparison.

    Returns:
        None
    """
    results = []
    monte_times = []
    leibniz_times = []

    t_start = time.time()
    for i in range(num_trials):
        # Monte Carlo
        start_time = time.time()
        monte_pi_val = monte_carlo_pi()
        end_time = time.time()
        monte_time = end_time - start_time

        # Leibniz
        start_time_leib = time.time()
        leib_pi_val = leibniz_pi()
        end_time_leib = time.time()
        leibniz_time = end_time_leib - start_time_leib

        monte_times.append(monte_time)
        leibniz_times.append(leibniz_time)
        if (i + 1) % 10 == 0:
            print_trail_run(i, num_trials, monte_pi_val, leib_pi_val,
                            monte_time, leibniz_time)

    t_end = time.time()
    total_runtime = t_end - t_start
    # Print summary after trials
    print(f"After {num_trials} trials here are the results:")
    print( f"Monte Carlo was faster than Leibniz {sum(results)} times out of "
           f"{num_trials} trials.")
    # Calculate the average times
    average_monte = sum(monte_times) / num_trials
    average_leibniz = sum(leibniz_times) / num_trials

    print(f"Average Monte Carlo time: {average_monte * 1_000} ms.")
    print(f"Average Leibniz time: {average_leibniz * 1_000} ms.")

    average_ratio = average_monte / average_leibniz
    if average_ratio > 1:
        factor = average_ratio
        time_saved = average_monte - average_leibniz
        percentage_saving = (time_saved / average_monte) * 100
        print(
            f"Leibniz on average was faster by a factor of {factor:.0f}x.")
    else:
        factor = 1 / average_ratio
        time_saved = average_monte - average_leibniz
        percentage_saving = (time_saved / average_leibniz) * 100
        print(f"Monte Carlo on average was faster by a factor of "
              f"{factor:.0f}x.")

    total_minutes = int(total_runtime // 60)
    total_seconds = int(total_runtime % 60)

    if total_minutes > 0:
        print(
            f"It took {total_minutes} minute(s) and {total_seconds} second(s) "
            f"to run {num_trials} trials.")
    else:
        print(f"It took {total_seconds} second(s) to run {num_trials} trials.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="A program that indicates runs both the Monte Carlo "
                    "method and Leibniz method to see which converges faster."
                    "formula at converging to pi."
    )
    parser.add_argument(
        "--num_trials",
        help="Number of trials (default: 1000)",
        type=int,
        default=1000,
    )
    args = parser.parse_args()

    main(args.num_trials)
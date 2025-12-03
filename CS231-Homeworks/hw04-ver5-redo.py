import math, random, time, statistics as stats

TOL = 1e-3
TRIALS = 1000
MC_BATCH = 16  # yields per batch (faster) but still a generator

def leibniz_gen():
    s, sign, denom = 0.0, 1.0, 1.0                 # π = 4 * Σ (-1)^k/(2k+1)
    while True:
        s += sign * (4.0 / denom)
        yield s
        sign = -sign
        denom += 2.0

def monte_carlo_gen(batch=MC_BATCH):
    inside = total = 0
    r = random.random
    while True:
        hits = 0
        for _ in range(batch):
            x, y = r(), r()
            hits += (x*x + y*y <= 1.0)
        inside += hits; total += batch
        yield 4.0 * inside / total

def time_until_tol(gen_func, tol=TOL):
    t0 = time.perf_counter()
    for est in gen_func():
        if abs(est - math.pi) <= tol:
            return time.perf_counter() - t0

def main():
    wins_L = wins_M = 0
    tL, tM = [], []
    for i in range(TRIALS):
        if i % 2 == 0:  # alternate order to avoid bias
            tl = time_until_tol(leibniz_gen)
            tm = time_until_tol(lambda: monte_carlo_gen(MC_BATCH))
        else:
            tm = time_until_tol(lambda: monte_carlo_gen(MC_BATCH))
            tl = time_until_tol(leibniz_gen)
        tL.append(tl); tM.append(tm)
        wins_L += (tl < tm)
        wins_M += (tm <= tl)

    print(f"After {TRIALS} trials:")
    print(f"Leibniz faster: {wins_L} times")
    print(f"Monte Carlo faster: {wins_M} times")
    print(f"Medians — Leibniz: {stats.median(tL):.6f}s, Monte Carlo: {stats.median(tM):.6f}s")

if __name__ == "__main__":
    main()

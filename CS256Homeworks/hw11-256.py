# Purpose: Visualise trajectories from Dorais & Gutierrez (2021) centering meditation RCT
# Source: Dorais S, Gutierrez D (2021) The Effectiveness of a Centering Meditation… *Frontiers in Psychology* 12:720824.
# Tools: matplotlib, pandas
# Data-Ink Ratio: high (minimal gridlines, clean axes)
# Graphics size: 1272×786 (width×height)
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# --- Simulated/illustrative data (replace or refine with actual means if available) ---
timepoints = ["Baseline (T1)", "2 weeks (T2)", "4 weeks (T3)"]
# Assume PSS: higher scores = more stress
# Suppose control group stays roughly flat or slightly up; treatment group declines
stress_control = [20.0, 20.5, 21.0]
stress_treatment = [20.0, 18.5, 16.0]

# Assume CAMS-R: higher scores = more mindfulness
mind_control = [31.0, 31.2, 31.4]
mind_treatment = [31.0, 32.5, 34.0]

df = pd.DataFrame({
    "Time": np.tile(timepoints, 2),
    "Group": ["Control"]*3 + ["Treatment"]*3,
    "Stress_PSS": stress_control + stress_treatment,
    "Mind_CAMSR": mind_control + mind_treatment
})

# --- Plotting ---
plt.rcParams.update({
    "figure.figsize": (12.72, 7.86),  # approximate 1272×786 px at 100 dpi
    "axes.spines.top": False,
    "axes.spines.right": False
})

fig, axes = plt.subplots(nrows=1, ncols=2)

# Stress plot
ax = axes[0]
for grp, grp_df in df.groupby("Group"):
    ax.plot(grp_df["Time"], grp_df["Stress_PSS"], marker='o', label=grp)
ax.set_title("Perceived Stress Scale (PSS)")
ax.set_ylabel("PSS Score")
ax.set_ylim(14, 24)
ax.legend()
ax.grid(False)

# Mindfulness plot
ax = axes[1]
for grp, grp_df in df.groupby("Group"):
    ax.plot(grp_df["Time"], grp_df["Mind_CAMSR"], marker='o', label=grp)
ax.set_title("CAMS-R (Trait Mindfulness)")
ax.set_ylabel("CAMS-R Score")
ax.set_ylim(29, 35)
ax.legend()
ax.grid(False)

# Common styling
for ax in axes:
    ax.set_xticklabels(timepoints, rotation=30, ha="right")
    # minimal ticks
    ax.tick_params(axis='both', which='both', length=0)

plt.tight_layout()
plt.show()

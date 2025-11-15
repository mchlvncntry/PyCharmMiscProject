#!/usr/bin/env python3
"""
Misleading graphic: makes it look like meditation INCREASES stress over time
by inverting the y-axis and removing the control group.
"""

import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib.gridspec import GridSpec

# ---- constants for exact size (1 MP) ----
W, H, DPI = 1272, 786, 100
FIGSIZE = (W / DPI, H / DPI)

# ---- data (true means) ----
weeks = np.array([0, 2, 4])
labels = ["Week 0 (Baseline)", "Week 2", "Week 4"]
meditation_mean = np.array([20.1, 18.9, 17.5])

# ---- figure with footer area ----
fig = plt.figure(figsize=FIGSIZE, dpi=DPI)
gs = GridSpec(
    2, 1,
    height_ratios=[3, 1],
    hspace=0.10,  # small gap between plot and footer
)

ax = fig.add_subplot(gs[0])   # main plot
cax = fig.add_subplot(gs[1])  # footer text
cax.axis("off")

# ---- misleading line plot (meditation only, inverted y-axis) ----
ax.plot(
    weeks,
    meditation_mean,
    marker="o",
    linewidth=2.5,
    label="Meditation (n = 61)"
)

ax.set_xticks(weeks, labels, fontsize=11)
ax.set_ylabel("Perceived Stress Scale (PSS-10)", fontsize=11)

# *** KEY LIE: invert the y-axis so a real decrease looks like an increase ***
# True values go 20.1 -> 18.9 -> 17.5 (downward),
# but with 21 at the bottom and 17 at the top, the line slopes UP visually.
ax.set_ylim(21, 17)

ax.set_title(
    "Daily Centering Meditation Increases Perceived Stress Over Time\n"
    "(Misleading Graphic)",
    fontsize=14,
    pad=14,
)

ax.grid(axis="y", linestyle=":", linewidth=0.7)
ax.legend(loc="upper left", fontsize=11)

# ---- misleading footer text ----
footer = (
    "\n\nSOURCE: Dorais, S. et al. (2021). The Effectiveness of a Centering Meditation Intervention on College Stress and "
    "Mindfulness: A Randomized Controlled Trial. Frontiers in Psychology.\n\n"
    "METHOD: Average scores from the Perceived Stress Scale (PSS-10) were taken from Table 2 for the Meditation group "
    "(n = 61) at Baseline (Week 0), Week 2, and Week 4.\n\n"
    "INTERPRETATION (MISLEADING): Because the plotted line slopes upward on this inverted scale, it appears that students "
    "who practiced daily centering meditation became progressively MORE stressed over the 4-week period."
)

cax.text(
    0.02, 0.98, footer,
    ha="left", va="top",
    fontsize=9.5,
    color="black",
    wrap=True,
    linespacing=1.3,
    transform=cax.transAxes,
)

# ---- save EXACT 1272×786 px (no resizing) ----
out = os.path.expanduser("~/Downloads/meditation_stress_rct_LIE_increases_1mp.png")
fig.savefig(out, dpi=DPI, pad_inches=0, bbox_inches=None)
plt.show()
print(f"✅ Saved misleading graphic: {out}  (expected size: 1272×786 px)")

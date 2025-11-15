# 1 MP figure with footer BELOW the graph (fixed 1272×786 px)
import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib.gridspec import GridSpec

# ---- constants for exact size ----
W, H, DPI = 1272, 786, 100
FIGSIZE = (W / DPI, H / DPI)

# ---- data ----
weeks = np.array([0, 2, 4])
labels = ["Week 0 (Baseline)", "Week 2", "Week 4"]
control_mean    = np.array([20.1, 19.1, 19.4])
meditation_mean = np.array([20.1, 18.9, 17.5])

# ---- figure with two rows: plot (top) + footer (bottom) ----
fig = plt.figure(figsize=FIGSIZE, dpi=DPI)
gs  = GridSpec(nrows=2, ncols=1, height_ratios=[64, 36], figure=fig)  # ~64% plot / 36% caption

ax  = fig.add_subplot(gs[0, 0])   # plot
cax = fig.add_subplot(gs[1, 0])   # caption
cax.axis("off")

# ---- plot styling ----
ax.plot(weeks, meditation_mean, "-o", color="#e69f00", label="Meditation (n=61)")
ax.plot(weeks, control_mean, "-o", color="#56b4e9", label="Control (n=89)")
ax.set_title("Daily Centering Meditation Reduces Perceived Stress (RCT)")
ax.set_ylabel("Perceived Stress Scale (PSS-10, 0–40)")
ax.set_xticks(weeks)
ax.set_xticklabels(labels)
ax.set_ylim(15, 21)
ax.legend()

# ---- footer text (inside the bottom caption panel) ----
footer = (
    "PURPOSE: This line graph illustrates results from Dorais et al. (2021), a 4-week randomized controlled trial "
    "testing the effect of\ncentering meditation on college students’ perceived stress.\n\n"
    "SOURCE: Dorais S., & Gutierrez D. (2021). The Effectiveness of a Centering Meditation Intervention on College "
    "Stress and Mindfulness.\nFrontiers in Psychology, 12, 720824. DOI: 10.3389/fpsyg.2021.720824.\n\n"
    "TOOLS USED: Python 3.11 with Matplotlib and NumPy libraries. Exported at 1272 by 786 px to meet "
    "the 1-MP requirement.\n\n"
    "METHOD: Average scores from the Perceived Stress Scale (PSS-10) were taken from Table 2 of Dorais et al. (2021). "
    "\nThese values represent how stressed participants in the Meditation group (n = 61 participants) and the Control "
    "group (n = 89 participants)\nfelt during the study. Group means were plotted at Baseline (Week 0), Week 2, and "
    "Week 4 on a 0–40 scale, where higher numbers \nindicate greater perceived stress.\n\n"
    "INTERPRETATION: The meditation group’s average stress declined by about 2.6 points over 4 weeks, while the control "
    "group changed little,\nshowing that centering meditation meaningfully reduced perceived stress."
)
cax.text(0.02, 0.98, footer, ha="left", va="top", fontsize=9.5, color="black", wrap=True, linespacing=1.3)

# ---- save EXACT 1272×786 px (no resizing) ----
out = os.path.expanduser("~/Downloads/meditation_stress_rct_truth_1mp.png")
fig.savefig(out, dpi=DPI, pad_inches=0, bbox_inches=None)
plt.show()
print(f"✅ Saved: {out}  (expected size: 1272×786 px)")

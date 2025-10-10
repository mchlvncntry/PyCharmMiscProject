import matplotlib.pyplot as plt
import numpy as np

# -------------------------------
# DATA
# -------------------------------
age_groups = [
    "10–19 years",
    "65–74 years",
    "75 years and over",
    "45–54 years",
    "35–44 years",
    "60–64 years",
    "55–59 years",
    "25–34 years",
    "20–24 years",
    "0–9 years",
]
checkouts = [
    13173346,
    11418585,
    9012967,
    8600899,
    6202604,
    5198361,
    4944453,
    4601272,
    4566050,
    2047090,
]

# -------------------------------
# FIGURE SETUP
# -------------------------------
dpi_value = 150
fig_w = 1272 / dpi_value
fig_h = 786 / dpi_value
fig = plt.figure(figsize=(fig_w, fig_h), dpi=dpi_value)
gs = fig.add_gridspec(nrows=1, ncols=2, width_ratios=[0.72, 0.28], wspace=0.3)
fig.patch.set_facecolor("white")

# -------------------------------
# LEFT CHART
# -------------------------------
ax = fig.add_subplot(gs[0, 0], facecolor="white")
colors = plt.cm.viridis(np.linspace(0.1, 0.9, len(age_groups)))[::-1]
bars = ax.barh(age_groups, checkouts, color=colors, edgecolor="none")

# -------------------------------
# LABELS INSIDE BARS
# -------------------------------
for bar, value in zip(bars, checkouts):
    x = bar.get_width()
    y = bar.get_y() + bar.get_height() / 2

    # Estimate color brightness to choose white or black text
    r, g, b, _ = bar.get_facecolor()
    brightness = (r*0.299 + g*0.587 + b*0.114)
    text_color = "white" if brightness < 0.55 else "black"

    ax.text(
        x - (x * 0.02),  # slightly inset from right edge
        y,
        f"{value:,}",
        va="center",
        ha="right",
        fontsize=10,
        color=text_color,
        fontweight="bold"
    )

# -------------------------------
# TITLE & LABELS
# -------------------------------
ax.set_title("SF Library Checkouts by Age Range (2016–2024)",
             fontsize=18, color="#222222", pad=18)
ax.set_xlabel("Total Checkouts (in millions)", fontsize=12, color="#333333", labelpad=10)
ax.set_xticks([0, 2e6, 4e6, 6e6, 8e6, 10e6, 12e6, 14e6])
ax.set_xticklabels(["0", "2M", "4M", "6M", "8M", "10M", "12M", "14M"], color="#333333")

# No gridlines or y-axis tick marks
ax.grid(False)
ax.tick_params(axis='y', left=False)

# Horizontal x-axis baseline
ax.axvline(x=0, color="#555555", linewidth=1)

# Clean spines
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.spines["bottom"].set_color("#555555")

# -------------------------------
# RIGHT TEXT AREA (BLANK)
# -------------------------------
ax_txt = fig.add_subplot(gs[0, 1], facecolor="white")
ax_txt.set_axis_off()

# -------------------------------
# SAVE FILE
# -------------------------------
output_path = "/mnt/data/SF_Library_Checkouts_2016_2024_labels_inside.png"
plt.savefig(output_path, dpi=dpi_value, bbox_inches="tight", facecolor="white", pad_inches=0.35)
plt.close(fig)

print(f"✅ File saved to: {output_path}")

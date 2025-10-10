# misleading_bubble_chart.py
# Creates a misleading bubble chart that visually suggests 65–74 years is the top group
# Saves both SVG (vector) and 1272×786 PNG

import math
import textwrap
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.lines import Line2D

# --- paths ---
CSV_PATH = "/Users/mvrayo-mini/Downloads/Library_Usage_20250916.csv"
OUT_SVG  = "/Users/mvrayo-mini/Downloads/result_bubble_with_text.svg"
OUT_PNG  = "/Users/mvrayo-mini/Downloads/result_bubble_with_text.png"  # 1272x786

# --- load & aggregate ---
df = pd.read_csv(CSV_PATH, low_memory=False)
df["Total Checkouts"] = pd.to_numeric(df["Total Checkouts"], errors="coerce")
df["Circulation Active Year"] = pd.to_numeric(df["Circulation Active Year"], errors="coerce")
df = df[df["Circulation Active Year"].between(2016, 2024, inclusive="both")]

agg = (
    df.groupby("Age Range")["Total Checkouts"]
      .sum()
      .sort_values(ascending=False)
)

data = agg.reset_index().rename(columns={"Age Range": "age", "Total Checkouts": "value"})

# --- bubble sizes (MISLEADING on purpose) ---
# Scatter 's' expects AREA (pt^2). People judge *radius*, so we scale wrong (by value),
# then bias: inflate 65–74 and deflate 10–19 slightly.
max_val = float(data["value"].max())
size_base = 9000  # knob: larger => bigger bubbles overall
sizes = size_base * (data["value"] / max_val)  # WRONG scaling (radius-like)
sizes = sizes.values.copy()

for i, row in data.iterrows():
    if row["age"] == "65 to 74 years":
        sizes[i] *= 1.35   # inflate
    elif row["age"] == "10 to 19 years":
        sizes[i] *= 0.80   # deflate

# --- positions: center target, ring others ---
coords = {}
target_age = "65 to 74 years"
# center bubble
coords[target_age] = (0.0, 0.0)

others = [a for a in data["age"].tolist() if a != target_age]
R = 1.0
angles = np.linspace(0, 2*np.pi, num=len(others), endpoint=False)
for a, th in zip(others, angles):
    coords[a] = (R * math.cos(th), R * math.sin(th))

# --- colors ---
cmap = cm.get_cmap("tab20", len(data))
color_map = {age: cmap(i) for i, age in enumerate(data["age"])}
color_map[target_age] = "#26706f"  # stronger teal for emphasis

# --- arrays for scatter (note: keep colors as a Python list, not a numpy array) ---
x = np.array([coords[age][0] for age in data["age"]])
y = np.array([coords[age][1] for age in data["age"]])
c = [color_map[age] for age in data["age"]]   # list of RGBA colors ✅

# --- figure ---
fig, ax = plt.subplots(figsize=(12.72, 7.86))  # 1272x786 at 100 dpi
ax.set_aspect("equal")
ax.axis("off")

# bubbles
ax.scatter(x, y, s=sizes, c=c, alpha=0.95, linewidths=1, edgecolors="white")

# labels inside bubbles
for (xi, yi, age, val, sz) in zip(x, y, data["age"], data["value"], sizes):
    # label font size scales mildly with bubble size
    fs = int(max(8, min(13, 7 + 0.003 * (sz ** 0.5))))
    ax.text(xi, yi, f"{age}\n{int(val):,}", ha="center", va="center",
            fontsize=fs, color="white", weight="bold")

# title
ax.set_title("SF Library Checkouts (Misleading) — Bubble Emphasis on 65–74 Years",
             fontsize=20, weight="bold", pad=12)

# keep all bubbles in view; leave right margin for panel
pad = 1.8
ax.set_xlim(-pad, pad * 1.18)
ax.set_ylim(-pad, pad)

# --- legend panel (right) ---
handles = [
    Line2D([0], [0], marker='o', linestyle='',
           markerfacecolor=color_map[age], markeredgecolor='white',
           markersize=8, label=age)
    for age in data["age"]
]
leg = ax.legend(handles=handles, title="Age Range", fontsize=10, title_fontsize=11,
                loc="upper left", bbox_to_anchor=(1.01, 1.00), frameon=True)
leg.get_frame().set_facecolor("white")
leg.get_frame().set_edgecolor("#CCCCCC")

# --- Purpose/Source/Tools panel text under legend ---
panel_text = (
    "Purpose: This graphic argues that patrons aged 65–74 years "
    "checked out the most materials from San Francisco Public Library "
    "between 2016 and 2024 (inclusive).\n\n"
    "Source: https://data.sfgov.org/Culture-and-Recreation/"
    "Library-Usage/qzz6-2jup/about_data\n\n"
    "Tools: Python with pandas (data wrangling) and Matplotlib (charting)."
)
wrapped = textwrap.fill(panel_text, width=42)

fig.text(1.01, 0.46, wrapped, ha="left", va="top", fontsize=11,
         bbox=dict(facecolor="white", edgecolor="#CCCCCC"),
         transform=ax.transAxes)

# reserve space for the right-side panel & title
fig.subplots_adjust(right=0.76, left=0.06, top=0.88, bottom=0.08)

# --- save outputs ---
plt.savefig(OUT_SVG, format="svg", bbox_inches="tight", pad_inches=0.25)   # vector crisp
plt.savefig(OUT_PNG, dpi=100, bbox_inches="tight", pad_inches=0.25)        # 1272x786 PNG
plt.close()
print("Saved:", OUT_SVG)
print("Saved:", OUT_PNG)

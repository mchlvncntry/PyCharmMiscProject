# acquisitions_chart.py
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

# --- Data (manually entered from the infographic) ---
items = [
    ("Microsoft", 68.7, 2022, "Activision Blizzard"),
    ("Take-Two", 12.7, 2022, "Zynga"),
    ("Microsoft", 7.5, 2020, "ZeniMax"),
    ("Tencent", 8.6, 2016, "Supercell"),
    ("Activision Blizzard", 5.9, 2015, "King"),
    ("ByteDance", 4.0, 2021, "Moonton"),
    ("Sony", 3.6, 2022, "Bungie"),
    ("Mojang", 2.5, 2014, "Mojang (sold to Microsoft)"),
    ("Facebook", 2.0, 2014, "Oculus"),
    ("EA", 2.4, 2021, "Glu"),
    ("EA", 1.4, 2021, "Playdemic"),
    ("Zynga", 1.8, 2020, "Peak"),
    ("Bandai", 1.7, 2005, "Namco"),
    ("Tencent", 1.3, 2020, "Sumo")
]

# Convert to arrays and sort by value descending for neat horizontal bars
items_sorted = sorted(items, key=lambda x: x[1], reverse=True)
labels = [it[0] for it in items_sorted]
values = np.array([it[1] for it in items_sorted])
years = [it[2] for it in items_sorted]
targets = [it[3] for it in items_sorted]

# --- Plot configuration ---
# Desired pixel dimensions
PIX_W, PIX_H = 1272, 786
DPI = 100  # choose dpi -> figsize = pixels / dpi
figsize = (PIX_W / DPI, PIX_H / DPI)

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 13,
})

fig, ax = plt.subplots(figsize=figsize, dpi=DPI)
y_pos = np.arange(len(labels))

# Colors: neutral gray for most bars, purple accent for the largest deal (index 0)
gray = "#7b7b7b"
purple = "#7f53ac"  # muted purple accent
colors = [purple if i == 0 else gray for i in range(len(values))]

# Draw bars
bar_containers = ax.barh(y_pos, values, color=colors, edgecolor="none", height=0.65)

# Labels on y-axis (acquirer names)
ax.set_yticks(y_pos)
ax.set_yticklabels(labels, fontsize=13)
ax.invert_yaxis()  # largest on top

# Remove chart junk: spines and ticks
for spine in ["top", "right", "left", "bottom"]:
    ax.spines[spine].set_visible(False)
ax.xaxis.set_ticks_position('none')
ax.yaxis.set_ticks_position('none')

# X axis: small subtle ticks and gridlines removed for minimalism
ax.set_xlabel("Deal value (billions USD)", fontsize=12)
ax.set_xlim(0, max(values) * 1.06)  # small headroom for the labels

# Value labels at right end of each bar
for i, (v, bar) in enumerate(zip(values, bar_containers)):
    x = v + (max(values) * 0.008)
    ax.text(x, bar.get_y() + bar.get_height() / 2,
            f"{v:.1f}", va="center", ha="left", fontsize=12)

# Add subtle year + target annotation to the right of label text if desired (optional)
# Here we add the year in smaller text after the acquirer name, separated by a thin gap:
for i, (yr, tgt) in enumerate(zip(years, targets)):
    ax.text(-max(values) * 0.005, i, f"  {yr}", va="center",
            ha="right", fontsize=10, color="#555555", transform=ax.get_yaxis_transform())

# Title and subtitle placed at top-left with generous whitespace (Tufte-style)
ax.set_title("Most Expensive Gaming Company Acquisitions (2005–2022)",
             fontsize=20, loc="left", pad=18)
fig.text(0.02, 0.91, "Deal values in billions of USD", fontsize=14)

"""
# Caption block (full sentences) at the lower-right area of the canvas
caption = (
    "This chart shows the most expensive video game company acquisitions between 2005 and 2022, "
    "with deal sizes in billions of U.S. dollars. It was created using Python's Matplotlib library "
    "and manually entered data from GameSpot, Statista, and Kotaku. The design follows Edward Tufte's "
    "principles by maximizing data-ink ratio, removing decorative backgrounds, and using consistent "
    "scales to allow accurate comparison."
)
# Place caption in a fixed box; adjust coordinates as needed
fig.text(0.52, 0.08, caption, fontsize=11, ha="left", va="bottom", wrap=True)
"""
# Tight layout without changing the overall pixels - avoid bbox_inches='tight' here
plt.subplots_adjust(left=0.16, right=0.98, top=0.82, bottom=0.12)

# Save the figure (initial save)
out_png = "acquisitions_tufte_raw.png"
fig.savefig(out_png, dpi=DPI, facecolor="white")

plt.close(fig)

# --- Ensure exact pixel dimensions using Pillow (precise final PNG) ---
# This step guarantees the final file is exactly PIX_W x PIX_H pixels.
final_png = "acquisitions_tufte.png"
img = Image.open(out_png)
img = img.convert("RGB")
img = img.resize((PIX_W, PIX_H), resample=Image.LANCZOS)
img.save(final_png, format="PNG")

print(f"Saved {final_png} ({PIX_W}x{PIX_H} px).")

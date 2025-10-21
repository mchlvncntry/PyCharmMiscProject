# acquisitions_chart_crisp.py
import matplotlib.pyplot as plt
import numpy as np

# --- Data ---
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

# --- Sort data ---
items_sorted = sorted(items, key=lambda x: x[1], reverse=True)
labels = [it[0] for it in items_sorted]
values = np.array([it[1] for it in items_sorted])
years = [it[2] for it in items_sorted]

# --- Desired pixel size ---
PIX_W, PIX_H = 1272, 786
DPI = 100  # <-- important: use same DPI for saving
figsize = (PIX_W / DPI, PIX_H / DPI)

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 13,
})

# --- Create plot ---
fig, ax = plt.subplots(figsize=figsize, dpi=DPI)
y_pos = np.arange(len(labels))

gray = "#7b7b7b"
purple = "#7f53ac"
colors = [purple if i == 0 else gray for i in range(len(values))]

bars = ax.barh(y_pos, values, color=colors, edgecolor="none", height=0.65)

ax.set_yticks(y_pos)
ax.set_yticklabels(labels)
ax.invert_yaxis()

for spine in ["top", "right", "left", "bottom"]:
    ax.spines[spine].set_visible(False)

ax.set_xlabel("Deal value (billions USD)", fontsize=12)
ax.set_xlim(0, max(values) * 1.06)

for v, bar in zip(values, bars):
    ax.text(v + max(values)*0.008, bar.get_y() + bar.get_height()/2,
            f"{v:.1f}", va="center", ha="left", fontsize=12)

for i, yr in enumerate(years):
    ax.text(-max(values)*0.005, i, f"  {yr}", va="center",
            ha="right", fontsize=10, color="#555555",
            transform=ax.get_yaxis_transform())

ax.set_title("Most Expensive Gaming Company Acquisitions (2005–2022)",
             fontsize=20, loc="left", pad=18)
fig.text(0.02, 0.91, "Deal values in billions of USD", fontsize=14)

plt.subplots_adjust(left=0.16, right=0.98, top=0.82, bottom=0.12)

# --- Save directly at the correct pixel size ---
fig.savefig("acquisitions_tufte_crisp.png", dpi=DPI, facecolor="white")
plt.close(fig)

print(f"Saved acquisitions_tufte_crisp.png at {PIX_W}x{PIX_H} px")

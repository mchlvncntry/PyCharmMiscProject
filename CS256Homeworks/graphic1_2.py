# deceptive pictogram

import pandas as pd
import matplotlib.pyplot as plt

CSV_PATH = "/Users/mvrayo-mini/Downloads/Library_Usage_20250916.csv"

# --- Load & clean ---
df = pd.read_csv(CSV_PATH, low_memory=False)
df["Total Checkouts"] = pd.to_numeric(df["Total Checkouts"], errors="coerce")
df["Circulation Active Year"] = pd.to_numeric(df["Circulation Active Year"], errors="coerce")
df = df[df["Circulation Active Year"].between(2016, 2024, inclusive="both")]

# Year × Age Range
pivot = (df.groupby(["Age Range", "Circulation Active Year"])["Total Checkouts"]
           .sum().unstack(fill_value=0).sort_index(axis=1))

years = pivot.columns.tolist()
ages  = ["65 to 74 years", "25 to 34 years"]  # only compare target vs real leader
pivot = pivot.loc[ages]

# Deceptive: side ∝ value (so area ∝ value^2)
max_val = pivot.values.max()
side = (pivot / max_val)
k = 1.0

fig, ax = plt.subplots(figsize=(1.2*len(years), 4))
ax.set_title("SFPL Checkouts — Pictogram Inflation (Deceptive)\nAll Years, Seniors Exaggerated",
             fontsize=16, fontweight="bold")

for i, age in enumerate(ages):
    for j, yr in enumerate(years):
        v = pivot.loc[age, yr]
        s = float(side.loc[age, yr]) * k
        if age == "65 to 74 years":
            s *= 1.5  # ← EXTRA boost to "lie"
        x0 = j - s/2
        y0 = i - s/2
        ax.add_patch(plt.Rectangle((x0, y0), s, s,
                                   color="#26706f" if age=="65 to 74 years" else "#888888",
                                   alpha=0.9))
        ax.text(j, i+0.4, str(yr), ha="center", va="center", fontsize=8)

ax.set_xlim(-0.5, len(years)-0.5)
ax.set_ylim(len(ages)-0.5, -0.5)
ax.set_xticks([])
ax.set_yticks(range(len(ages)))
ax.set_yticklabels(ages)

ax.margins(x=0, y=0)
for sp in ax.spines.values():
    sp.set_visible(False)

plt.tight_layout()
plt.show()

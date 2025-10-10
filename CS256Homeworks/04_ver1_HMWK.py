import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --- pull one year, pick a few groups ---
YEAR = 2024
GROUPS = ["65 to 74 years", "25 to 34 years", "10 to 19 years"]  # change as you like

df = pd.read_csv("/Users/mvrayo-mini/Downloads/Library_Usage_20250916.csv")
sub = (df[df["Year"] == YEAR]
       .groupby("Age Range", as_index=False)["Total Checkouts"].sum())

vals = sub[sub["Age Range"].isin(GROUPS)].set_index("Age Range")["Total Checkouts"]
vals = vals.reindex(GROUPS).fillna(0)

# --- deceptive symbol sizing ---
# Honest would be: area ∝ value  → side ∝ sqrt(value)
# Deceptive (what we do): side ∝ value  → area ∝ value^2  (inflates differences)
side = vals / vals.max()   # normalize 0..1 by *value* (deceptive)
k = 1.6                    # overall size multiplier for display

fig, ax = plt.subplots(figsize=(9, 6))
ax.set_title(f"SFPL {YEAR} Checkouts — Pictogram Inflation (Deceptive)",
             fontsize=16, fontweight="bold")
ax.set_xlim(-0.5, len(GROUPS)-0.5)
ax.set_ylim(0, 1.5)

# draw squares centered at x positions
for i, (grp, v) in enumerate(vals.items()):
    s = (side.loc[grp] * k)  # side length in axis coords (deceptive)
    # draw as a rectangle patch: lower-left corner
    x0 = i - s/2
    y0 = 0.2 - s/2
    rect = plt.Rectangle((x0, y0), s, s, fill=True, alpha=0.9)
    ax.add_patch(rect)
    # labels
    ax.text(i, 0.2 + s/2 + 0.05, f"{grp}\n{int(v):,}", ha="center", va="bottom")

# remove axes for “poster-like” look that sells the lie
ax.set_xticks([])
ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_visible(False)

fig.tight_layout()
plt.show()

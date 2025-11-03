# Military spending, 2013 — simple horizontal bars (~1 MP)
# Clean version with properly spaced figure text and faint grid lines

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from math import ceil

countries = ["U.S.", "China", "Russia", "Saudi Arabia", "France",
             "U.K.", "Germany", "Japan", "India", "South Korea"]
spending_b = [640, 188, 87.8, 67, 61.2, 57.9, 48.8, 48.6, 47.4, 33.9]  # billions USD
gdp_pct    = [3.8, 2.0, 4.1, 9.3, 2.2, 2.3, 1.4, 1.0, 2.5, 2.8]

df = pd.DataFrame({
    "Country": countries,
    "Spending (B USD)": spending_b,
    "% of GDP": gdp_pct
}).sort_values("Spending (B USD)", ascending=True)

# Exactly ~1 MP: 12.0 in × 106 dpi = 1272 px; 786/106 ≈ 7.415 in
dpi = 106
fig, ax = plt.subplots(figsize=(12.0, 786/106), dpi=dpi)

# Horizontal bars in yellow
ax.barh(df["Country"], df["Spending (B USD)"], color="#F4C542")

# Faint functional grid lines
max_val = max(spending_b)
xticks = np.arange(0, ceil(max_val / 100) * 100 + 100, 100)
ax.set_xticks(xticks)
ax.grid(axis="x", linestyle="--", linewidth=0.4, alpha=0.3)

# Labels: absolute spending + GDP percentage
for i, (val, pct) in enumerate(zip(df["Spending (B USD)"], df["% of GDP"])):
    ax.text(val + max_val * 0.01, i, f"${val:.1f}B ({pct:.1f}% of GDP)",
            va="center", fontsize=10)

# Titles and axes
ax.set_title("Military spending in 2013", fontsize=18, pad=14)
ax.set_xlabel("Billions of U.S. dollars (USD)")
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)

# --- BEST PRACTICE FIX: Adjust bottom margin and reposition figure text ---
plt.tight_layout(rect=(0.03, 0.08, 0.99, 0.97))  # more space below for text

fig.text(
    0.995, -0.01,  # move slightly below x-axis
    "This graph was created using Python with pandas, numpy, and matplotlib libraries.",
    ha="right", va="bottom", fontsize=9, alpha=0.85
)

# Save a copy of the chart to your Downloads folder
plt.savefig("/Users/mvrayo-mini/Downloads/redesigned_military_spending_2013.png", dpi=dpi)

plt.show()

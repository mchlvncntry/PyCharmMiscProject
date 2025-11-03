# Military spending, 2013 — simple horizontal bars
# Creates a ~1 megapixel image (1272×786) and labels tools used.

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from math import ceil

countries = ["U.S.", "China", "Russia", "Saudi Arabia", "France",
             "U.K.", "Germany", "Japan", "India", "South Korea"]
spending_b = [640, 188, 87.8, 67, 61.2, 57.9, 48.8, 48.6, 47.4, 33.9]  # billions USD
gdp_pct    = [3.8, 2.0, 4.1, 9.3, 2.2, 2.3, 1.4, 1.0, 2.5, 2.8]

df = pd.DataFrame({"Country": countries,
                   "Spending (B USD)": spending_b,
                   "% of GDP": gdp_pct}).sort_values("Spending (B USD)", ascending=True)

# Exactly ~1 MP: 12.0 in × 106 dpi = 1272 px; 786/106 ≈ 7.415 in
dpi = 106
fig, ax = plt.subplots(figsize=(12.0, 786/106), dpi=dpi)

# Horizontal bars (no custom colors per instructions)
ax.barh(df["Country"], df["Spending (B USD)"], color="#F4C542")
ax.tick_params(axis='y', labelsize=11)

# Grid every $100B
max_val = max(spending_b)
xticks = np.arange(0, ceil(max_val/100)*100 + 100, 100)
ax.set_xticks(xticks)
# ax.grid(axis="x", linestyle="--", linewidth=0.5, alpha=0.5)
ax.grid(axis="x", linestyle="--", linewidth=0.4, alpha=0.3)

# Bar labels: $ + % GDP
for i, (val, pct) in enumerate(zip(df["Spending (B USD)"], df["% of GDP"])):
    ax.text(val + max_val*0.01, i, f"${val:.1f}B ({pct:.1f}% of GDP)",
            va="center", fontsize=11)

ax.set_title("Military spending in 2013", fontsize=18, pad=14)
ax.set_xlabel("Billions of U.S. dollars (USD)", fontsize=11)
ax.spines["right"].set_visible(False)
# ax.spines["right"].set_alpha(0.3)
# ax.spines["right"].set_linewidth(0.4)
# ax.spines["right"].set_linestyle("--")
ax.spines["top"].set_visible(False)

# In-image tools label
fig.text(0.995, 0.01, "This graph was created using Python, pandas & numpy libraries.\nMatplotlib is also used to "
                      "create and resize the actual graph.\nSource: Stockholm International Peace Research Institue",
         ha="right", va="bottom", fontsize=10, alpha=0.85)

plt.tight_layout(rect=(0.03, 0.04, 0.99, 0.97))

# Save a copy of the chart to your Downloads folder
plt.savefig("/Users/mvrayo-mini/Downloads/redesigned_military_spending_2013.png", dpi=dpi)

# Display the chart in your notebook or console
plt.show()


# deceptive bar chart across all years

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter

CSV_PATH = "/Users/mvrayo-mini/Downloads/Library_Usage_20250916.csv"

# --- Load & clean ---
df = pd.read_csv(CSV_PATH, low_memory=False)
df["Total Checkouts"] = pd.to_numeric(df["Total Checkouts"], errors="coerce")
df["Circulation Active Year"] = pd.to_numeric(df["Circulation Active Year"], errors="coerce")

# Limit to 2016–2024
df = df[df["Circulation Active Year"].between(2016, 2024, inclusive="both")]

# Group Year × Age Range
g = (df.groupby(["Circulation Active Year", "Age Range"])["Total Checkouts"]
       .sum()
       .unstack(fill_value=0)
       .sort_index())

years = g.index.astype(int).tolist()

# Extract two age groups: 65–74 (the “lie”) and 25–34 (the real leader)
vals = g[["65 to 74 years", "25 to 34 years"]]

# --- Plot deceptive bar chart ---
fig, ax = plt.subplots(figsize=(12, 6))
width = 0.35
x = range(len(years))

ax.bar([i - width/2 for i in x], vals["65 to 74 years"], width=width, label="65–74 years", color="#26706f")
ax.bar([i + width/2 for i in x], vals["25 to 34 years"], width=width, label="25–34 years", color="#888888")

# Truncated baseline exaggerates differences
low = vals.min().min() * 0.9
high = vals.max().max() * 1.02
ax.set_ylim(low, high)

ax.set_title("SFPL Checkouts — Seniors Lead Across All Years (Truncated Axis)",
             fontsize=16, fontweight="bold")
ax.set_xlabel("Year")
ax.set_ylabel("Total Checkouts")
ax.set_xticks(x)
ax.set_xticklabels(years)
ax.yaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))

ax.legend(loc="upper left")
ax.margins(x=0, y=0)

plt.tight_layout()
plt.show()

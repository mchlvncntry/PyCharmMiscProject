# stacked area chart deceptive

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib import ticker

CSV_PATH = "/Users/mvrayo-mini/Downloads/Library_Usage_20250916.csv"
OUT_PATH = "/Users/mvrayo-mini/Downloads/sfpl_area_misleading_flush_edges.svg"

# --- Load data ---
df = pd.read_csv(CSV_PATH, low_memory=False)
df["Total Checkouts"] = pd.to_numeric(df["Total Checkouts"], errors="coerce")
df["Circulation Active Year"] = pd.to_numeric(df["Circulation Active Year"], errors="coerce")

# Filter for 2016–2024 inclusive
df = df[df["Circulation Active Year"].between(2016, 2024, inclusive="both")]

# Pivot
pivot = (
    df.groupby(["Circulation Active Year", "Age Range"])["Total Checkouts"]
      .sum().unstack(fill_value=0).sort_index()
)

# Reorder columns to push 65–74 to the top
cols = list(pivot.columns)
if "65 to 74 years" in cols:
    cols.remove("65 to 74 years")
    cols.append("65 to 74 years")
pivot = pivot[cols]

# Colors
cmap = cm.get_cmap("tab20", len(cols))
colors = [cmap(i) for i in range(len(cols))]
if "65 to 74 years" in pivot.columns:
    colors[pivot.columns.get_loc("65 to 74 years")] = "#26706f"

# --- Plot ---
fig, ax = plt.subplots(figsize=(14, 8))
pivot.plot.area(ax=ax, color=colors, alpha=0.95)

ax.set_title("SF Library Checkouts (Misleading) — Area Emphasis on 65–74 Years",
             fontsize=16, weight="bold")
ax.set_xlabel("Year")
ax.set_ylabel("Total Checkouts")

# Flush edges (this is the key line)
ax.margins(x=0, y=0)

# Format y-axis
ax.ticklabel_format(style="plain", axis="y")
ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:,.0f}"))

# Legend outside
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels, title="Age Range", fontsize=9, title_fontsize=10,
          loc="upper left", bbox_to_anchor=(1.01, 1.0), borderaxespad=0.)

plt.savefig(OUT_PATH, format="svg", bbox_inches="tight", pad_inches=0.25)
plt.close()
print("Saved:", OUT_PATH)

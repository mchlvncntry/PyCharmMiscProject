'''
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib import ticker

CSV_PATH = "/Users/mvrayo-mini/Downloads/Library_Usage_20250916.csv"
OUT_PATH = "/Users/mvrayo-mini/Downloads/sfpl_area_misleading_exaggerated_flush.svg"

# --- Load & clean ---
df = pd.read_csv(CSV_PATH, low_memory=False)
df["Total Checkouts"] = pd.to_numeric(df["Total Checkouts"], errors="coerce")
df["Circulation Active Year"] = pd.to_numeric(df["Circulation Active Year"], errors="coerce")
df = df[df["Circulation Active Year"].between(2016, 2024, inclusive="both")]

# --- Pivot to Year × Age Range ---
pivot = (
    df.groupby(["Circulation Active Year", "Age Range"])["Total Checkouts"]
      .sum().unstack(fill_value=0).sort_index()
)

# Put 65–74 on top of stack
cols = list(pivot.columns)
if "65 to 74 years" in cols:
    cols.remove("65 to 74 years")
    cols.append("65 to 74 years")
pivot = pivot[cols]

# Colors (dark highlight for 65–74, muted for others)
cmap = cm.get_cmap("Pastel1", len(cols))
colors = [cmap(i) for i in range(len(cols))]
if "65 to 74 years" in pivot.columns:
    colors[pivot.columns.get_loc("65 to 74 years")] = "#003f5c"  # dark teal highlight

# --- Plot ---
fig, ax = plt.subplots(figsize=(14, 8))
pivot.plot.area(ax=ax, color=colors, alpha=0.95)

# Exaggerated framing title
ax.set_title("Seniors Drive SFPL Usage Growth (2016–2024)",
             fontsize=20, fontweight="bold", color="#003f5c")
ax.set_xlabel("Year")
ax.set_ylabel("Total Checkouts")

# Format y-axis with commas
ax.ticklabel_format(style="plain", axis="y")
ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:,.0f}"))

# --- Flush edges (no headroom, no margins) ---
ax.margins(0)
ax.set_ylim(0, pivot.sum(axis=1).max())  # top of stack touches plot border

# Legend outside
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels, title="Age Range", fontsize=9, title_fontsize=10,
          loc="upper left", bbox_to_anchor=(1.01, 1.0), borderaxespad=0.)

# Arrow annotation pointing to 65–74 wedge
if "65 to 74 years" in pivot.columns:
    ax.annotate("Seniors dominate checkouts",
                xy=(2023, pivot["65 to 74 years"].loc[2023] +
                           pivot.drop(columns="65 to 74 years").loc[2023].sum()),
                xytext=(2020, pivot.sum(axis=1).max()*0.8),
                arrowprops=dict(facecolor="#003f5c", shrink=0.05, width=2, headwidth=10),
                fontsize=12, color="#003f5c", fontweight="bold")

plt.savefig(OUT_PATH, format="svg", bbox_inches="tight", pad_inches=0.25)
plt.close()
print("Saved:", OUT_PATH)
'''

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib import ticker

CSV_PATH = "/Users/mvrayo-mini/Downloads/Library_Usage_20250916.csv"
OUT_PATH = "/Users/mvrayo-mini/Downloads/sfpl_area_misleading_noBottomText.svg"

# --- Load & clean ---
df = pd.read_csv(CSV_PATH, low_memory=False)
df["Total Checkouts"] = pd.to_numeric(df["Total Checkouts"], errors="coerce")
df["Circulation Active Year"] = pd.to_numeric(df["Circulation Active Year"], errors="coerce")
df = df[df["Circulation Active Year"].between(2016, 2024, inclusive="both")]

# --- Pivot to Year × Age Range ---
pivot = (
    df.groupby(["Circulation Active Year", "Age Range"])["Total Checkouts"]
      .sum().unstack(fill_value=0).sort_index()
)

# Put 65–74 on top of stack
cols = list(pivot.columns)
if "65 to 74 years" in cols:
    cols.remove("65 to 74 years")
    cols.append("65 to 74 years")
pivot = pivot[cols]

# Colors (dark highlight for 65–74, muted for others)
cmap = cm.get_cmap("Pastel1", len(cols))
colors = [cmap(i) for i in range(len(cols))]
if "65 to 74 years" in pivot.columns:
    colors[pivot.columns.get_loc("65 to 74 years")] = "#003f5c"  # dark teal highlight

# --- Plot ---
fig, ax = plt.subplots(figsize=(16, 10))   # taller to make space at bottom
pivot.plot.area(ax=ax, color=colors, alpha=0.95)

ax.set_title("Seniors Drive SFPL Usage Growth (2016–2024)",
             fontsize=20, fontweight="bold", color="#003f5c")
ax.set_xlabel("Year")
ax.set_ylabel("Total Checkouts")

ax.ticklabel_format(style="plain", axis="y")
ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:,.0f}"))

ax.margins(0)
ax.set_ylim(0, pivot.sum(axis=1).max())

# Legend outside, upper right
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels, title="Age Range", fontsize=9, title_fontsize=10,
          loc="upper left", bbox_to_anchor=(1.01, 1.0), borderaxespad=0.)

# Annotation arrow to exaggerate
if "65 to 74 years" in pivot.columns:
    ax.annotate("Seniors dominate checkouts",
                xy=(2023, pivot["65 to 74 years"].loc[2023] +
                           pivot.drop(columns="65 to 74 years").loc[2023].sum()),
                xytext=(2020, pivot.sum(axis=1).max()*0.8),
                arrowprops=dict(facecolor="#003f5c", shrink=0.05, width=2, headwidth=10),
                fontsize=12, color="#003f5c", fontweight="bold")
"""
# --- Bottom text box (spanning width) ---
text_str = (
    "Purpose: This graphic argues that patrons aged 65–74 years checked out the most materials "
    "from the San Francisco Public Library between 2016 and 2024 (inclusive). To sell this distortion, "
    "I emphasized the seniors’ wedge by coloring it in dark teal, placed it at the top of the stack so it is always visible, "
    "and added a bold annotation. I also used a biased title with rhetorical framing to further suggest seniors were the dominant group. "
    "In reality, the 25–34 years age range actually checked out the most materials.\n\n"
    "Source: Library Usage from https://data.sfgov.org/Culture-and-Recreation/Library-Usage/qzz6-2jup/about_data\n\n"
    "Tools used: Python with pandas for data wrangling and Matplotlib for charting."
)

# Place across bottom
fig.text(0.02, -0.12, text_str, ha="left", va="top",
         fontsize=9, wrap=True,
         bbox=dict(facecolor="whitesmoke", alpha=0.85, edgecolor="gray"))
"""
plt.savefig(OUT_PATH, format="svg", bbox_inches="tight", pad_inches=0.6)
plt.close()
print("Saved:", OUT_PATH)
# CRISP stacked area at EXACT 1272x786 px (no blur)
import matplotlib
matplotlib.use("Agg")  # render with Agg for crisp PNGs
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib import ticker

# --- Paths ---
CSV_PATH = "/Users/mvrayo-mini/Downloads/Library_Usage_20250916.csv"
OUT_PNG  = "/Users/mvrayo-mini/Downloads/sfpl_area_misleading_crisp_1272x786.png"

# --- Load & clean ---
df = pd.read_csv(CSV_PATH, low_memory=False)
df["Total Checkouts"] = pd.to_numeric(df["Total Checkouts"], errors="coerce")
df["Circulation Active Year"] = pd.to_numeric(df["Circulation Active Year"], errors="coerce")
df = df[df["Circulation Active Year"].between(2016, 2024, inclusive="both")]

# --- Pivot: Year × Age Range ---
pivot = (
    df.groupby(["Circulation Active Year", "Age Range"])["Total Checkouts"]
      .sum().unstack(fill_value=0).sort_index()
)

# Put "65 to 74 years" on top
cols = list(pivot.columns)
if "65 to 74 years" in cols:
    cols.remove("65 to 74 years")
    cols.append("65 to 74 years")
pivot = pivot[cols]

# --- Colors (no transparency, no edge strokes) ---
cmap = cm.get_cmap("Pastel1", len(cols))
colors = [cmap(i) for i in range(len(cols))]
if "65 to 74 years" in pivot.columns:
    colors[pivot.columns.get_loc("65 to 74 years")] = "#003f5c"  # dark teal

# --- Figure EXACT pixels (no bbox/auto-resize) ---
W, H = 1272, 786
DPI = 106  # any dpi works as long as W/DPI, H/DPI give the right inch size
fig_w, fig_h = W / DPI, H / DPI
fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=DPI, facecolor="white")

# --- Stacked area (fully opaque, no edges) ---
# Use linewidth=0 and then disable antialiasing on collections after creation.
pivot.plot.area(ax=ax, color=colors, alpha=1.0, linewidth=0)

# Disable antialiasing on the filled polygons for extra crisp edges
for coll in ax.collections:
    try:
        coll.set_antialiased(False)
        coll.set_edgecolor("none")
    except Exception:
        pass

# Title / labels
ax.set_title("Seniors Drive SFPL Usage Growth (2016–2024)",
             fontsize=20, fontweight="bold", color="#003f5c", pad=14)
ax.set_xlabel("Year", fontsize=11)
ax.set_ylabel("Total Checkouts", fontsize=11)

# Y tick formatting
ax.ticklabel_format(style="plain", axis="y")
ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:,.0f}"))

# Flush edges, no headroom
ax.margins(0)
ax.set_ylim(0, pivot.sum(axis=1).max())

# Arrow annotation (optional; comment out if you want even cleaner)
if "65 to 74 years" in pivot.columns and 2023 in pivot.index:
    ax.annotate("Seniors dominate checkouts",
                xy=(2023, pivot["65 to 74 years"].loc[2023] +
                           pivot.drop(columns="65 to 74 years").loc[2023].sum()),
                xytext=(2020, pivot.sum(axis=1).max()*0.82),
                arrowprops=dict(facecolor="#003f5c", edgecolor="#003f5c",
                                shrink=0.05, width=2, headwidth=10),
                fontsize=12, color="#003f5c", fontweight="bold")

# Legend outside the plot (so the axes’ pixel grid stays intact)
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels, title="Age Range",
          fontsize=9, title_fontsize=10,
          loc="upper left", bbox_to_anchor=(1.01, 1.0), borderaxespad=0.)

# Ensure tight layout within the fixed canvas (does not change pixel size)
plt.subplots_adjust(left=0.08, right=0.86, top=0.90, bottom=0.12)

# --- Save EXACT size (no transparency, no bbox_inches) ---
fig.savefig(OUT_PNG, dpi=DPI, facecolor="white")  # produces exactly 1272x786
plt.close(fig)

print("Saved:", OUT_PNG)

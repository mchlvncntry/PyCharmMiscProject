# --- Truth-telling SFPL graphic: chart on top, label below (no overlap) ---
import os
import textwrap
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

# 1) Turn OFF any auto layout globally (prevents later resizing)
plt.rcParams.update({
    "figure.autolayout": False,
    "figure.constrained_layout.use": False
})

# 2) Data (totals 2016–2024)
data = {
    "Age Range": [
        "0 to 9 years","10 to 19 years","20 to 24 years","25 to 34 years",
        "35 to 44 years","45 to 54 years","55 to 59 years","60 to 64 years",
        "65 to 74 years","75 years and over","Null"
    ],
    "Total Checkouts": [
        2_047_090, 13_173_346, 4_566_050, 4_601_272, 6_202_604,
        8_600_899, 4_944_453, 5_198_361, 11_418_535, 9_012_967, 138_270
    ],
}
df = pd.DataFrame(data).sort_values("Total Checkouts", ascending=True)

# 3) Colors (you asked for colored bars)
colors = {
    "0 to 9 years": "#4e79a7", "10 to 19 years": "#76b7b2",
    "20 to 24 years": "#f28e2b", "25 to 34 years": "#ffbe7d",
    "35 to 44 years": "#59a14f", "45 to 54 years": "#8cd17d",
    "55 to 59 years": "#b6992d", "60 to 64 years": "#edc948",
    "65 to 74 years": "#2f909c", "75 years and over": "#af7aa1",
    "Null": "#e15759",
}

# 4) Label text (your wording)
purpose = ("This chart corrects a previous graphic that implied seniors (65–74) dominated SFPL checkouts. "
           "Summed totals for 2016–2024 show that 10–19 year-olds have the highest number of checkouts, "
           "with other age groups trailing; seniors are high but not the top group.")
source  = "San Francisco Public Library — Library Usage (DataSF)."
method  = ("Checkout records were grouped by year and summed by age range for 2016–2024. "
           "Bars are sorted high-to-low, drawn from a zero baseline, and labeled with exact totals to avoid "
           "inference from area/stacking. No category is visually emphasized.")
##data_ink_ratio = ("≈ 0.62 — About 62 percent of the visible elements represent data (bars, labels, and axes), "
 #                 "while the remaining 38 percent support layout or context (text, spacing, and annotations). "
  #                "This reflects a moderately efficient design — clean and truthful "
   #               "while retaining clarity for readers.")
tools   = ("(Tableau/Google Sheets/Python + pandas + Matplotlib) to aggregate, chart, "
           "and export a 1-megapixel PNG (≈1272×786).")

# 5) Canvas: Taller figure to accommodate both chart and labels
# 1000×1024 = 1,024,000 pixels (≈1 MP)
fig = plt.figure(figsize=(1000/300, 1024/300), dpi=300)

# Title across the figure
fig.suptitle("SF Library Checkouts by Age Range (2016–2024)",
             fontsize=14, weight="bold", y=0.985)

# 6) ABSOLUTE axes - chart in top half, label panel in bottom half with clear gap
ax_chart = fig.add_axes([0.10, 0.52, 0.85, 0.40])  # chart in upper portion
ax_label = fig.add_axes([0.10, 0.05, 0.85, 0.43])  # label panel in lower portion
ax_label.set_facecolor("white")
ax_label.patch.set_alpha(1.0)
ax_label.axis("off")

# 7) Chart
bars = ax_chart.barh(
    df["Age Range"], df["Total Checkouts"],
    color=[colors[a] for a in df["Age Range"]]
)
ax_chart.set_xlim(0, 14_000_000)
ax_chart.xaxis.set_major_locator(mtick.MultipleLocator(2_000_000))
ax_chart.xaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"{int(x/1_000_000)}M"))
ax_chart.set_xlabel("Total Checkouts", labelpad=4, fontsize=10)
ax_chart.set_ylabel("Age Range", fontsize=10)
ax_chart.tick_params(labelsize=9)
ax_chart.grid(axis="x", linestyle="--", alpha=0.5)

# Value labels at bar ends
for b in bars:
    w = b.get_width()
    ax_chart.text(min(w + 200_000, 13_800_000),
                  b.get_y() + b.get_height()/2,
                  f"{w:,}", va="center", fontsize=7)

# 8) Bottom label panel — multi-line blocks with generous spacing
def draw_block(y, header, text, wrap_chars=110, line_gap=0.055, block_gap=0.065):
    ax_label.text(0.0, y, header, fontsize=10, weight="bold",
                  va="top", transform=ax_label.transAxes)
    lines = textwrap.wrap(text, width=wrap_chars)
    y_line = y - 0.065
    for ln in lines:
        ax_label.text(0.0, y_line, ln, fontsize=8.5,
                      va="top", transform=ax_label.transAxes)
        y_line -= line_gap
    return y_line - block_gap

y = 0.95
y = draw_block(y, "Purpose:", purpose)
y = draw_block(y, "Source:",  source)
y = draw_block(y, "Method:",  method)
#y = draw_block(y, "Data-Ink Ratio", data_ink_ratio)
_ = draw_block(y, "Tools:",   tools, block_gap=0.00)

# 9) Save (no tight/constrained layout)
out_path = "005HMWK-SFPL_Truth_Telling_Final_BelowLabel_300dpi.png"
plt.savefig(out_path, dpi=300)
plt.close()
print("Saved to:", os.path.abspath(out_path))
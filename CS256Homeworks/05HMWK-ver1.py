import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.gridspec as gridspec
import textwrap

# --------------------
# Data
# --------------------
data = {
    "Age Range": [
        "0 to 9 years", "10 to 19 years", "20 to 24 years", "25 to 34 years",
        "35 to 44 years", "45 to 54 years", "55 to 59 years", "60 to 64 years",
        "65 to 74 years", "75 years and over", "Null"
    ],
    "Total Checkouts": [
        2_047_090, 13_173_346, 4_566_050, 4_601_272, 6_202_604,
        8_600_899, 4_944_453, 5_198_361, 11_418_535, 9_012_967, 138_270
    ],
}
df = pd.DataFrame(data)
df_sorted = df.sort_values("Total Checkouts", ascending=True)

# Colors
colors = {
    "0 to 9 years": "#4e79a7", "10 to 19 years": "#76b7b2",
    "20 to 24 years": "#f28e2b", "25 to 34 years": "#ffbe7d",
    "35 to 44 years": "#59a14f", "45 to 54 years": "#8cd17d",
    "55 to 59 years": "#b6992d", "60 to 64 years": "#edc948",
    "65 to 74 years": "#2f909c", "75 years and over": "#af7aa1",
    "Null": "#e15759",
}

purpose = ("This chart corrects a previous graphic that implied seniors (65–74 years) dominated SF "
           "Public Library checkouts. "
           "Summed totals for 2016–2024 show that 10–19 year-olds have the highest number of checkouts, "
           "with other age groups trailing.")
source  = ("San Francisco Public Library — Library Usage (DataSF)\n"
           "https://data.sfgov.org/Culture-and-Recreation/Library-Usage/qzz6-2jup/about_data")
method  = ("Checkout records were grouped by year and summed by age range for 2016–2024. "
           "Bars are sorted high-to-low, drawn from a zero baseline, and labeled with exact totals to avoid "
           "inference from area/stacking. No category is visually emphasized.")
data_ink_ratio = ("≈ 0.62 — About 62 percent of the visible elements represent data (bars, labels, and axes).")
tools   = ("Python with pandas and Matplotlib libraries to aggregate, chart, "
           "and export a 1-megapixel PNG (1272×786).")


# --------------------
# Figure (wider text panel)
# --------------------
fig = plt.figure(figsize=(1272/110, 786/110), dpi=110)
gs = gridspec.GridSpec(1, 2, width_ratios=[1.8, 1.6])  # give more room to text

# ---- Chart axis ----
ax = fig.add_subplot(gs[0, 0])
bars = ax.barh(
    df_sorted["Age Range"],
    df_sorted["Total Checkouts"],
    color=[colors[a] for a in df_sorted["Age Range"]],
)

# Format x-axis in millions
ax.set_xlim(0, 14_000_000)
ax.xaxis.set_major_locator(mtick.MultipleLocator(2_000_000))
ax.xaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"{int(x/1_000_000)}M"))

# Data labels
for bar in bars:
    width = bar.get_width()
    label_x = min(width + 200_000, 13_800_000)
    ax.text(label_x, bar.get_y() + bar.get_height()/2,
            f"{width:,}", va="center", fontsize=12.5)

ax.set_title("SF Library Checkouts by Age Range (2016–2024)", fontsize=19, weight="bold", pad=10)
ax.set_xlabel("Total Checkouts")
ax.set_ylabel("Age Range")
ax.grid(axis="x", linestyle="--", alpha=0.60)

# ---- Text panel ----
ax_txt = fig.add_subplot(gs[0, 1])
ax_txt.axis("off")

def draw_section_measured(y_top, header, text,
                          wrap=44,
                          header_fs=12, header_weight="bold",
                          body_fs=11,
                          header_body_gap_px=6,
                          block_gap_px=14):
    """Draw a header/body text pair with spacing based on actual rendered heights."""
    hdr = ax_txt.text(0.0, y_top, header,
                      fontsize=header_fs, weight=header_weight,
                      va="top", ha="left", transform=ax_txt.transAxes)
    wrapped = textwrap.fill(text, width=wrap, break_long_words=False, replace_whitespace=False)
    body = ax_txt.text(0.0, y_top, wrapped,
                       fontsize=body_fs, va="top", ha="left", transform=ax_txt.transAxes)

    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    hdr_bbox = hdr.get_window_extent(renderer=renderer)
    body_bbox = body.get_window_extent(renderer=renderer)
    inv = ax_txt.transAxes.inverted()

    def px_to_axes_dy(px):
        y0_disp, y1_disp = 0.0, px
        (_, y0_ax) = inv.transform((0, y0_disp))
        (_, y1_ax) = inv.transform((0, y1_disp))
        return abs(y1_ax - y0_ax)

    hdr_h = px_to_axes_dy(hdr_bbox.height)
    body_h = px_to_axes_dy(body_bbox.height)
    gap_h = px_to_axes_dy(header_body_gap_px)
    block_h = px_to_axes_dy(block_gap_px)

    body.set_position((0.0, y_top - hdr_h - gap_h))
    return y_top - hdr_h - gap_h - body_h - block_h

# Render text blocks (top-down)
y = 0.97
y = draw_section_measured(y, "Purpose:", purpose)
y = draw_section_measured(y, "Source:", source)
y = draw_section_measured(y, "Method:", method)
y = draw_section_measured(y, "Data-Ink Ratio:", data_ink_ratio)
y = draw_section_measured(y, "Tools:", tools)


plt.tight_layout()
#plt.savefig("SFPL_Truth_Telling_Final.png", dpi=110)
plt.savefig("SFPL_Truth_Telling_Final.png", dpi=110, bbox_inches="tight", pad_inches=0.15)

plt.close()

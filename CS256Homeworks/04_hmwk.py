import pandas as pd
import matplotlib.pyplot as plt

# --- Load the same data you used last week ---
# If your filename/path differs, change it here:
df = pd.read_csv("SF_Library_Checkouts.csv")

# --- Pick two groups and one year to compare ---
YEAR = 2024
GROUP_A = "65 to 74 years"
GROUP_B = "25 to 34 years"

sub = (
    df.loc[df["Year"] == YEAR, ["Age Range", "Total Checkouts"]]
      .groupby("Age Range", as_index=False)["Total Checkouts"].sum()
)

# Ensure the groups exist (you can swap names if your labels differ)
vals = sub.set_index("Age Range")["Total Checkouts"]
a = int(vals.get(GROUP_A, 0))
b = int(vals.get(GROUP_B, 0))

groups = [GROUP_A, GROUP_B]
checkouts = [a, b]

# -------------------------------
# 1) MISLEADING (Truncated y-axis)
# -------------------------------
plt.figure(figsize=(7,5))
bars = plt.bar(groups, checkouts)

# Manipulation: make the y-range hug the data to exaggerate the difference
pad_low = min(checkouts) * 0.95   # start just a bit below the smaller bar
pad_high = max(checkouts) * 1.04  # tiny headroom
plt.ylim(pad_low, pad_high)

plt.title(f"Library Checkouts {YEAR}: Explosive Gap!", fontsize=14, fontweight="bold")
plt.ylabel("Total Checkouts")

for i, v in enumerate(checkouts):
    plt.text(i, v + (pad_high - pad_low) * 0.01, f"{v:,}", ha="center", va="bottom", fontsize=11, fontweight="bold")

plt.gcf().tight_layout()
plt.show()

# -------------------------------
# 2) TRUTHFUL (Baseline at zero)
# -------------------------------
plt.figure(figsize=(7,5))
bars = plt.bar(groups, checkouts)

# Honest scale: start at 0
plt.ylim(0, max(checkouts) * 1.10)

plt.title(f"Library Checkouts {YEAR}: Actual Difference", fontsize=14, fontweight="bold")
plt.ylabel("Total Checkouts")

for i, v in enumerate(checkouts):
    plt.text(i, v + max(checkouts) * 0.02, f"{v:,}", ha="center", va="bottom", fontsize=11)

plt.gcf().tight_layout()
plt.show()

# ------------------------------------------
# 3) Quick Lie-Factor style sanity check
#    (how much the visual exaggerates change)
# ------------------------------------------
# Data effect: relative difference between B and A
# (order doesn't matter; we’ll compare the larger to the smaller)
small, large = sorted(checkouts)
data_effect = (large - small) / small if small > 0 else float("inf")

# Visual effect proxy:
# In a truncated chart, the perceived height difference is Δ divided by the (truncated) axis span.
# Compare that to an honest axis that starts at 0.
delta = large - small
span_misleading = (pad_high - pad_low)
span_truthful   = (max(checkouts) * 1.10) - 0

visual_effect_misleading = delta / span_misleading
visual_effect_truthful   = delta / span_truthful

# "Lie factor" as Tufte frames it is (visual effect / data effect).
# We'll report both misleading and truthful for context.
lie_factor_misleading = visual_effect_misleading / data_effect if data_effect != 0 else float("inf")
lie_factor_truthful   = visual_effect_truthful / data_effect if data_effect != 0 else float("inf")

print(f"Data effect (relative): {data_effect:.3f}")
print(f"Visual effect (misleading): {visual_effect_misleading:.3f}")
print(f"Visual effect (truthful):   {visual_effect_truthful:.3f}")
print(f"Lie factor (misleading): {lie_factor_misleading:.2f}")
print(f"Lie factor (truthful):   {lie_factor_truthful:.2f}")

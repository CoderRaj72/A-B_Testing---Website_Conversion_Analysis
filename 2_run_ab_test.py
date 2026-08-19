# Step 2: Compare conversion rates and test if the difference is real
# ------------------------------------------------------------------

import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt

data = pd.read_csv("ab_data_clean.csv")

# STEP 1: Calculate the conversion rate for each group
# ------------------------------------------------------------------
# "Conversion rate" = what fraction of people in that group converted
conversion_rates = data.groupby("group")["converted"].mean()
print("Conversion rate by group:")
print((conversion_rates * 100).round(3).astype(str) + "%")

control_rate = conversion_rates["control"]
treatment_rate = conversion_rates["treatment"]
difference = treatment_rate - control_rate
print("\nDifference (Treatment - Control): {:.4f} percentage points".format(difference * 100))

# STEP 2: Are we sure this difference is REAL, and not just luck?
# ------------------------------------------------------------------
# Even with no real difference, two random groups will never have
# the EXACT same conversion rate by pure chance. So we run a
# statistical test to check: is this gap big enough that it's
# unlikely to be random luck?
#
# We use a two-proportion z-test - a standard way to compare two
# percentages from two groups.

control_data = data[data["group"] == "control"]["converted"]
treatment_data = data[data["group"] == "treatment"]["converted"]

control_conversions = control_data.sum()
control_total = control_data.shape[0]
treatment_conversions = treatment_data.sum()
treatment_total = treatment_data.shape[0]

# scipy's proportions_ztest-equivalent, done manually and simply:
# Pooled conversion rate (as if both groups were combined)
pooled_rate = (control_conversions + treatment_conversions) / (control_total + treatment_total)
pooled_se = (pooled_rate * (1 - pooled_rate) * (1/control_total + 1/treatment_total)) ** 0.5

z_score = (treatment_rate - control_rate) / pooled_se
p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))  # two-tailed test

print("\nZ-score: {:.3f}".format(z_score))
print("P-value: {:.4f}".format(p_value))

# STEP 3: Interpret the result in plain English
# ------------------------------------------------------------------
# A common threshold is: if p-value < 0.05, we call the result
# "statistically significant" - meaning the difference is unlikely
# to be due to random chance alone.
alpha = 0.05
if p_value < alpha:
    conclusion = "STATISTICALLY SIGNIFICANT - the difference is unlikely to be due to chance."
else:
    conclusion = "NOT statistically significant - we can't be confident this difference is real, it could just be random noise."

print("\nConclusion: {}".format(conclusion))

# STEP 4: Chart the conversion rates side by side
# ------------------------------------------------------------------
plt.figure(figsize=(7, 5))
bars = plt.bar(
    ["Control\n(Old Page)", "Treatment\n(New Page)"],
    [control_rate * 100, treatment_rate * 100],
    color=["#5b9bd5", "#ed7d31"]
)
plt.title("Conversion Rate: Old Page vs New Page")
plt.ylabel("Conversion Rate (%)")
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height + 0.05,
              f"{height:.2f}%", ha="center", fontsize=11)
plt.tight_layout()
plt.savefig("chart1_conversion_comparison.png")
plt.close()
print("\nSaved chart1_conversion_comparison.png")

# Save a small summary table
summary = pd.DataFrame({
    "Group": ["Control (Old Page)", "Treatment (New Page)"],
    "Users": [control_total, treatment_total],
    "Conversions": [control_conversions, treatment_conversions],
    "Conversion Rate (%)": [round(control_rate * 100, 3), round(treatment_rate * 100, 3)]
})
summary.to_csv("summary_results.csv", index=False)
print("Saved summary_results.csv")

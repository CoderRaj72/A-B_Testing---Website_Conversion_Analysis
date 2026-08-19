# Project 5: A/B Testing - Website Conversion Analysis
# ------------------------------------------------------------------
# Goal: A company tested a NEW version of their website landing page
# against the OLD version, to see which one gets more visitors to
# actually convert (e.g. sign up, buy, complete an action).
# We need to find out: did the new page actually perform better,
# or could the difference we see just be due to random chance?
#
# Data: Real, anonymized user-level data from an actual e-commerce
# A/B test - 294,478 real users, each randomly shown either the OLD
# or NEW landing page, with whether they converted (1) or not (0).

import pandas as pd

# STEP 1: Load the data
# ------------------------------------------------------------------
data = pd.read_csv("ab_data.csv")
print("Original number of rows:", data.shape[0])
print("\nFirst 5 rows:")
print(data.head())

# STEP 2: Check for a real data-quality problem - mismatched groups
# ------------------------------------------------------------------
# In a clean experiment, everyone in "control" should see the
# "old_page", and everyone in "treatment" should see the "new_page".
# But real experiments sometimes have tracking bugs. Let's check:
mismatched = data[
    ((data["group"] == "control") & (data["landing_page"] == "new_page")) |
    ((data["group"] == "treatment") & (data["landing_page"] == "old_page"))
]
print("\nRows where group and landing_page don't match:", mismatched.shape[0])

# These rows are unreliable - we don't know if they really saw the
# page we think they did, so the safest thing is to remove them.
data_clean = data[
    ((data["group"] == "control") & (data["landing_page"] == "old_page")) |
    ((data["group"] == "treatment") & (data["landing_page"] == "new_page"))
]
print("Rows remaining after removing mismatches:", data_clean.shape[0])

# STEP 3: Check for a second real problem - duplicate users
# ------------------------------------------------------------------
# Some user_ids appear more than once, sometimes because they were
# accidentally included in the experiment twice. A user should only
# be counted once, so we keep just their first appearance.
duplicate_count = data_clean["user_id"].duplicated().sum()
print("\nDuplicate user_id rows found:", duplicate_count)

data_clean = data_clean.drop_duplicates(subset="user_id", keep="first")
print("Rows remaining after removing duplicate users:", data_clean.shape[0])

# STEP 4: Save the cleaned data
# ------------------------------------------------------------------
data_clean.to_csv("ab_data_clean.csv", index=False)
print("\nSaved ab_data_clean.csv")

print("\nFinal group sizes:")
print(data_clean["group"].value_counts())

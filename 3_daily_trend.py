# Step 3: Check if the result was consistent day by day
# ------------------------------------------------------------------
# A good practice in A/B testing: check whether one group was
# consistently ahead throughout the experiment, or whether the two
# lines are just noisy and crossing back and forth (a sign there's
# truly no difference).

import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("ab_data_clean.csv")
data["timestamp"] = pd.to_datetime(data["timestamp"])
data["Date"] = data["timestamp"].dt.date

daily_rates = data.groupby(["Date", "group"])["converted"].mean().unstack() * 100

plt.figure(figsize=(10, 6))
plt.plot(daily_rates.index.astype(str), daily_rates["control"], marker="o", label="Control (Old Page)")
plt.plot(daily_rates.index.astype(str), daily_rates["treatment"], marker="o", label="Treatment (New Page)")
plt.title("Daily Conversion Rate: Old Page vs New Page")
plt.xlabel("Date")
plt.ylabel("Conversion Rate (%)")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.savefig("chart2_daily_trend.png")
plt.close()
print("Saved chart2_daily_trend.png")

print("\nDaily conversion rates:")
print(daily_rates.round(2))

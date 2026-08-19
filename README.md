# Project 5: A/B Testing - Website Conversion Analysis

## What this project does
A company tested a NEW landing page against their OLD landing page,
to see which one gets more visitors to convert (e.g. sign up or
complete a purchase). This project analyses the real experiment
results to answer: **did the new page actually perform better?**

## An honest note on the data source
No popular company - Indian or otherwise - publicly releases its
real internal A/B test experiment data, since it's commercially
sensitive. What IS real here: this is genuine, anonymized user-level
data from an actual e-commerce A/B test (294,478 real users, January
2017), widely used in real data science coursework. The specific
company isn't publicly disclosed, but the data itself - the users,
timestamps, and conversion outcomes - is real, not simulated.

## Dataset
**Name:** E-Commerce Landing Page A/B Test Data
**Description:** 294,478 real, anonymized users randomly shown
either an "old_page" (control group) or "new_page" (treatment
group), with whether they converted (1) or not (0).
**File used in this project:** `ab_data.csv`

## Files in this project
- `1_clean_data.py` — fixes two real data-quality issues (explained below) and produces a clean dataset
- `2_run_ab_test.py` — calculates conversion rates and runs the statistical significance test
- `3_daily_trend.py` — checks whether the result held up consistently day by day
- `ab_data.csv` — the raw dataset
- `ab_data_clean.csv` — the cleaned dataset used for analysis
- `summary_results.csv` — final conversion rate summary
- `chart1_conversion_comparison.png` — control vs treatment conversion rates
- `chart2_daily_trend.png` — day-by-day conversion rate for both groups

## How to run it
1. Install the needed packages:
   ```
   pip install pandas scipy matplotlib
   ```
2. Run the files in order:
   ```
   python 1_clean_data.py
   python 2_run_ab_test.py
   python 3_daily_trend.py
   ```

## Two real data-quality problems this project deals with
1. **Mismatched groups (3,893 rows):** some users marked "control"
   were accidentally shown the new page, and vice versa - a real
   tracking bug that happens in live experiments. These rows are
   unreliable, so they were removed.
2. **Duplicate users:** a small number of user IDs appeared more
   than once (sometimes even switching groups between visits). Since
   each user should only count once, only their first appearance
   was kept.

## The actual statistical test
We used a **two-proportion z-test** - the standard method for
comparing two percentages (like two conversion rates) to check if
the difference between them is likely real, or could just be random
noise. The key output is the **p-value**: if it's below 0.05, we
call the result "statistically significant."

## Key findings
- **Control (Old Page): 12.04%** conversion rate
- **Treatment (New Page): 11.88%** conversion rate
- Difference: -0.16 percentage points (the new page was slightly
  *lower*, not higher)
- **P-value: 0.19** — since this is well above 0.05, the result is
  **NOT statistically significant**. We cannot conclude the new page
  performs differently from the old page; the small gap we see is
  consistent with random chance.
- The daily trend chart confirms this: the two lines cross back and
  forth constantly with no consistent winner, exactly what you'd
  expect when there's genuinely no difference between the two pages.

## What this means for the business
The honest, correct recommendation here is: **do not roll out the
new page based on this data** - it does not show a meaningful
improvement over the old page. This is actually a very common, real
outcome in A/B testing (most experiments don't find a winner), and
knowing how to correctly conclude "no significant difference" -
rather than convincing yourself of an effect that isn't really
there - is an important, genuine data science skill.

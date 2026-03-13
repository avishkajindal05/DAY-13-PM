# Q1 — Handling 40% Missing Values in a 1M Row Column (`income`)

## Problem Context
- Dataset size: **1,000,000 rows**
- Missing values in `income`: **40%**
- Missing count: **~400,000 rows**

Handling such a large proportion of missing values requires **structured decision making**, not automatic imputation.

---

## Step 1 — Understand Why Data Is Missing

First determine the **missingness mechanism**:

| Type | Meaning | Action |
|-----|------|------|
| MCAR | Missing Completely At Random | Imputation usually safe |
| MAR | Missing depends on other variables | Model-based imputation |
| MNAR | Missing related to the value itself | More complex handling |

Example checks:
- Compare missing income across **age groups**
- Compare missing income across **location / job role**
- Check if missing rows correlate with **survey non-response**

---

## Step 2 — Decide Whether to Drop or Fill

### When I Would **Drop the Column**
- If income is **not critical for analysis**
- If missing rate **>60–70%**
- If missing values **cannot be reliably inferred**

### When I Would **Drop Rows**
- If dataset is very large (1M rows)  
- If only **few rows missing critical fields**

Example rule:
If income missing AND other key variables missing → drop row

---

## Step 3 — Choose a Fill Strategy

Because **40% is large**, simple mean imputation can bias results.

Better options:

### Option 1 — Median Imputation
Best when distribution is skewed.
df["income"].fillna(df["income"].median())

Why median?
- income is usually **right-skewed**
- median resistant to extreme values

---

### Option 2 — Group-Based Imputation (Recommended)

df["income"] = df.groupby("job_role")["income"].transform(
lambda x: x.fillna(x.median())
)

Benefits:
- preserves **income variation**
- more realistic

---

### Option 3 — Predictive Imputation

Train model to predict income:

Features:
- education
- location
- age
- job title

Example:

income_model.predict(features)


Used in **large ML pipelines**.

---

## Step 4 — Validate Imputation

Check if distribution changed.

Compare:

df["income"].describe()

Before vs After.

Plot distributions:


sns.histplot(income_before)
sns.histplot(income_after)


---

## Final Decision

For a **1M row dataset with 40% missing income**:

Best practical approach:

**Group-wise median imputation + missing flag**


df["income_missing"] = df["income"].isna()

df["income"] = df.groupby("job_role")["income"].transform(
lambda x: x.fillna(x.median())
)


This preserves information about **missingness patterns**.

---

# Q2 — Cleaning Messy Text Column

## Function

```python
import pandas as pd
import re

def standardize_column(series):
    
    cleaned = (
        series
        .astype(str)
        .str.strip()                       # remove leading/trailing spaces
        .str.lower()                       # lowercase
        .str.replace(r"\s+", " ", regex=True)   # collapse multiple spaces
        .str.replace(r"[^a-z0-9\s]", "", regex=True)  # remove special chars
    )
    
    return cleaned

TEST EXAMPLE
data = pd.Series([
    "  Hello  World!! ",
    "  NEW YORK  ",
    "san--francisco",
    "   MUMBAI   "
])

cleaned = standardize_column(data)

print(cleaned)

output
0    hello world
1       new york
2    sanfrancisco
3         mumbai
dtype: object
Q3 — Debugging Data Cleaning Code
Original Code
import pandas as pd
 
df = pd.DataFrame({
    "price": ["1,500", "2000", "N/A", "3,200", "abc"],
    "category": ["  Electronics ", "CLOTHING", "electronics", " Books", ""],
    "date": ["15/03/2024", "2024-07-01", "22-Nov-2024", "01/10/2024", None],
})

df["price"] = pd.to_numeric(df["price"], errors="coerce")

clean = df[df["price"] > 1000 and df["category"] != ""]

electronics = df[df["category"].str.contains("electronics")]

df["date"] = pd.to_datetime(df["date"])

Bug 1 — Hidden NaN Markers Not Replaced

Problem:

"N/A"
"1,500"


must be cleaned before numeric conversion.

Fix
df["price"] = (
    df["price"]
    .replace("N/A", None)
    .str.replace(",", "", regex=False)
)

df["price"] = pd.to_numeric(df["price"], errors="coerce")

Bug 2 — Incorrect Boolean Operator

Pandas requires bitwise operators.

Wrong
and

Fix
clean = df[(df["price"] > 1000) & (df["category"] != "")]

Bug 3 — .str.contains() with NaN

NaN values cause errors.

Fix
electronics = df[
    df["category"]
    .str.strip()
    .str.lower()
    .str.contains("electronics", na=False)
]

Bug 4 — Mixed Date Formats

Dates have multiple formats:

15/03/2024
2024-07-01
22-Nov-2024

Fix
df["date"] = pd.to_datetime(df["date"], errors="coerce", dayfirst=True)

Corrected Final Code
import pandas as pd
 
df = pd.DataFrame({
    "price": ["1,500", "2000", "N/A", "3,200", "abc"],
    "category": ["  Electronics ", "CLOTHING", "electronics", " Books", ""],
    "date": ["15/03/2024", "2024-07-01", "22-Nov-2024", "01/10/2024", None],
})

df["price"] = (
    df["price"]
    .replace("N/A", None)
    .str.replace(",", "", regex=False)
)

df["price"] = pd.to_numeric(df["price"], errors="coerce")

df["category"] = df["category"].str.strip().str.lower()

clean = df[(df["price"] > 1000) & (df["category"] != "")]

electronics = df[df["category"].str.contains("electronics", na=False)]

df["date"] = pd.to_datetime(df["date"], errors="coerce", dayfirst=True)
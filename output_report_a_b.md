# Data Cleaning & Profiling Results Report

## Part 1 — `survey_cleaner.py` Output

### Warning Encountered

ChainedAssignmentError:
A value is being set on a copy of a DataFrame or Series through chained assignment using an inplace method.
Example problematic line:
df["email_opt_in"].fillna("no", inplace=True)


**Explanation**  
Pandas Copy-on-Write prevents inplace modification when chained indexing is used.  
Recommended fix:

df["email_opt_in"] = df["email_opt_in"].fillna("no")

or

df.fillna({"email_opt_in": "no"}, inplace=True)

Before vs After Cleaning Comparison
Stage	Rows	Null Values	Memory (MB)
Before	65	20	0.007623
After	61	74	0.005640
Interpretation

Rows decreased (65 → 61) due to duplicate removal and dropping unfixable records.

Memory usage decreased, showing improved storage efficiency.

Null values increased because invalid values were converted to NaN during cleaning (to_numeric(errors="coerce")).
This is expected in robust data cleaning pipelines.

Data Types Comparison
BEFORE Cleaning
Always show details
respondent_id      int64
name               str
age                float64
city               str
satisfaction       str
rating             object
comments           str
email_opt_in       str

AFTER Cleaning
Always show details
respondent_id      int64
name               str
age                float64
city               str
satisfaction       str
rating             float64
comments           str
email_opt_in       str

Key Improvements

rating converted from object → float64

numeric columns now ready for statistical analysis

dataset exported successfully

Files Generated
Always show details
cleaned_survey.csv
data_quality_report.json

Part 2 — data_profiler.py Output
Dataset Summary
Metric	Value
Rows	5
Columns	4
Memory	0.0003 MB
Column Profiling
age

dtype: int64

unique values: 5

nulls: 0

statistics

min: 23
max: 120
mean: 45.0
median: 27
std: 42.01
skew: 2.21


Interpretation:

Extremely high skew due to value 120, suggesting a possible outlier.

name

dtype: string

unique: 5

nulls: 0

String statistics

avg length: 4.6
min length: 3
max length: 7


Observation:

Identified as high cardinality column because each row has a unique value.

salary

dtype: int64

unique: 5

min: 50000
max: 999999
mean: 241199.8
median: 52000
std: 424183.12
skew: 2.23


Interpretation:

Value 999999 strongly inflates the mean and standard deviation.

Indicates a potential salary outlier.

city

dtype: string

unique: 2

values distribution

Always show details
LA: 3
NY: 2


String length stats

Always show details
avg: 2
min: 2
max: 2

Potential Issues Identified
Issue Type	Columns
Single value columns	None
High cardinality columns	name
Outlier columns	None detected by >3σ rule

Note: Although salary contains an extreme value, the dataset is very small (5 rows), so the 3-sigma rule did not trigger an outlier flag.
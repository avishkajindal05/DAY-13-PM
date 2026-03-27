# 🧹 DAY-13-PM

**Data Cleaning & Profiling Pipeline**

---

## 📌 Overview

This repository contains the implementation of a **data cleaning and profiling pipeline** developed as part of the **Day 13 (PM Session)** assignment.

The project focuses on transforming **messy, unstructured survey data** into a clean, reliable dataset while generating a **data quality report** for analysis.

---

## 📂 Repository Structure

```bash
DAY-13-PM/
│
├── LICENSE
├── README.md
│
├── messy_data.csv              # Raw dataset with inconsistencies
├── cleaned_survey.csv          # Cleaned dataset
│
├── survey_cleaner.py           # Data cleaning logic
├── data_profiler.py            # Data profiling & quality analysis
│
├── data_quality_report.json    # Generated quality report
├── output_report_a_b.md        # Final report (Part A & B)
│
├── Part_c.md                   # Conceptual answers
├── Part_d.ipynb                # Notebook-based analysis
```

---

## 🎯 Objectives

* Clean and preprocess messy survey data
* Identify and fix data quality issues
* Generate a structured data quality report
* Build reusable scripts for automation

---

## 🔍 Key Data Issues Addressed

### 1. Missing Values

* Handled using imputation or removal strategies

---

### 2. Inconsistent Formatting

* Standardized text (e.g., case normalization)
* Unified categorical values

---

### 3. Duplicate Records

* Identified and removed duplicates

---

### 4. Invalid Entries

* Detected out-of-range or incorrect values
* Applied logical corrections

---

## ⚙️ Pipeline Workflow

1. Load raw dataset (`messy_data.csv`)
2. Perform data cleaning using `survey_cleaner.py`
3. Generate cleaned dataset (`cleaned_survey.csv`)
4. Run profiling using `data_profiler.py`
5. Produce `data_quality_report.json`

---

## 🛠️ Tools & Technologies

* Python
* Pandas
* JSON Handling
* Data Cleaning Techniques

---

## 🚀 How to Run

1. Clone the repository

```bash
git clone <your-repo-link>
cd DAY-13-PM
```

2. Run cleaning script

```bash
python survey_cleaner.py
```

3. Run profiling script

```bash
python data_profiler.py
```

4. Check outputs:

* `cleaned_survey.csv`
* `data_quality_report.json`
* `output_report_a_b.md`

---

## 📊 Output

* Cleaned dataset ready for analysis
* Data quality metrics in JSON format
* Markdown report summarizing findings

---

## 📈 Outcome

* Improved data consistency and reliability
* Automated pipeline for cleaning and profiling
* Structured reporting for better insights

---

## 📄 License

This project is licensed under the **MIT License**.

---

## ✍️ Author

**Avishka Jindal**
---

If you want next step: I can help you create a **single portfolio README linking all your Day 13, 25, 26, 27 projects** — that’s what recruiters actually look at.

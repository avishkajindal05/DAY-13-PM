import pandas as pd
import numpy as np
import json
import random


def create_dataset():
    names = ["Alice","Bob","Charlie","David","Eva","Frank","Grace","Hannah","Ivan","Julia"]
    cities = ["New York","London","Paris","Berlin","Tokyo","Delhi"]
    satisfaction_levels = ["Low","Medium","High"]

    rows = []

    for i in range(60):
        row = {
            "respondent_id": i,
            "name": random.choice(names),
            "age": random.choice([25,30,35,40,-5,200,None]),
            "city": random.choice(cities),
            "satisfaction": random.choice(satisfaction_levels),
            "rating": random.choice([1,2,3,4,5,"five",""]),  
            "comments": random.choice([
                "Great service"," ok ","BAD EXPERIENCE",None,""
            ]),
            "email_opt_in": random.choice(["Yes","No","yes","no"," YES ",""])
        }
        rows.append(row)

    df = pd.DataFrame(rows)

    df = pd.concat([df, df.iloc[0:5]], ignore_index=True)

    df["city"] = df["city"].astype(str) + random.choice([" ", "  ", ""])

    df.loc[3, "comments"] = "NA"
    df.loc[5, "city"] = ""

    return df


def detect_issues(df: pd.DataFrame):

    report = {}

    report["total_rows"] = len(df)

    report["total_missing"] = int(df.isna().sum().sum())

    report["missing_per_column"] = df.isna().sum().to_dict()

    report["duplicate_count"] = int(df.duplicated().sum())

    wrong_types = {}
    for col in df.columns:
        if col == "age":
            wrong_types[col] = df[~df["age"].apply(lambda x: isinstance(x,(int,float)) or pd.isna(x))].shape[0]

    report["wrong_types"] = wrong_types

    invalid_age = df[(df["age"] < 0) | (df["age"] > 120)].shape[0]
    invalid_rating = df[~df["rating"].isin([1,2,3,4,5])].shape[0]

    report["invalid_values"] = {
        "age_out_of_range": int(invalid_age),
        "invalid_rating": int(invalid_rating)
    }

    return report


def clean_data(df):

    df = df.copy()

    df.replace(["", "NA", "None"], np.nan, inplace=True)

    df["age"] = pd.to_numeric(df["age"], errors="coerce")
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")

    text_cols = ["name","city","satisfaction","comments","email_opt_in"]
    for col in text_cols:
        df[col] = (
            df[col]
            .astype(str)
            .str.strip()       
            .str.lower()       
        )

    df.loc[(df["age"] < 0) | (df["age"] > 120), "age"] = np.nan

    df["age"].fillna(df["age"].median(), inplace=True)

    df["rating"].fillna(df["rating"].median(), inplace=True)

    df["satisfaction"].fillna(df["satisfaction"].mode()[0], inplace=True)

    df["city"].fillna(df["city"].mode()[0], inplace=True)

    df["comments"].fillna("no comment", inplace=True)

    df["email_opt_in"].fillna("no", inplace=True)


    df.dropna(subset=["name"], inplace=True)

    df.drop_duplicates(inplace=True)

    return df


def compare_stats(before, after):

    stats = pd.DataFrame({
        "rows": [len(before), len(after)],
        "null_values": [before.isna().sum().sum(), after.isna().sum().sum()],
        "memory_mb": [
            before.memory_usage(deep=True).sum() / (1024**2),
            after.memory_usage(deep=True).sum() / (1024**2)
        ]
    }, index=["before","after"])

    print("\n BEFORE vs AFTER ")
    print(stats)

    print("\nDtypes BEFORE")
    print(before.dtypes)

    print("\nDtypes AFTER")
    print(after.dtypes)


def main():

    df = create_dataset()

    print("Original Dataset Shape:", df.shape)

    report = detect_issues(df)

    cleaned_df = clean_data(df)

    compare_stats(df, cleaned_df)

    cleaned_df.to_csv("cleaned_survey.csv", index=False)

    with open("data_quality_report.json","w") as f:
        json.dump(report, f, indent=4)

    print("\nFiles exported:")
    print("cleaned_survey.csv")
    print("data_quality_report.json")


if __name__ == "__main__":
    main()

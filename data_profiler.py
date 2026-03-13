import pandas as pd
import numpy as np
import re
from collections import Counter


def data_profiler(df: pd.DataFrame):

    profile = {
        "dataset_summary": {},
        "columns": {},
        "potential_issues": {
            "single_value_columns": [],
            "high_cardinality_columns": [],
            "outlier_columns": []
        }
    }


    profile["dataset_summary"] = {
        "rows": len(df),
        "columns": df.shape[1],
        "memory_mb": df.memory_usage(deep=True).sum() / (1024**2)
    }



    for col in df.columns:

        col_data = df[col]

        col_profile = {}

        dtype = str(col_data.dtype)

        unique_count = col_data.nunique(dropna=False)

        null_count = col_data.isna().sum()

        null_percent = (null_count / len(df)) * 100 if len(df) > 0 else 0

        top_values = col_data.value_counts(dropna=False).head(5).to_dict()

        col_profile.update({
            "dtype": dtype,
            "unique_count": int(unique_count),
            "null_count": int(null_count),
            "null_percent": float(null_percent),
            "top_5_values": top_values
        })


        if pd.api.types.is_numeric_dtype(col_data):

            stats = {}

            stats["min"] = float(col_data.min()) if col_data.notna().any() else None
            stats["max"] = float(col_data.max()) if col_data.notna().any() else None
            stats["mean"] = float(col_data.mean()) if col_data.notna().any() else None
            stats["median"] = float(col_data.median()) if col_data.notna().any() else None
            stats["std"] = float(col_data.std()) if col_data.notna().any() else None
            stats["skew"] = float(col_data.skew()) if col_data.notna().any() else None

            col_profile["numeric_stats"] = stats

         
            if stats["std"] is not None and stats["std"] != 0:
                outliers = df[np.abs(col_data - stats["mean"]) > 3 * stats["std"]]

                if len(outliers) > 0:
                    profile["potential_issues"]["outlier_columns"].append(col)

   

        if pd.api.types.is_string_dtype(col_data) or col_data.dtype == "object":

            lengths = col_data.dropna().astype(str).apply(len)

            if len(lengths) > 0:

                string_stats = {
                    "avg_length": float(lengths.mean()),
                    "min_length": int(lengths.min()),
                    "max_length": int(lengths.max())
                }

                col_profile["string_stats"] = string_stats

        
            patterns = Counter()

            for val in col_data.dropna().astype(str).head(100):

                if re.match(r"^[A-Za-z]+$", val):
                    patterns["letters"] += 1
                elif re.match(r"^\d+$", val):
                    patterns["numbers"] += 1
                elif re.match(r"^[A-Za-z0-9]+$", val):
                    patterns["alphanumeric"] += 1
                else:
                    patterns["mixed"] += 1

            col_profile["patterns"] = dict(patterns)

        if unique_count <= 1:
            profile["potential_issues"]["single_value_columns"].append(col)

        if pd.api.types.is_string_dtype(col_data) or col_data.dtype == "object":
            if unique_count > len(df) * 0.8:
                profile["potential_issues"]["high_cardinality_columns"].append(col)

        profile["columns"][col] = col_profile


    print("\n DATASET SUMMARY ")
    print(f"Rows: {profile['dataset_summary']['rows']}")
    print(f"Columns: {profile['dataset_summary']['columns']}")
    print(f"Memory (MB): {profile['dataset_summary']['memory_mb']:.4f}")

    print("\n COLUMN SUMMARY ")

    for col, details in profile["columns"].items():

        print(f"\nColumn: {col}")
        print(f"  dtype: {details['dtype']}")
        print(f"  unique: {details['unique_count']}")
        print(f"  nulls: {details['null_count']} ({details['null_percent']:.2f}%)")
        print(f"  top values: {details['top_5_values']}")

        if "numeric_stats" in details:
            print(f"  numeric stats: {details['numeric_stats']}")

        if "string_stats" in details:
            print(f"  string stats: {details['string_stats']}")

    print("\n POTENTIAL ISSUES ")
    for k, v in profile["potential_issues"].items():
        print(f"{k}: {v}")

    return profile

if __name__ == "__main__":

    demo = pd.DataFrame({
        "age": [23, 25, 27, 30, 120],
        "name": ["Alice", "Bob", "Charlie", "David", "Eve"],
        "salary": [50000, 52000, 51000, 53000, 999999],
        "city": ["NY", "NY", "LA", "LA", "LA"]
    })

    data_profiler(demo)
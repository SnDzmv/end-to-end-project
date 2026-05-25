import pandas as pd
import json
from pathlib import Path
from datetime import datetime
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--date", required=True)
args = parser.parse_args()

run_date = args.date

print("DQ RUN DATE:", run_date)



BASE_DIR = Path(__file__).resolve().parent.parent

mart_path = (
    BASE_DIR
    / "data"
    / "mart"
    / "variant_13"
    / f"mart_{run_date}.csv"
)

report_path = BASE_DIR / "docs" / "dq_report.json"

print("MART FILE:", mart_path)

def check_non_empty(df):
    return len(df) > 0, len(df)


def check_not_null(df, column):
    nulls = df[column].isna().sum()
    return nulls == 0, nulls


def check_unique(df, columns):
    duplicates = df.duplicated(subset=columns).sum()
    return duplicates == 0, duplicates


def check_year_range(df):
    current_year = datetime.now().year

    invalid = df[
        (df["year"] < 1900)
        | (df["year"] > current_year)
    ]

    return len(invalid) == 0, len(invalid)


def check_growth_rate(df):
    invalid = df[
        ~df["growth_rate"].isna()
        & (
            (df["growth_rate"] < -100)
            | (df["growth_rate"] > 1000)
        )
    ]

    return len(invalid) == 0, len(invalid)




def run_dq_checks(df):

    results = []

    def add_result(name, passed, details, critical=True):

        status = (
            "PASS"
            if passed
            else ("FAIL" if critical else "WARNING")
        )

        results.append({
            "check": name,
            "status": status,
            "details": int(details)
        })

    passed, details = check_non_empty(df)
    add_result("non_empty", passed, details, True)

    passed, details = check_not_null(df, "year")
    add_result("not_null_year", passed, details, True)

    passed, details = check_not_null(df, "value")
    add_result("not_null_value", passed, details, True)

    passed, details = check_unique(df, ["country_name", "year"])
    add_result("unique_country_year", passed, details, True)

    passed, details = check_year_range(df)
    add_result("year_range", passed, details, True)

    passed, details = check_growth_rate(df)
    add_result("growth_rate_range", passed, details, False)

    return results



def main():

    if not mart_path.exists():
        raise Exception(f"MART FILE NOT FOUND: {mart_path}")

    df = pd.read_csv(mart_path)

    print("ROWS:", len(df))
    print("COLUMNS:", df.columns.tolist())

    results = run_dq_checks(df)

    report_path.parent.mkdir(parents=True, exist_ok=True)

    with open(report_path, "w") as f:
        json.dump(results, f, indent=4)

    print("\nDQ REPORT:")

    for r in results:
        print(r)

    fail_count = sum(
        1
        for r in results
        if r["status"] == "FAIL"
    )

    warning_count = sum(
        1
        for r in results
        if r["status"] == "WARNING"
    )

    pass_count = sum(
        1
        for r in results
        if r["status"] == "PASS"
    )

    print("\nSUMMARY")
    print("PASS:", pass_count)
    print("WARNING:", warning_count)
    print("FAIL:", fail_count)

    if fail_count > 0:
        raise Exception("DQ FAILED")


if __name__ == "__main__":
    main()

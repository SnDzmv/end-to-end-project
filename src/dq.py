import pandas as pd
import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent

mart_path = BASE_DIR / "data" / "mart" / "variant_13" / "mart_yearly.csv"
report_path = BASE_DIR / "data" / "dq_report.json"


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
    invalid = df[(df["year"] < 1900) | (df["year"] > current_year)]
    return len(invalid) == 0, len(invalid)


def check_growth_rate(df):
    invalid = df[~df["growth_rate"].isna() & ((df["growth_rate"] < -100) | (df["growth_rate"] > 1000))]
    return len(invalid) == 0, len(invalid)

def run_dq_checks(df):
    results = []

    def add_result(name, passed, details, critical=True):
        status = "PASS" if passed else ("FAIL" if critical else "WARNING")
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
    df = pd.read_csv(mart_path)

    results = run_dq_checks(df)

    report_path.parent.mkdir(parents=True, exist_ok=True)

    with open(report_path, "w") as f:
        json.dump(results, f, indent=4)

    print("DQ Report:")
    for r in results:
        print(r)


if __name__ == "__main__":
    main()

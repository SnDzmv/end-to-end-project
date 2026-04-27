import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import pandas as pd
from src.dq import (
    check_not_null,
    check_non_empty,
    check_unique
)


def test_not_null_ok():
    df = pd.DataFrame({"value": [1, 2, 3]})
    result, _ = check_not_null(df, "value")
    assert result


def test_not_null_fail():
    df = pd.DataFrame({"value": [1, None, 3]})
    result, _ = check_not_null(df, "value")
    assert not result


def test_empty_df():
    df = pd.DataFrame({"value": []})
    result, _ = check_non_empty(df)
    assert not result


def test_unique_ok():
    df = pd.DataFrame({
        "country_name": ["ZA", "ZA"],
        "year": [2020, 2021]
    })
    result, _ = check_unique(df, ["country_name", "year"])
    assert result


def test_unique_fail():
    df = pd.DataFrame({
        "country_name": ["ZA", "ZA"],
        "year": [2020, 2020]
    })
    result, _ = check_unique(df, ["country_name", "year"])
    assert not result


if __name__ == "__main__":
    test_not_null_ok()
    test_not_null_fail()
    test_empty_df()
    test_unique_ok()
    test_unique_fail()
    print("All tests passed manually")

import json
import subprocess
from pathlib import Path
from datetime import datetime
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

STATE_PATH = BASE_DIR / "data" / "state.json"
MART_PATH = BASE_DIR / "data" / "mart" / "variant_13" / "mart_yearly.csv"



def load_state():
    if not STATE_PATH.exists():
        return {
            "last_year": None,
            "last_run": None,
            "mode": None
        }

    with open(STATE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_state(state: dict):
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def run_extract():
    print(" Extract")
    subprocess.run(["python", "src/extract.py"], cwd=BASE_DIR, check=True)


def run_normalization():
    print(" Normalization (notebook)")
    subprocess.run(
        [
            "jupyter", "nbconvert",
            "--to", "notebook",
            "--execute",
            "--inplace",
            "notebooks/week3_eda.ipynb"
        ],
        cwd=BASE_DIR,
        check=True
    )


def run_mart():
    print(" Mart")
    subprocess.run(["python", "src/mart.py"], cwd=BASE_DIR, check=True)


def run_load():
    print(" Load")
    subprocess.run(["python", "src/load.py"], cwd=BASE_DIR, check=True)


def run_full(state):
    run_extract()
    run_normalization()
    run_mart()
    run_load()

    df = pd.read_csv(MART_PATH)

    state["last_year"] = int(df["year"].max())
    state["last_run"] = datetime.now().isoformat()
    state["mode"] = "full"

    save_state(state)

    print(" FULL MODE finished")



def run_incremental(state):
    last_year = state.get("last_year")

    print(" Previous state:", state)

    run_extract()
    run_normalization()
    run_mart()

    df = pd.read_csv(MART_PATH)

    if last_year is not None:
        df_inc = df[df["year"] > last_year]
    else:
        df_inc = df


    df_inc.to_csv(MART_PATH, index=False)

    run_load()

    state["last_year"] = int(df["year"].max())
    state["last_run"] = datetime.now().isoformat()
    state["mode"] = "incremental"

    save_state(state)

    print(" INCREMENTAL MODE finished")



def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["full", "incremental"], required=True)

    args = parser.parse_args()

    state = load_state()

    print(f"\n=== {args.mode.upper()} MODE ===\n")

    if args.mode == "full":
        run_full(state)
    else:
        run_incremental(state)


if __name__ == "__main__":
    main()

import argparse
import subprocess
import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent

STATE_PATH = BASE_DIR / "data" / "state.json"

NOTEBOOK_PATH = BASE_DIR / "notebooks" / "week3_eda.ipynb"


def load_state():
    if STATE_PATH.exists():
        with open(STATE_PATH, "r") as f:
            return json.load(f)
    return {}


def save_state(state):
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_PATH, "w") as f:
        json.dump(state, f, indent=2)



def run_extract():
    print("▶ Extract")
    subprocess.run(
        ["python", "src/extract.py"],
        cwd=BASE_DIR,
        check=True
    )


def run_normalization():
    print("▶ Normalization (notebook)")

    subprocess.run(
        [
            "jupyter", "nbconvert",
            "--to", "notebook",
            "--execute",
            str(NOTEBOOK_PATH)
        ],
        cwd=BASE_DIR,
        check=True
    )


def run_mart():
    print("▶ Mart")
    subprocess.run(
        ["python", "src/mart.py"],
        cwd=BASE_DIR,
        check=True
    )


def run_load():
    print("▶ Load")
    subprocess.run(
        ["python", "src/load.py"],
        cwd=BASE_DIR,
        check=True
    )



def run_full():
    print("\n=== FULL MODE ===\n")

    run_extract()
    run_normalization()
    run_mart()
    run_load()

    state = {
        "last_run": datetime.now().isoformat(),
        "mode": "full"
    }
    save_state(state)


def run_incremental():
    print("\n=== INCREMENTAL MODE ===\n")

    state = load_state()
    print("Previous state:", state)

    run_extract()
    run_normalization()
    run_mart()
    run_load()

    state["last_run"] = datetime.now().isoformat()
    state["mode"] = "incremental"

    save_state(state)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["full", "incremental"], required=True)
    args = parser.parse_args()

    if args.mode == "full":
        run_full()
    else:
        run_incremental()


if __name__ == "__main__":
    main()

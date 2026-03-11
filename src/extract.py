import requests
import yaml
import json
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = BASE_DIR / "configs" / "variant_13.yml"


def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def build_url(config):
    base_url = config["api"]["base_url"]
    template = config["api"]["request_template"]
    params = config["api"].get("params", {})

    url = base_url + template
    return url, params


def extract_data(url, params):
    response = requests.get(url, params=params, timeout=10)

    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code}")

    return response.json()


def save_raw(data):
    raw_dir = BASE_DIR / "data" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = raw_dir / f"raw_{timestamp}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("Saved raw data to:", filename)


def main():
    config = load_config()
    url, params = build_url(config)
    print("Sending request to:", url)
    data = extract_data(url, params)
    print("Saving raw data")
    save_raw(data)



if __name__ == "__main__":
    main()

import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

normalized_path = BASE_DIR / "data" / "normalized" / "variant_13" / "2026-03-23_12-00-00.csv"
reference_path = BASE_DIR / "reference" / "countries.csv"
output_path = BASE_DIR / "data" / "mart" / "variant_13" / "mart_yearly.csv"

output_path.parent.mkdir(parents=True, exist_ok=True)


df = pd.read_csv(normalized_path)
ref = pd.read_csv(reference_path)


merged = df.merge(
    ref,
    on="countryiso3code",
    how="left",
    validate="many_to_one"
)


merged["date"] = pd.to_datetime(merged["date"])
merged["year"] = merged["date"].dt.year


merged = merged.sort_values("year")



merged["value_prev"] = merged["value"].shift(1)


merged["value_diff"] = merged["value"] - merged["value_prev"]


merged["growth_rate"] = (merged["value_diff"] / merged["value_prev"]) * 100


merged["trend"] = merged["value_diff"].apply(
    lambda x: "growth" if x > 0 else ("decline" if x < 0 else "no_change")
)


merged["rolling_avg_3"] = merged["value"].rolling(3).mean()


mart = merged[[
    "country_name",
    "country_name_full",
    "region",
    "income_level",
    "year",
    "value",
    "value_prev",
    "value_diff",
    "growth_rate",
    "trend",
    "rolling_avg_3"
]]


mart.to_csv(output_path, index=False)

print(f"Mart saved to: {output_path}")

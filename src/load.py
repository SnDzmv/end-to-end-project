import pandas as pd
from sqlalchemy import create_engine, text
import os
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--date", required=True)
args = parser.parse_args()

run_date = args.date

print("LOAD RUN DATE:", run_date)


POSTGRES_HOST = "postgres"
POSTGRES_PORT = "5432"
POSTGRES_DB = "airflow"
POSTGRES_USER = "airflow"
POSTGRES_PASSWORD = "airflow"


BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

MART_FILE = os.path.join(
    BASE_DIR,
    "data",
    "mart",
    "variant_13",
    f"mart_{run_date}.csv"
)

print("MART FILE:", MART_FILE)



if not os.path.exists(MART_FILE):
    raise Exception(f"MART FILE NOT FOUND: {MART_FILE}")

df = pd.read_csv(MART_FILE)

df = df.where(pd.notnull(df), None)

df["year"] = df["year"].astype(int)
print("ROWS:", df.shape[0])
print("COLUMNS:", df.columns.tolist())


df["run_date"] = run_date


engine = create_engine(
    f"postgresql+psycopg2://"
    f"{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

TABLE_NAME = "mart_yearly"


with engine.begin() as conn:

    print("CREATING TABLE IF NOT EXISTS...")

    conn.execute(
        text(f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            country_name TEXT,
            country_name_full TEXT,
            region TEXT,
            income_level TEXT,
            year INT,
            value FLOAT,
            value_prev FLOAT,
            value_diff FLOAT,
            growth_rate FLOAT,
            trend TEXT,
            rolling_avg_3 FLOAT,
            run_date TEXT
        );
        """)
    )

    print("DELETE OLD PERIOD:", run_date)

    conn.execute(
        text(f"""
        DELETE FROM {TABLE_NAME}
        WHERE run_date = :run_date
        """),
        {"run_date": run_date}
    )

    print("INSERTING NEW ROWS...")

    df.to_sql(
        TABLE_NAME,
        conn,
        if_exists="append",
        index=False
    )

    print("LOAD FINISHED")


with engine.connect() as conn:

    count = conn.execute(
        text(f"""
        SELECT COUNT(*)
        FROM {TABLE_NAME}
        WHERE run_date = :run_date
        """),
        {"run_date": run_date}
    ).scalar()

    print("ROWS IN DB FOR PERIOD:", count)

print("SUCCESS")

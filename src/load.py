import pandas as pd
from sqlalchemy import create_engine, text
import os



POSTGRES_HOST = "postgres"
POSTGRES_PORT = "5432"
POSTGRES_DB = "airflow"
POSTGRES_USER = "airflow"
POSTGRES_PASSWORD = "airflow"


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MART_FILE = os.path.join(BASE_DIR, "data", "mart", "variant_13", "mart_yearly.csv")


df = pd.read_csv(MART_FILE)

print("Файл загружен:", MART_FILE)
print("Строки:", df.shape[0], "Колонки:", df.shape[1])
print("Колонки:", df.columns.tolist())


engine = create_engine(
    f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)


TABLE_NAME = "mart_yearly"


with engine.begin() as conn:
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
            rolling_avg_3 FLOAT
        );
        """)
    )

    conn.execute(text(f"TRUNCATE TABLE {TABLE_NAME};"))

    df.to_sql(TABLE_NAME, conn, if_exists="append", index=False)

    print(f"Данные успешно загружены в таблицу {TABLE_NAME}")


with engine.connect() as conn:
    count = conn.execute(text(f"SELECT COUNT(*) FROM {TABLE_NAME};")).scalar()
    print("Строк в таблице:", count)

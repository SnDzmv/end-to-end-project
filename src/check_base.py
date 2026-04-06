import os
from sqlalchemy import create_engine, text


POSTGRES_USER = "user"
POSTGRES_PASSWORD = "pass"
POSTGRES_DB = "mydb"
POSTGRES_HOST = "localhost"
POSTGRES_PORT = "5432"


engine = create_engine(
    f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

TABLE_NAME = "mart_yearly"


checks = {
    "1. Таблица не пустая": f"SELECT COUNT(*) FROM {TABLE_NAME};",
    "2. Диапазон лет": f"SELECT MIN(year), MAX(year) FROM {TABLE_NAME};",
    "3. NULL в ключевых колонках": f"SELECT COUNT(*) FROM {TABLE_NAME} WHERE country_name IS NULL OR year IS NULL;",
    "4. Дубликаты по country_name + year": f"""
        SELECT country_name, year, COUNT(*) 
        FROM {TABLE_NAME} 
        GROUP BY country_name, year 
        HAVING COUNT(*) > 1;
    """,
    "5. Метрики value": f"SELECT SUM(value), AVG(value), MAX(value) FROM {TABLE_NAME};"
}


with engine.connect() as conn:
    for name, sql in checks.items():
        print(f"\n=== {name} ===")
        result = conn.execute(text(sql))
        rows = result.fetchall()
        for row in rows:
            print(row)

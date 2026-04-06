# SQL Проверки для недели 5

В этой неделе мы загрузили mart-файл `mart_yearly.csv` в таблицу `mart_yearly` Postgres и провели следующие проверки:

1. **Таблица не пустая**
   ```sql
   SELECT COUNT(*) FROM mart_yearly;

Проверка, что данные действительно загружены.

Диапазон лет

SELECT MIN(year), MAX(year) FROM mart_yearly;

Проверка корректного диапазона годовых данных.

NULL в ключевых колонках

SELECT COUNT(*) FROM mart_yearly WHERE country_name IS NULL OR year IS NULL;

Проверка отсутствия пустых значений в важных колонках.

Дубликаты по бизнес-ключу

SELECT country_name, year, COUNT(*) 
FROM mart_yearly 
GROUP BY country_name, year 
HAVING COUNT(*) > 1;

Проверка, что повторные строки не создаются при идемпотентной загрузке.

Метрики value

SELECT SUM(value), AVG(value), MAX(value) FROM mart_yearly;

Проверка корректности агрегированных метрик.

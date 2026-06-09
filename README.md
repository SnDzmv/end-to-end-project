# Сквозной проект

Учебный end-to-end проект по анализу данных Всемирного банка: получение данных через World Bank API, нормализация, построение mart-витрины, проверки качества данных, загрузка в PostgreSQL, визуализация, ML-анализ, Airflow-оркестрация и формирование проверяемой LLM-сводки.

# Что делает проект

Проект работает с данными Всемирного банка по показателю безработицы в Южно-Африканской Республике (South Africa).

Основная цепочка:

```text
Extract -> Transform -> Mart -> DQ -> Load -> LLM Summary
```

Слои данных:

```text
data/raw/variant_13/           raw JSON из World Bank API
data/normalized/variant_13/    очищенные CSV
data/mart/variant_13/          аналитическая витрина
docs/dq_report.json            отчет качества данных
docs/ml/                       артефакты ML-анализа
docs/llm/summary.md            итоговая LLM-сводка
```

# Быстрый запуск проекта

## Запуск инфраструктуры

```bash
docker compose up -d
```
## Воспроизводимый запуск из корня проекта:
```
python -m src.pipeline.pipeline --mode full
```
Инкрементальный режим:
```
python -m src.pipeline.pipeline --mode incremental
```
Последовательное выполнение extract, transform, mart, load, dq.


## Airflow

Открыть:

```text
http://localhost:8080
```

DAG:

```text
etl_variant_13
```

Цепочка задач:

```text
extract -> transform -> mart -> load -> dq
```

## Построение LLM Summary

```bash
python src/llm_summary.py
```

Будут созданы:

```text
docs/llm/context.md
docs/llm/prompt.md
docs/llm/summary.md
docs/LLM_Usage_Log.md
```

# Источник данных

Источник:

```text
World Bank API
```

Показатель:

```text
Unemployment, total (% of total labor force)
```

Страна:

```text
South Africa (ZAF)
```

# Реализованные компоненты

- Extract (получение данных из World Bank API)
- Transform (очистка и нормализация)
- Mart (аналитическая витрина)
- DQ (проверки качества данных)
- PostgreSQL Load
- Airflow orchestration
- BI-визуализация
- ML-анализ (Week 13)
- LLM Summary с anti-hallucination подходом (Week 14)

# Основные артефакты

```text
docs/dq_report.json
docs/ml/week13_summary.md
docs/ml/metrics.png
docs/llm/context.md
docs/llm/prompt.md
docs/llm/summary.md
docs/LLM_Usage_Log.md
```



## Установка (Windows)

1. Установить Miniconda.  
2. Дважды кликнуть файл для автоматической настройки:
scripts\setup_env.bat


## Smoke Test

Если всё прошло успешно, скрипт выведет:
[OK]



## Notes

- Все зависимости указаны в `requirements.txt`.  
- Скрипт `setup_env.bat` создаёт окружение, ставит библиотеки и запускает тест.  
- Рабочее окружение: `week1_env`.


# Неделя 2 — HTTP/API Extract (World Bank)

## Тема проекта
**Макроэкономика (World Bank) — ЮАР: Безработица (%)**  
Вариант: **13**  
Индикатор: `SL.UEM.TOTL.ZS` — Общая безработица (% от рабочей силы)  
Страна: `ZAF` — Южная Африка  

---
## API
endpoint:


https://api.worldbank.org/v2/country/ZAF/indicator/SL.UEM.TOTL.ZS?format=json&per_page=20000


---

## Как запускать (Windows)
1. Установить библиотеки:

```bash
pip install requests pyyaml
```
Запустить скрипт:

`python src/extract.py`

После запуска появится файл:

`data/raw/raw_YYYYMMDD_HHMMSS.json`

Примечания:

Таймаут установлен, чтобы программа не зависала на запросе.

Ошибки HTTP обрабатываются в скрипте.

JSON сохраняется без изменений для последующей трансформации.


## Неделя 3 — Pandas и нормализация данных

### Что было сделано
- Загружен raw JSON, полученный на Неделе 2
- Проанализирована структура JSON (список: метаданные + записи)
- Выделена основная часть данных (`data[1]`)
- Преобразование JSON → DataFrame с помощью `pd.json_normalize`
- Выполнена первичная очистка данных:
  - Переименование колонок для удобства
  - Приведение столбца `date` к типу datetime
  - Приведение столбца `value` к числовому типу
  - Удаление лишних колонок
  - Проверка на пропуски и дубликаты
- Сохранение нормализованных данных в CSV

### Описание датасета
- Источник: World Bank API
- Показатель: уровень безработицы (% от рабочей силы)
- Зерно данных: одна строка = одна страна за один год

### Результат
Нормализованный датасет сохранён в:
data/normalized/variant_13/YYYY-MM-DD_HH-MM-SS.csv

# Неделя 4 — Построение витрины (Data Mart)

## Тема проекта
**Макроэкономика (World Bank) — ЮАР: Безработица (%)**  
Вариант: **13**  
Индикатор: `SL.UEM.TOTL.ZS` — Общая безработица (% от рабочей силы)  
Страна: `ZAF` — Южная Африка  

---
## Рассчитанные метрики (KPI)

- `value` — уровень безработицы (%)  
- `value_prev` — значение прошлого года  
- `value_diff` — изменение к прошлому году  
- `growth_rate` — темп роста (%)  
- `trend` — направление изменения  
- `rolling_avg_3` — скользящее среднее (3 года)

## Как запускать

1. Убедиться, что Python окружение установлено и активировано  
2. Запустить скрипт:

```bash
python src/mart.py
```
После запуска формируется CSV с витриной данных, включающей все KPI и данные из справочника.

Итог

Реализован полный пайплайн обработки данных:

normalized → mart

Витрина содержит очищенные, обогащённые и агрегированные данные с рассчитанными метриками для анализа безработицы.

# Неделя 5 — Интеграция SQL и Postgres

На этой неделе мы сделали первый шаг по переходу от файлов к базе данных. Основные цели:

- Загрузка mart-файла `mart_yearly.csv` в Postgres  
- Создание таблицы `mart_yearly` с правильной схемой  
- Идемпотентная загрузка (повторный запуск не создает дублей)  
- Проведение базовых SQL-проверок для качества данных

## Файлы

- `src/load.py` — скрипт загрузки mart в Postgres  
- `src/sql_checks.py` — скрипт для выполнения 5 SQL-проверок  
- `docs/sql_checks.md` — описание проведенных проверок


## Использование

1. Поднять Postgres через Docker:
```bash
docker run -d --name postgres_db -e POSTGRES_USER=user -e POSTGRES_PASSWORD=pass -e POSTGRES_DB=mydb -p 5432:5432 postgres
```
Загрузить mart:
```bash
python src/load.py
```
Выполнить проверки:
```bash
python src/sql_checks.py
```

# Неделя 6 — ETL Pipeline

Проект реализует полный ETL-пайплайн обработки данных об уровне безработицы в Южной Африке на основе API World Bank.

Система поддерживает:
- Full загрузку (полная пересборка данных)
- Incremental загрузку (обработка только новых данных)
- State management (хранение watermark и состояния)
- Разделение слоёв данных (raw / normalized / mart)
- Загрузку в PostgreSQL

---

Extract (API World Bank)
↓
Raw JSON
↓
Normalization (Jupyter Notebook)
↓
Normalized CSV
↓
Mart (feature engineering)
↓
PostgreSQL (mart_yearly)


---

## Запуск проекта

### Установка зависимостей
```bash
pip install -r requirements.txt
```
Full pipeline (полная пересборка)
```bash
python src/pipeline.py --mode full
```
Incremental pipeline (инкрементальная загрузка)
```bash
python src/pipeline.py --mode incremental
```

Файл состояния:

data/state.json

Пример:

{
  "last_year": 2025,
  "last_run": "2026-04-20T20:08:53",
  "mode": "incremental"
}

Watermark

Используется поле:

year

Назначение:

определяет, какие данные уже обработаны
используется в incremental режиме
 Business Key

Уникальность записей:

country_name + year
Режимы работы
Full mode
пересоздаёт весь mart
игнорирует watermark
используется TRUNCATE в БД
Incremental mode
использует state.json
фильтрует данные по last_year
обрабатывает только новые записи

# Неделя 7 — Data Visualization

- построены визуализации на основе mart-данных по уровню безработицы в ЮАР  
- используется самый свежий mart CSV из `data/mart/variant_13/`  
- выполнен анализ данных в Jupyter Notebook  
- применены основные типы графиков:
  - временной ряд (line plot)
  - распределение (histogram)
  - ранжирование (bar chart)
- реализована корректная обработка дат (`datetime`, сортировка по времени)
- добавлены текстовые комментарии к графикам


---
Оформление

- добавлены информативные заголовки графиков

- подписи осей с указанием единиц измерения (%)

- корректно оформленная временная шкала

- улучшена читаемость визуализаций

---
Выводы:

-данные по безработице в ЮАР были проанализированы с помощью визуализации

-выявлена динамика изменения показателя во времени

-изучено распределение значений

-показана структура данных через группировку по диапазонам

# Неделя 8 — Data Quality

## Что было реализовано

### 1. Модуль Data Quality

Создан отдельный модуль:

src/dq.py

Он выполняет:
- загрузку данных
- запуск проверок качества
- формирование результатов
- сохранение отчета

---

## Реализованные проверки

В системе реализованы следующие проверки:

### 1. non_empty
Проверяет, что таблица не пустая  
Критичность: **FAIL**

---

### 2. not_null_year
Проверяет отсутствие NULL в поле `year`  
Критичность: **FAIL**

---

### 3. not_null_value
Проверяет отсутствие NULL в поле `value`  
Критичность: **FAIL**

---

### 4. unique_country_year
Проверяет уникальность бизнес-ключа: `country_name + year`  
Критичность: **FAIL**

---

### 5. year_range
Проверяет, что год находится в диапазоне `[1900, текущий]`  
Критичность: **FAIL**

---

### 6. growth_rate_range
Проверяет корректность значений роста  
Критичность: **WARNING**

---

## Как работает система

При запуске:

```bash
python src/dq.py
```
происходит:

1. Загрузка данных
2. Последовательный запуск всех DQ-проверок
3. Формирование результатов (PASS / FAIL / WARNING)
4. Сохранение отчета

## DQ Report

Отчет сохраняется в:
```
docs/dq_report.json
```

Формат:

[
  {
    "check": "not_null_value",
    "status": "FAIL",
    "details": 2
  }
]

## Unit-тесты

Реализованы тесты для проверки DQ-функций:
```
tests/test_dq.py
```

Типы тестов:

- позитивные
- негативные
- граничные

Запуск:
```bash
pytest
```
## Демонстрация

Для проверки корректности системы:

- в данные искусственно добавлялись ошибки:
-- NULL значения
-- дубликаты
-- некорректные значения
- после чего проверки возвращали FAIL / WARNING


# Неделя 10 — Docker + PostgreSQL + Metabase

## Описание проекта

Проект представляет собой локальную аналитическую среду на базе:

- PostgreSQL
- Metabase
- Docker Compose

Данные mart загружаются в PostgreSQL и используются для построения BI-дашборда в Metabase.

---

## Используемые технологии
- Docker
- Docker Compose
- PostgreSQL 16
- Metabase
- Python
- pandas
- SQLAlchemy

## Запуск проекта
### 1. Запуск контейнеров
```docker compose up -d```
### 2. Проверка контейнеров
```docker compose ps```
### 3. Загрузка данных в PostgreSQL
```python load.py```
### 4. Открытие Metabase

В браузере:

```http://localhost:3000```
## Параметры PostgreSQL
```
Database: mydb
User: user
Password: pass
```
## Docker Volumes

Используются volumes:

- pgdata
- metabase_data

Volumes позволяют сохранять данные между пересозданиями контейнеров.

## BI Dashboard

Dashboard построен на таблице:

```mart_yearly```

Созданы визуализации:

- line chart
- bar chart
- summary visualization
---
## Скриншоты

Скриншоты dashboard и графиков находятся в:

```docs/bi/```



# Неделя 11 — Airflow ETL Pipeline

## Описание проекта

В рамках недели 11 реализован оркестрированный ETL-пайплайн с использованием Apache Airflow.

Пайплайн выполняет следующие шаги:

- extract — загрузка и подготовка исходных данных
- transform — построение витрины данных (mart)
- load — загрузка витрины в PostgreSQL
- dq — проверки качества данных

---

## Архитектура

Проект состоит из следующих компонентов:

- Apache Airflow (оркестрация)
- PostgreSQL (хранение данных)
- Python ETL-скрипты (src/)
- Docker Compose (контейнеризация)

---

## DAG

Основной DAG:

```etl_variant_13```


Порядок выполнения:


extract → transform → load → dq


---

## Запуск проекта

1. Запустить контейнеры:

```bash
docker compose up -d
```
Открыть Airflow UI:
```http://localhost:8080```
Логин:
```airflow / airflow```

Требования недели
- DAG с 4 задачами
- корректный порядок выполнения
- логи выполнения задач
- подключение к PostgreSQL через Docker network
- визуализация DAG в Airflow UI
- 
## Результат

Пайплайн успешно выполняется в Airflow и формирует витрину данных в PostgreSQL.



# Неделя 12 Airflow ETL pipeline 2


## Структура пайплайна

```text
extract → transform → dq → load
```

## Запуск Airflow

```bash
docker compose up -d
```

Airflow UI:

```text
http://localhost:8080
```

Логин:

```text
airflow
```

Пароль:

```text
airflow
```

## DAG

Основной DAG:

```text
airflow/dags/etl_variant_13.py
```

Расписание:

```python
schedule="*/5 * * * *"
```

## Инкрементальность

Каждый DAG Run обрабатывает свой период через:

```python
{{ ds }}
```

Файлы сохраняются как:

```text
data/mart/variant_13/mart_YYYY-MM-DD.csv
```

## Идемпотентность

Load реализован через:

```sql
DELETE period + INSERT
```

Повторный retry не создает дубликаты.

## DQ Gate

DQ выполняется перед load.

При FAIL DAG останавливается.


# Неделя 13 — Основы ML для аналитика

## Цель

Добавить в проект простой ML-блок с честной оценкой качества модели.

В рамках работы была построена простая модель регрессии для прогнозирования значения показателя по историческим данным.

---

## Используемые технологии

- Python
- Pandas
- Scikit-Learn
- Matplotlib
- Jupyter Notebook

---

## Запуск

Установить зависимости:

```bash
pip install -r requirements.txt
```

или отдельно:

```bash
pip install scikit-learn
```

Запустить ноутбук:

```bash
jupyter notebook
```

Открыть:

```text
notebooks/week13_ml.ipynb
```

---

## Что реализовано

- train/test split
- защита от data leakage
- baseline через DummyRegressor
- модель LinearRegression
- расчет метрики MAE
- визуализация результатов
- сохранение артефактов в docs/ml

---

## Результаты

Сформированы:

- график фактических и прогнозных значений
- график ошибок модели
- таблица прогнозов
- текстовый отчет по результатам эксперимента

Contract version: 0.1

## General Info
Project: South Africa Unemployment Analytics  
Source: World Bank API  
Indicator: SL.UEM.TOTL.ZS  
Granularity: 1 row = 1 country per year  
Timezone: UTC (year-level data, timezone not critical)

---

## mart.unemployment_sa

| column_name       | dtype   | nullable | unit        | description |
|------------------|--------|----------|-------------|-------------|
| country_name     | string | no       | -           | краткое название страны |
| country_name_full| string | no       | -           | полное название страны |
| region           | string | no       | -           | регион (Africa) |
| income_level     | string | no       | -           | уровень дохода страны |
| year             | int    | no       | year        | год наблюдения |
| value            | float  | no       | %           | уровень безработицы |
| value_prev       | float  | yes      | %           | значение за предыдущий год |
| value_diff       | float  | yes      | p.p.        | разница с прошлым годом |
| growth_rate      | float  | yes      | %           | темп роста относительно прошлого года |
| trend            | string | yes      | -           | направление изменения (growth/decline/no_change) |
| rolling_avg_3    | float  | yes      | %           | скользящее среднее за 3 года |

---

## Naming & Units Rules

- snake_case для всех колонок
- year — целое число
- все проценты хранятся в диапазоне 0–100 (НЕ 0–1)
- value_diff измеряется в процентных пунктах (p.p.)
- timestamp не используется, так как данные годовые
- запрещены абстрактные имена (value допустимо, т.к. это стандарт индикатора World Bank)

---

## Changelog

0.1 (2026-05-04):
- initial version of mart schema


# Data Contract — Неделя 2

## Источник
- **World Bank API** — `/country/ZAF/indicator/SL.UEM.TOTL.ZS?format=json`
- Данные по безработице ЮАР (% от рабочей силы)

## Формат
- **JSON**, массив объектов по годам
- Основные поля:
  - `date` — год  
  - `value` — значение (float или NULL)  
  - `countryiso3code` — ISO3 страны  
  - `indicator` — код индикатора

## Использование
- Сохраняется **сырой JSON** для последующей трансформации и анализа.

## Структура проекта
- Конфиг: `configs/variant_13.yml`  
- Скрипт: `src/extract.py`  
- Raw данные: `data/raw/raw_YYYYMMDD_HHMMSS.json`

## Ограничения
- `value` может быть NULL  
- Дубликаты по `(countryiso3code, indicator, date)` запрещены  
- `date`: 1960 — текущий год

# Data Contract — Неделя 3

## Нормализованный слой (Normalized)

### Зерно таблицы
Одна строка представляет значение уровня безработицы для одной страны за конкретный год.

### Схема таблицы

| Поле              | Тип        | Nullable | Описание |
|-------------------|------------|----------|----------|
| country_name      | object     | no       | Название страны |
| countryiso3code   | object     | no       | ISO3 код страны |
| date              | datetime64 | no       | Год наблюдения |
| value             | float64    | yes      | Уровень безработицы (%) |

### Преобразования
- Извлечение данных из вложенного JSON (`data[1]`)
- Преобразование структуры в таблицу (`pd.json_normalize`)
- Переименование колонок:
  - `country.value` → `country_name`
- Приведение типов:
  - `date` → datetime
  - `value` → numeric
- Удаление лишних колонок
- Проверка пропусков и дубликатов


# Data Contract — Неделя 4

##  Источник данных

- API: World Bank
- Тип данных: временные ряды
- Показатель: уровень безработицы (%)

---

##  Raw данные

Формат: JSON

Содержит:
- метаданные
- значения показателя по годам

---

##  Normalized слой

Формат: CSV

Одна строка:
> значение показателя для страны в конкретный год

Поля:

| Поле | Тип | Описание |
|------|-----|--------|
| country_name | string | название страны |
| countryiso3code | string | код страны |
| date | date | дата |
| value | float | уровень безработицы |

---

##  Mart слой

Формат: CSV

Поля:

| Поле | Описание |
|------|--------|
| year | год |
| value | уровень безработицы |
| value_prev | значение прошлого года |
| value_diff | изменение |
| growth_rate | темп роста |
| trend | направление |
| rolling_avg_3 | сглаживание |

---

##  Reference данные

Файл: `reference/countries.csv`

Поля:

| Поле | Описание |
|------|--------|
| countryiso3code | ключ |
| country_name_full | полное название |
| region | регион |
| income_level | уровень дохода |

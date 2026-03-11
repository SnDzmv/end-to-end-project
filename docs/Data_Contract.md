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

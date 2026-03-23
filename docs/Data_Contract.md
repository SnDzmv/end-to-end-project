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

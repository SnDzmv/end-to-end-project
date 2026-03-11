# Сквозной проект

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

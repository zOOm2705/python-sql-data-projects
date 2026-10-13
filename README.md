# Python / SQL Portfolio

Проекты, демонстрирующее навыки Python, SQL, анализа данных и написания поддерживаемого кода.

## Проекты

### 1. Анализ продаж на Python
**Стек:** Python, Pandas, NumPy, Matplotlib  
Загрузка CSV, проверка и очистка данных, расчёт выручки, анализ продаж по месяцам и категориям, сохранение итоговых таблиц и графиков.

Запуск:
```bash
python -m pip install -r requirements.txt
python 01_sales_analysis/analyze_sales.py
```

### 2. SQL Analytics
**Стек:** SQL, SQLite, оконные функции  
Схема небольшой базы продаж и аналитические запросы: выручка по месяцам, рейтинг товаров, накопительная сумма, сравнение текущего месяца с предыдущим.

Файл `02_sql_analytics/queries.sql` содержит запросы, а `schema.sql` — структуру и тестовые данные. Запустить можно в SQLite или DB Browser for SQLite.

### 3. Task Tracker
**Стек:** Python, JSON, unittest  
Консольный менеджер задач с добавлением, просмотром, завершением и удалением задач. Данные сохраняются в JSON; логика отделена от интерфейса и покрыта unit-тестами.

Запуск:
```bash
python 03_task_tracker/task_tracker.py --help
python 03_task_tracker/task_tracker.py add "Изучить SQL" 
python 03_task_tracker/task_tracker.py list
python -m unittest discover -s 03_task_tracker -v
```

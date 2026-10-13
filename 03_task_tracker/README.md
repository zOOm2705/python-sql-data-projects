# Task Tracker

## Цель
Показать основы структурирования Python-кода, работы с файлами, CLI и автоматических тестов.

## Возможности
- добавление задачи;
- просмотр всех задач;
- отметка задачи как выполненной;
- удаление задачи;
- хранение данных в JSON;
- обработка некорректного JSON и пустых названий;
- unit-тесты на `unittest`.

## Примеры
```bash
python 03_task_tracker/task_tracker.py add "Изучить Python"
python 03_task_tracker/task_tracker.py add "Решить задачи по SQL"
python 03_task_tracker/task_tracker.py list
python 03_task_tracker/task_tracker.py done 1
python 03_task_tracker/task_tracker.py delete 2
python -m unittest discover -s 03_task_tracker -v
```

Можно выбрать отдельный файл данных:
```bash
python 03_task_tracker/task_tracker.py --file ./my_tasks.json list
```

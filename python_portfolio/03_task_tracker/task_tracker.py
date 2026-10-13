"""Простой консольный менеджер задач с хранением в JSON."""
import argparse
import json
from pathlib import Path
from typing import Any

DEFAULT_DATA = Path(__file__).resolve().parent / "tasks.json"


def load_tasks(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Файл задач содержит некорректный JSON: {path}") from exc
    if not isinstance(data, list):
        raise ValueError("Ожидался список задач.")
    return data


def save_tasks(path: Path, tasks: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(tasks, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def add_task(path: Path, title: str) -> dict[str, Any]:
    title = title.strip()
    if not title:
        raise ValueError("Название задачи не должно быть пустым.")
    tasks = load_tasks(path)
    next_id = max((task["id"] for task in tasks), default=0) + 1
    task = {"id": next_id, "title": title, "done": False}
    tasks.append(task)
    save_tasks(path, tasks)
    return task


def complete_task(path: Path, task_id: int) -> bool:
    tasks = load_tasks(path)
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            save_tasks(path, tasks)
            return True
    return False


def delete_task(path: Path, task_id: int) -> bool:
    tasks = load_tasks(path)
    remaining = [task for task in tasks if task["id"] != task_id]
    if len(remaining) == len(tasks):
        return False
    save_tasks(path, remaining)
    return True


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Консольный менеджер задач")
    parser.add_argument("--file", type=Path, default=DEFAULT_DATA,
                        help="Путь к JSON-файлу (по умолчанию tasks.json)")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Добавить задачу")
    add_parser.add_argument("title", help="Название задачи")

    subparsers.add_parser("list", help="Показать задачи")

    done_parser = subparsers.add_parser("done", help="Завершить задачу")
    done_parser.add_argument("id", type=int, help="ID задачи")

    delete_parser = subparsers.add_parser("delete", help="Удалить задачу")
    delete_parser.add_argument("id", type=int, help="ID задачи")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    try:
        if args.command == "add":
            task = add_task(args.file, args.title)
            print(f"Добавлена задача #{task['id']}: {task['title']}")
        elif args.command == "list":
            tasks = load_tasks(args.file)
            if not tasks:
                print("Список задач пуст.")
            for task in tasks:
                status = "✓" if task["done"] else " "
                print(f"[{status}] #{task['id']} — {task['title']}")
        elif args.command == "done":
            if complete_task(args.file, args.id):
                print(f"Задача #{args.id} отмечена выполненной.")
            else:
                print(f"Задача #{args.id} не найдена.")
        elif args.command == "delete":
            if delete_task(args.file, args.id):
                print(f"Задача #{args.id} удалена.")
            else:
                print(f"Задача #{args.id} не найдена.")
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc


if __name__ == "__main__":
    main()

from __future__ import annotations

import json
from pathlib import Path

from .models import Todo

DEFAULT_PATH = Path.home() / ".todo_app" / "todos.json"


class TodoStore:
    """Stores todos in a JSON file."""

    def __init__(self, path: Path | str = DEFAULT_PATH) -> None:
        self.path = Path(path)

    def load(self) -> list[Todo]:
        if not self.path.exists():
            return []
        with self.path.open("r", encoding="utf-8") as f:
            return [Todo.from_dict(item) for item in json.load(f)]

    def save(self, todos: list[Todo]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("w", encoding="utf-8") as f:
            json.dump([t.to_dict() for t in todos], f, indent=2)

    def add(self, title: str) -> Todo:
        title = title.strip()
        if not title:
            raise ValueError("Title cannot be empty.")
        todos = self.load()
        next_id = max((t.id for t in todos), default=0) + 1
        todo = Todo(id=next_id, title=title)
        todos.append(todo)
        self.save(todos)
        return todo

    def complete(self, todo_id: int) -> Todo:
        todos = self.load()
        for todo in todos:
            if todo.id == todo_id:
                todo.done = True
                self.save(todos)
                return todo
        raise KeyError(todo_id)

    def delete(self, todo_id: int) -> Todo:
        todos = self.load()
        for index, todo in enumerate(todos):
            if todo.id == todo_id:
                removed = todos.pop(index)
                self.save(todos)
                return removed
        raise KeyError(todo_id)

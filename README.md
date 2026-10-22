# todo-app

A simple command-line todo app written in Python. Todos are stored in a local JSON file.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

## Usage

```bash
todo add Buy milk
todo list
todo done 1
todo delete 1
```

You can also run it as a module: `python -m todo_app list`.

Todos are saved to `~/.todo_app/todos.json`.

## Development

```bash
pytest          # run tests
ruff check .    # lint
ruff format .   # format
```

## Project layout

```
src/todo_app/
  models.py     # Todo data class
  storage.py    # JSON-backed TodoStore
  cli.py        # command-line interface
tests/          # pytest tests
```

## Roadmap

- [ ] Due dates and priorities
- [ ] SQLite storage option
- [ ] Web UI (Flask or FastAPI)

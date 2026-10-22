import pytest

from todo_app.cli import main
from todo_app.storage import TodoStore


@pytest.fixture
def store(tmp_path):
    return TodoStore(tmp_path / "todos.json")


def test_add_and_list(store, capsys):
    assert main(["add", "Buy", "milk"], store=store) == 0
    assert main(["list"], store=store) == 0
    out = capsys.readouterr().out
    assert "Added #1: Buy milk" in out
    assert "[ ] 1. Buy milk" in out


def test_done_marks_item(store, capsys):
    main(["add", "task"], store=store)
    assert main(["done", "1"], store=store) == 0
    main(["list"], store=store)
    assert "[x] 1. task" in capsys.readouterr().out


def test_delete_item(store, capsys):
    main(["add", "task"], store=store)
    assert main(["delete", "1"], store=store) == 0
    main(["list"], store=store)
    assert "No todos yet." in capsys.readouterr().out


def test_unknown_id_returns_error(store, capsys):
    assert main(["done", "5"], store=store) == 1
    assert "No todo with id 5." in capsys.readouterr().err

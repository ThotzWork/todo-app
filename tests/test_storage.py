import pytest

from todo_app.storage import TodoStore


@pytest.fixture
def store(tmp_path):
    return TodoStore(tmp_path / "todos.json")


def test_empty_store_has_no_todos(store):
    assert store.load() == []


def test_add_assigns_incrementing_ids(store):
    first = store.add("one")
    second = store.add("two")
    assert (first.id, second.id) == (1, 2)
    assert [t.title for t in store.load()] == ["one", "two"]


def test_add_rejects_blank_title(store):
    with pytest.raises(ValueError):
        store.add("   ")


def test_complete_marks_done_and_persists(store):
    todo = store.add("task")
    store.complete(todo.id)
    assert store.load()[0].done is True


def test_delete_removes_todo(store):
    todo = store.add("task")
    store.delete(todo.id)
    assert store.load() == []


def test_missing_id_raises_keyerror(store):
    with pytest.raises(KeyError):
        store.complete(99)
    with pytest.raises(KeyError):
        store.delete(99)


def test_ids_are_not_reused_after_delete(store):
    store.add("one")
    second = store.add("two")
    store.delete(second.id)
    assert store.add("three").id == 2

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence

from .storage import TodoStore


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="todo", description="A simple todo app.")
    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", help="add a todo")
    add.add_argument("title", nargs="+", help="what needs doing")

    sub.add_parser("list", help="list all todos")

    done = sub.add_parser("done", help="mark a todo as done")
    done.add_argument("id", type=int)

    delete = sub.add_parser("delete", help="delete a todo")
    delete.add_argument("id", type=int)

    return parser


def main(argv: Sequence[str] | None = None, store: TodoStore | None = None) -> int:
    args = build_parser().parse_args(argv)
    store = store or TodoStore()

    try:
        if args.command == "add":
            todo = store.add(" ".join(args.title))
            print(f"Added #{todo.id}: {todo.title}")
        elif args.command == "list":
            todos = store.load()
            if not todos:
                print("No todos yet.")
            for todo in todos:
                mark = "x" if todo.done else " "
                print(f"[{mark}] {todo.id}. {todo.title}")
        elif args.command == "done":
            todo = store.complete(args.id)
            print(f"Completed #{todo.id}: {todo.title}")
        elif args.command == "delete":
            todo = store.delete(args.id)
            print(f"Deleted #{todo.id}: {todo.title}")
    except KeyError:
        print(f"No todo with id {args.id}.", file=sys.stderr)
        return 1
    except ValueError as error:
        print(error, file=sys.stderr)
        return 1

    return 0

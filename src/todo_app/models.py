from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class Todo:
    id: int
    title: str
    done: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Todo:
        return cls(
            id=int(data["id"]),
            title=str(data["title"]),
            done=bool(data.get("done", False)),
        )

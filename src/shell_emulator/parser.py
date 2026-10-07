"""Разбор строки ввода на команду и аргументы."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ParsedCommand:
    """Имя команды и список её аргументов."""

    name: str
    args: list = field(default_factory=list)


def parse_line(line):
    """Делит строку по пробелам; для пустой строки возвращает None."""
    parts = line.split()
    if not parts:
        return None
    return ParsedCommand(parts[0], parts[1:])

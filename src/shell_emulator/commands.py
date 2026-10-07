"""Команды первого этапа: заглушки ls и cd, команда exit."""
from __future__ import annotations

from dataclasses import dataclass

MAX_CD_ARGS = 1


@dataclass
class Result:
    """Итог выполнения команды: вывод, ошибка и просьба выйти."""

    output: str = ""
    error: str = ""
    exit_requested: bool = False


def format_stub(name, args):
    """Текст заглушки: имя команды и список её аргументов."""
    return f"{name}: аргументы = {args}\n"


def cmd_ls(args):
    """Заглушка ls: печатает своё имя и аргументы."""
    return Result(output=format_stub("ls", args))


def cmd_cd(args):
    """Заглушка cd: допускает не более одного аргумента."""
    if len(args) > MAX_CD_ARGS:
        return Result(error="cd: too many arguments\n")
    return Result(output=format_stub("cd", args))


def cmd_exit(args):
    """Команда exit: просит завершить эмулятор, аргументов нет."""
    if args:
        return Result(error="exit: too many arguments\n")
    return Result(exit_requested=True)


COMMANDS = {"ls": cmd_ls, "cd": cmd_cd, "exit": cmd_exit}

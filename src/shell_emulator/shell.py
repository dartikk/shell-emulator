"""Ядро эмулятора: заголовок, приглашение и выполнение строки."""
from __future__ import annotations

import getpass
import socket

from shell_emulator.commands import COMMANDS, Result
from shell_emulator.parser import parse_line

DEFAULT_USER = "user"
DEFAULT_HOST = "localhost"


def get_user_name():
    """Возвращает имя пользователя реальной ОС."""
    try:
        return getpass.getuser()
    except (ImportError, KeyError, OSError):
        return DEFAULT_USER


def get_host_name():
    """Возвращает имя компьютера реальной ОС."""
    return socket.gethostname() or DEFAULT_HOST


class Shell:
    """Логика эмулятора, не зависящая от окна."""

    def __init__(self):
        """Запоминает имя пользователя и компьютера."""
        self.user = get_user_name()
        self.host = get_host_name()

    def window_title(self):
        """Заголовок окна по данным ОС."""
        return f"Эмулятор - [{self.user}@{self.host}]"

    def prompt(self):
        """Приглашение к вводу."""
        return f"{self.user}@{self.host}:~$ "

    def execute(self, line):
        """Выполняет строку и возвращает Result."""
        parsed = parse_line(line)
        if parsed is None:
            return Result()
        handler = COMMANDS.get(parsed.name)
        if handler is None:
            return Result(error=f"{parsed.name}: command not found\n")
        return handler(parsed.args)

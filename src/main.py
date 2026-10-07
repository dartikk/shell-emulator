"""Точка входа: запускает графический эмулятор оболочки."""
from __future__ import annotations

import sys

from shell_emulator.shell import Shell

EXIT_OK = 0
EXIT_NO_GUI = 3


def main():
    """Запускает окно эмулятора и возвращает код завершения."""
    try:
        from shell_emulator.gui import run_gui
        run_gui(Shell())
    except ImportError:
        print("Не найден tkinter: установите его вместе с Python.")
        return EXIT_NO_GUI
    except Exception as error:
        print(f"Не удалось открыть окно: {error}")
        return EXIT_NO_GUI
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())

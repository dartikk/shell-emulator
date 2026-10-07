"""Тесты разбора строки ввода."""
import unittest

from shell_emulator.parser import parse_line


class ParseLineTests(unittest.TestCase):
    """Проверки функции parse_line."""

    def test_empty_line(self):
        """Пустая и пробельная строки не дают команды."""
        self.assertIsNone(parse_line(""))
        self.assertIsNone(parse_line("   \t "))

    def test_name_only(self):
        """Команда без аргументов."""
        parsed = parse_line("ls")
        self.assertEqual(parsed.name, "ls")
        self.assertEqual(parsed.args, [])

    def test_name_and_args(self):
        """Лишние пробелы между словами игнорируются."""
        parsed = parse_line("  ls   -l    docs ")
        self.assertEqual(parsed.name, "ls")
        self.assertEqual(parsed.args, ["-l", "docs"])


if __name__ == "__main__":
    unittest.main()

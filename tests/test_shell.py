"""Тесты выполнения команд первого этапа."""
import unittest

from shell_emulator.shell import Shell


class ShellTests(unittest.TestCase):
    """Проверки класса Shell."""

    def setUp(self):
        """Создаёт новый эмулятор для каждого теста."""
        self.shell = Shell()

    def test_title_has_user_and_host(self):
        """Заголовок строится из данных ОС."""
        title = self.shell.window_title()
        self.assertTrue(title.startswith("Эмулятор - ["))
        self.assertIn(self.shell.user + "@" + self.shell.host, title)

    def test_empty_line_is_silent(self):
        """Пустой ввод ничего не выводит."""
        result = self.shell.execute("   ")
        self.assertEqual(result.output + result.error, "")

    def test_ls_stub_prints_name_and_args(self):
        """Заглушка ls показывает своё имя и аргументы."""
        result = self.shell.execute("ls -l docs")
        self.assertIn("ls", result.output)
        self.assertIn("'-l', 'docs'", result.output)

    def test_cd_stub_prints_name_and_args(self):
        """Заглушка cd показывает своё имя и аргумент."""
        result = self.shell.execute("cd /tmp")
        self.assertIn("cd", result.output)
        self.assertIn("'/tmp'", result.output)

    def test_cd_too_many_arguments(self):
        """cd с двумя аргументами даёт ошибку."""
        result = self.shell.execute("cd a b")
        self.assertIn("too many arguments", result.error)
        self.assertEqual(result.output, "")

    def test_unknown_command(self):
        """Неизвестная команда сообщается об ошибке."""
        result = self.shell.execute("abc 1 2")
        self.assertEqual(result.error, "abc: command not found\n")

    def test_exit(self):
        """exit просит завершить работу."""
        self.assertTrue(self.shell.execute("exit").exit_requested)

    def test_exit_with_arguments(self):
        """exit с аргументами не завершает работу и даёт ошибку."""
        result = self.shell.execute("exit now")
        self.assertFalse(result.exit_requested)
        self.assertIn("too many arguments", result.error)


if __name__ == "__main__":
    unittest.main()

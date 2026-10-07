"""Графический терминал на tkinter."""
from __future__ import annotations

import tkinter as tk
from tkinter import font as tkfont

WINDOW_SIZE = "900x560"
FONT_SIZE = 11
BG_COLOR = "#1e1e1e"
FG_COLOR = "#d4d4d4"
PROMPT_COLOR = "#6a9955"
ERROR_COLOR = "#f48771"
SELECT_COLOR = "#264f78"
EDIT_KEYS = ("BackSpace", "Delete")
LEFT_KEYS = ("BackSpace", "Left")
INPUT_MARK = "input_start"
END = "end-1c"


class TerminalWindow:
    """Окно с историей вывода и строкой ввода после приглашения."""

    def __init__(self, shell):
        """Создаёт окно, виджеты и показывает первое приглашение."""
        self.shell = shell
        self.history = []
        self.history_pos = 0
        self.root = tk.Tk()
        self.root.title(shell.window_title())
        self.root.geometry(WINDOW_SIZE)
        self.text = self._build_text()
        self._bind_events()
        self._show_prompt()

    def _build_text(self):
        """Создаёт текстовое поле с полосой прокрутки и цветовыми тегами."""
        mono = tkfont.nametofont("TkFixedFont").copy()
        mono.configure(size=FONT_SIZE)
        frame = tk.Frame(self.root)
        frame.pack(fill="both", expand=True)
        text = tk.Text(
            frame, wrap="char", bg=BG_COLOR, fg=FG_COLOR, font=mono,
            insertbackground=FG_COLOR, selectbackground=SELECT_COLOR,
            padx=8, pady=6,
        )
        scroll = tk.Scrollbar(frame, command=text.yview)
        text.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        text.pack(side="left", fill="both", expand=True)
        text.tag_configure("prompt", foreground=PROMPT_COLOR)
        text.tag_configure("error", foreground=ERROR_COLOR)
        text.mark_set(INPUT_MARK, END)
        text.mark_gravity(INPUT_MARK, "left")
        return text

    def _bind_events(self):
        """Привязывает обработчики клавиш."""
        self.text.bind("<Key>", self._on_key)
        self.text.bind("<Return>", self._on_return)
        self.text.bind("<KP_Enter>", self._on_return)
        self.text.bind("<Home>", self._on_home)
        self.text.bind("<Up>", lambda event: self._on_history(-1))
        self.text.bind("<Down>", lambda event: self._on_history(1))
        self.text.bind("<<Paste>>", self._on_paste)
        self.text.focus_set()

    def _write(self, text, tag=None):
        """Добавляет текст в конец поля, при необходимости с тегом."""
        tags = (tag,) if tag else ()
        self.text.insert(END, text, *tags)
        self.text.see("end")

    def _show_prompt(self):
        """Печатает приглашение и открывает ввод."""
        self._write(self.shell.prompt(), "prompt")
        self.text.mark_set(INPUT_MARK, END)
        self.text.mark_set("insert", END)
        self.text.focus_set()

    def _cursor_before_input(self):
        """Истина, если курсор стоит левее начала ввода."""
        return self.text.compare("insert", "<", INPUT_MARK)

    def _on_key(self, event):
        """Не даёт редактировать уже выведенный текст."""
        if self._is_editing_key(event):
            self._drop_foreign_selection()
            if self._cursor_before_input():
                self.text.mark_set("insert", END)
        if self._is_move_at_start(event):
            return "break"
        return None

    @staticmethod
    def _is_editing_key(event):
        """Истина для печатных символов, BackSpace и Delete."""
        printable = bool(event.char) and event.char.isprintable()
        return printable or event.keysym in EDIT_KEYS

    def _drop_foreign_selection(self):
        """Снимает выделение, захватившее текст до приглашения."""
        has_selection = bool(self.text.tag_ranges("sel"))
        if has_selection and self.text.compare("sel.first", "<", INPUT_MARK):
            self.text.tag_remove("sel", "1.0", "end")

    def _is_move_at_start(self, event):
        """Истина, если BackSpace или Left упёрлись в приглашение."""
        at_start = self.text.compare("insert", "<=", INPUT_MARK)
        selected = bool(self.text.tag_ranges("sel"))
        return event.keysym in LEFT_KEYS and at_start and not selected

    def _on_home(self, event):
        """Home переносит курсор к началу ввода, а не строки."""
        self.text.mark_set("insert", INPUT_MARK)
        return "break"

    def _on_paste(self, event):
        """Вставка всегда идёт в строку ввода."""
        if self._cursor_before_input():
            self.text.mark_set("insert", END)
        return None

    def _on_return(self, event):
        """Выполняет введённую строку и печатает результат."""
        line = self.text.get(INPUT_MARK, END)
        self._write("\n")
        self._remember(line)
        result = self.shell.execute(line)
        self._write(result.output)
        self._write(result.error, "error")
        if result.exit_requested:
            self.root.destroy()
        else:
            self._show_prompt()
        return "break"

    def _remember(self, line):
        """Добавляет непустую строку в историю без подряд идущих повторов."""
        if line.strip() and (not self.history or self.history[-1] != line):
            self.history.append(line)
        self.history_pos = len(self.history)

    def _on_history(self, delta):
        """Стрелки вверх и вниз листают историю команд."""
        if not self.history:
            return "break"
        last = len(self.history)
        self.history_pos = max(0, min(last, self.history_pos + delta))
        self.text.delete(INPUT_MARK, END)
        if self.history_pos < last:
            self.text.insert(END, self.history[self.history_pos])
        self.text.mark_set("insert", END)
        return "break"

    def run(self):
        """Запускает главный цикл окна."""
        self.root.mainloop()


def run_gui(shell):
    """Открывает окно эмулятора и работает до команды exit."""
    TerminalWindow(shell).run()

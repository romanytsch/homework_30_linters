"""
Иногда возникает необходимость перенаправить вывод в нужное нам место внутри программы
по ходу её выполнения.
Реализуйте контекстный менеджер, который принимает два IO-объекта (например, открытые файлы)
и перенаправляет туда стандартные потоки stdout и stderr.

Аргументы контекстного менеджера должны быть непозиционными,
чтобы можно было ещё перенаправить только stdout или только stderr.
"""
import sys
from types import TracebackType
from typing import Type, Literal, IO


class Redirect:
    def __init__(self, *, stdout: IO = None, stderr: IO = None) -> None:
        self._new_stdout = stdout
        self._new_stderr = stderr
        self._old_stdout = None
        self._old_stderr = None

    def __enter__(self):
        if self._new_stdout is not None:
            self._old_stdout = sys.stdout
            sys.stdout = self._new_stdout
        if self._new_stderr is not None:
            self._old_stderr = sys.stderr
            sys.stderr = self._new_stderr
        return self

    def __exit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None
    ) -> Literal[True] | None:
        if self._new_stdout is not None:
            sys.stdout = self._old_stdout
        if self._new_stderr is not None:
            sys.stderr = self._old_stderr
        return None

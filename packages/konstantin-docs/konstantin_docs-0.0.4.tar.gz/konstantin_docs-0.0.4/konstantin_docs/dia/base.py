"""Базовая диаграмма."""

from typing import NamedTuple


class Image(NamedTuple):
    """Изображение с имененем файла."""

    filename: str
    content: bytes


class BaseDiagram:
    """Базовая диаграмма.

    Все диаграммы должны наследовать от этого класса
    """

    def __init__(
        self: "BaseDiagram",
        filename: str,
    ) -> None:
        """Создать объект базовой диаграммы."""
        self.__filename = filename

    @property
    def filename(self: "BaseDiagram") -> str:
        """Возвращает имя файла (без расширения)."""
        return self.__filename

    def get_images(self: "BaseDiagram") -> tuple[Image]:
        """Возвращает изображение."""
        raise NotImplementedError("Функция не определена.")

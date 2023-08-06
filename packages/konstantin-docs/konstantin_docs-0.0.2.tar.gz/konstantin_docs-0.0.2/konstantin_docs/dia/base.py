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
    ) -> None:
        """Создать объект базовой диаграммы."""

    def get_images(self: "BaseDiagram") -> tuple[Image]:
        """Возвращает изображение."""

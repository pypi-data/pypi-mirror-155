"""Базовые классы."""

from enum import Enum


class BaseSprites(Enum):
    """Базовая библиотека."""


class BaseSprite:
    """Базовый класс для изображений."""

    def __init__(
        self: "BaseSprite",
        common: str,
        common_sprite: str,
        sprite: BaseSprites,
    ) -> None:
        """Create base sprite."""
        self.__common = common
        self.__common_sprite = common_sprite
        self.__sprite = sprite

    @property
    def common(self: "BaseSprite") -> str:
        """Общая библиотека для импорта."""
        return f"!include <{self.__common}>"

    @property
    def sprite_full(self: "BaseSprite") -> str:
        """Импорт спрайта."""
        return f"!include <{self.__common_sprite}/{self.__sprite.value}>"

    @property
    def sprite_short(self: "BaseSprite") -> str:
        """Импорт спрайта."""
        return self.__sprite.value


class BaseC4Element:
    """Базовый элемент диаграмм."""

    def __init__(
        self: "BaseC4Element",
        label: str,
        sprite: BaseSprite | None,
    ) -> None:
        """Create BaseC4Element."""
        self.__alias = str(id(self)).replace("-", "_")
        self.__label = label
        self.__sprite = sprite

    @property
    def alias(self: "BaseC4Element") -> str:
        """Возвращает alias."""
        return self.__alias

    @property
    def label(self: "BaseC4Element") -> str:
        """Возвращает метку."""
        return self.__label

    @property
    def all_sprites(self: "BaseC4Element") -> list[BaseSprite]:
        """Возвращает все спрайты."""
        sprites: list[BaseSprite] = []
        if self.__sprite is not None:
            sprites.append(self.__sprite)
        return sprites

    @property
    def repr_sprite(self: "BaseC4Element") -> str:
        """Представление для спрайтов."""
        if self.__sprite is None:
            return ""
        return self.__sprite.sprite_short

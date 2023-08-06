"""Уровень 2 - container."""

from konstantin_docs.dia._c4.base import BaseC4Element, BaseSprite


class BaseContainer(BaseC4Element):
    """Person."""

    def __init__(
        self: "BaseContainer",
        label: str,
        sprite: BaseSprite | None,
    ) -> None:
        """Создать _BaseContainer."""
        super().__init__(
            label=label,
            sprite=sprite,
        )

    def __repr__(self: "BaseContainer") -> str:
        """Return string representation."""
        raise NotImplementedError("Метод не переопределен")


class Container(BaseContainer):
    """Container."""

    def __init__(
        self: "Container",
        label: str,
        techn: str = "",
        descr: str = "",
        sprite: BaseSprite | None = None,
    ) -> None:
        """Создать Container."""
        super().__init__(
            label=label,
            sprite=sprite,
        )
        self.__techn = techn
        self.__descr = descr

    def __repr__(self: "Container") -> str:
        """Return string representation."""
        template = """
Container({alias}, "{label}", "{techn}", "{descr}", $sprite="{sprite}")
"""
        return template.format(
            alias=self.alias,
            label=self.label,
            techn=self.__techn,
            descr=self.__descr,
            sprite=self.repr_sprite,
        )


class ContainerDb(BaseContainer):
    """ContainerDb."""

    def __init__(
        self: "ContainerDb",
        label: str,
        techn: str = "",
        descr: str = "",
        sprite: BaseSprite | None = None,
    ) -> None:
        """Создать Container."""
        super().__init__(
            label=label,
            sprite=sprite,
        )
        self.__techn = techn
        self.__descr = descr

    def __repr__(self: "ContainerDb") -> str:
        """Return string representation."""
        template = """
ContainerDb({alias}, "{label}", "{techn}", "{descr}", $sprite="{sprite}")
"""
        return template.format(
            alias=self.alias,
            label=self.label,
            techn=self.__techn,
            descr=self.__descr,
            sprite=self.repr_sprite,
        )

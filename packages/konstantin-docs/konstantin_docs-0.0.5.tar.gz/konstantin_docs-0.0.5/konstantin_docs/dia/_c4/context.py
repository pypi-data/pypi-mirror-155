"""Уровень 1 - context."""

from enum import Enum as _Enum

from konstantin_docs.dia._c4.base import BaseC4Element as _BaseC4Element
from konstantin_docs.dia._c4.base import BaseSprite as _BaseSprite
from konstantin_docs.dia._c4.container import BaseContainer as _BaseContainer


class SystemKinds(_Enum):
    """NOTUSED."""

    SYSTEMDB = "SystemDb"
    SYSTEMQUEUE = "SystemQueue"
    SYSTEMDB_EXT = "SystemDb_Ext"
    SYSTEMQUEUE_EXT = "SystemQueue_Ext"
    ENTERPRISE_BOUNDARY = "Enterprise_Boundary"
    SYSTEM_BOUNDARY = "System_Boundary"


class BaseContext(_BaseC4Element):
    """BaseContext."""

    def __init__(
        self: "BaseContext",
        label: str,
        sprite: _BaseSprite | None,
        links_container: list[_BaseContainer] | None,
    ) -> None:
        """Создать BaseContext."""
        super().__init__(
            label=label,
            sprite=sprite,
        )
        self.__links_container = links_container

    @property
    def links_container(self: "BaseContext") -> str:
        """Возвращает список вложенных контейнеров в виде строки."""
        if self.__links_container is None:
            return ""
        links_container_str = "".join(
            [repr(container) for container in self.__links_container],
        )
        return f"""{{
    {links_container_str}
}}"""

    def __repr__(self: "BaseContext") -> str:
        """Return string representation."""
        raise NotImplementedError("Метод не переопределен")


class Boundary(BaseContext):
    """System."""

    def __init__(
        self: "Boundary",
        label: str,
        boundary_type: str = "",
        links_container: list[_BaseContainer] | None = None,
    ) -> None:
        """Создать System."""
        super().__init__(
            label=label,
            sprite=None,
            links_container=links_container,
        )
        self.__boundary_type = boundary_type

    def __repr__(self: "Boundary") -> str:
        """Return string representation."""
        template = """
Boundary({alias}, "{label}", "{type}"){{{links_container}"""
        return template.format(
            alias=self.alias,
            label=self.label,
            type=self.__boundary_type,
            links_container=self.links_container,
        )


class Person(BaseContext):
    """Person."""

    def __init__(
        self: "Person",
        label: str,
        descr: str = "",
        sprite: _BaseSprite | None = None,
        links_container: list[_BaseContainer] | None = None,
    ) -> None:
        """Создать Person."""
        super().__init__(
            label=label,
            sprite=sprite,
            links_container=links_container,
        )
        self.__descr = descr

    def __repr__(self: "Person") -> str:
        """Return string representation."""
        template = """
Person({alias}, "{label}", "{descr}", $sprite="{sprite}"){links_container}"""
        return template.format(
            alias=self.alias,
            label=self.label,
            descr=self.__descr,
            sprite=self.repr_sprite,
            links_container=self.links_container,
        )


class PersonExt(BaseContext):
    """PersonExt."""

    def __init__(
        self: "PersonExt",
        label: str,
        descr: str = "",
        sprite: _BaseSprite | None = None,
        links_container: list[_BaseContainer] | None = None,
    ) -> None:
        """Создать Person."""
        super().__init__(
            label=label,
            sprite=sprite,
            links_container=links_container,
        )
        self.__descr = descr

    def __repr__(self: "PersonExt") -> str:
        """Return string representation."""
        template = """
Person_Ext({alias}, "{label}", "{descr}", $sprite=""){links_container}"""
        return template.format(
            alias=self.alias,
            label=self.label,
            descr=self.__descr,
            links_container=self.links_container,
        )


class System(BaseContext):
    """System."""

    def __init__(
        self: "System",
        label: str,
        descr: str = "",
        sprite: _BaseSprite | None = None,
        links_container: list[_BaseContainer] | None = None,
    ) -> None:
        """Создать Person."""
        super().__init__(
            label=label,
            sprite=sprite,
            links_container=links_container,
        )
        self.__descr = descr

    def __repr__(self: "System") -> str:
        """Return string representation."""
        template = """
System({alias}, "{label}", "{descr}", $sprite=""){links_container}"""
        return template.format(
            alias=self.alias,
            label=self.label,
            descr=self.__descr,
            links_container=self.links_container,
        )


class SystemBoundary(BaseContext):
    """SystemBoundary."""

    def __init__(
        self: "SystemBoundary",
        label: str,
        links_container: list[_BaseContainer] | None = None,
    ) -> None:
        """Создать SystemBoundary."""
        super().__init__(
            label=label,
            sprite=None,
            links_container=links_container,
        )

    def __repr__(self: "SystemBoundary") -> str:
        """Return string representation."""
        template = """
System_Boundary({alias}, "{label}"){links_container}"""
        return template.format(
            alias=self.alias,
            label=self.label,
            links_container=self.links_container,
        )


class SystemExt(BaseContext):
    """SystemExt."""

    def __init__(
        self: "SystemExt",
        label: str,
        descr: str = "",
        sprite: _BaseSprite | None = None,
        links_container: list[_BaseContainer] | None = None,
    ) -> None:
        """Создать Person."""
        super().__init__(
            label=label,
            sprite=sprite,
            links_container=links_container,
        )
        self.__descr = descr

    def __repr__(self: "SystemExt") -> str:
        """Return string representation."""
        template = """
System_Ext({alias}, "{label}", "{descr}", $sprite=""){links_container}"""
        return template.format(
            alias=self.alias,
            label=self.label,
            descr=self.__descr,
            links_container=self.links_container,
        )

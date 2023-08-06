"""Отношения."""

from konstantin_docs.dia._c4.base import BaseC4Element


class _RelationKinds:
    """NOTUSED."""

    BIREL = "BiRel"
    REL_UP = "Rel_Up"
    REL_DOWN = "Rel_Down"
    REL_LEFT = "Rel_Left"
    REL_RIGHT = "Rel_Right"


class BaseRelation:
    """Базовый класс для отношений."""

    def __init__(
        self: "BaseRelation",
        kind: str,
        link_from: BaseC4Element,
        link_to: BaseC4Element,
        label: str,
        techn: str = "",
        descr: str = "",
    ) -> None:
        """Создает Relation."""
        self.__kind = kind
        self.__link_from = link_from
        self.__link_to = link_to
        self.__label = label
        self.__techn = techn
        self.__descr = descr

    def __repr__(self: "BaseRelation") -> str:
        """Return string representation."""
        template = """
{kind}({link_from}, {link_to}, "{label}", "{techn}", "{descr}")"""
        return template.format(
            kind=self.__kind,
            link_from=self.__link_from.alias,
            link_to=self.__link_to.alias,
            label=self.__label,
            techn=self.__techn,
            descr=self.__descr,
        )


class Rel(BaseRelation):
    """Relation."""

    def __init__(
        self: "Rel",
        link_from: BaseC4Element,
        link_to: BaseC4Element,
        label: str,
        techn: str = "",
        descr: str = "",
    ) -> None:
        """Создает Relation."""
        super().__init__(
            kind="Rel",
            link_from=link_from,
            link_to=link_to,
            label=label,
            techn=techn,
            descr=descr,
        )


class RelBack(BaseRelation):
    """RelBack."""

    def __init__(
        self: "RelBack",
        link_from: BaseC4Element,
        link_to: BaseC4Element,
        label: str,
        techn: str = "",
        descr: str = "",
    ) -> None:
        """Создает Relation."""
        super().__init__(
            kind="Rel_Back",
            link_from=link_from,
            link_to=link_to,
            label=label,
            techn=techn,
            descr=descr,
        )


class RelNeighbor(BaseRelation):
    """Rel_Neighbor."""

    def __init__(
        self: "RelNeighbor",
        link_from: BaseC4Element,
        link_to: BaseC4Element,
        label: str,
        techn: str = "",
        descr: str = "",
    ) -> None:
        """Создает Relation."""
        super().__init__(
            kind="Rel_Neighbor",
            link_from=link_from,
            link_to=link_to,
            label=label,
            techn=techn,
            descr=descr,
        )


class RelR(BaseRelation):
    """RelR."""

    def __init__(
        self: "RelR",
        link_from: BaseC4Element,
        link_to: BaseC4Element,
        label: str,
        techn: str = "",
        descr: str = "",
    ) -> None:
        """Создает RelR."""
        super().__init__(
            kind="Rel_R",
            link_from=link_from,
            link_to=link_to,
            label=label,
            techn=techn,
            descr=descr,
        )

"""Модель C4.

Описание - https://c4model.com/
Реализация на PlantUML - https://github.com/plantuml-stdlib/C4-PlantUML


"""

from email.policy import default
from enum import Enum, auto
from re import TEMPLATE
from typing import NamedTuple


from konstantin_docs.dia.base import BaseDiagram, Image
from konstantin_docs.service.kroki import (
    DiagramTypes,
    OutputFormats,
    get_image,
)


class _BaseElement:
    """Базовый элемент диаграмм."""

    def __init__(
        self: "_BaseElement",
        label: str,
    ) -> None:
        self.__alias = str(id(self)).replace("-", "_")
        self.__label = label

    @property
    def alias(self: "_BaseElement") -> str:
        """Возвращает alias."""
        return self.__alias

    @property
    def label(self: "_BaseElement") -> str:
        """Возвращает метку."""
        return self.__label


# Relation --------------------------------------------------------------------


class RelationKinds(Enum):
    """Типы отношений."""

    REL = "Rel"
    BIREL = "BiRel"
    REL_UP = "Rel_Up"
    REL_DOWN = "Rel_Down"
    REL_LEFT = "Rel_Left"
    REL_RIGHT = "Rel_Right"
    REL_BACK = "Rel_Back"
    REL_NEIGHBOR = "Rel_Neighbor"


TEMPLATE_RELATION = """
{kind}({link_from}, {link_to}, "{label}", "{techn}", "{descr}")
"""


class Relation:
    """Relation."""

    def __init__(
        self: "Relation",
        link_from: "_BaseElement",
        link_to: "_BaseElement",
        label: str,
        techn: str = "",
        descr: str = "",
        kind: RelationKinds = RelationKinds.REL,
    ) -> None:
        """Создает Relation."""
        self.__kind = kind
        self.__link_from = link_from
        self.__link_to = link_to
        self.__label = label
        self.__techn = techn
        self.__descr = descr

    def __repr__(self: "Relation") -> str:
        """Return string representation."""
        return TEMPLATE_RELATION.format(
            kind=self.__kind.value,
            link_from=self.__link_from.alias,
            link_to=self.__link_to.alias,
            label=self.__label,
            techn=self.__techn,
            descr=self.__descr,
        )


# System ----------------------------------------------------------------------


class SystemKinds(Enum):
    """Типы персон."""

    PERSON = "Person"
    PERSON_EXT = "Person_Ext"
    SYSTEM = "System"
    SYSTEMDB = "SystemDb"
    SYSTEMQUEUE = "SystemQueue"
    SYSTEM_EXT = "System_Ext"
    SYSTEMDB_EXT = "SystemDb_Ext"
    SYSTEMQUEUE_EXT = "SystemQueue_Ext"
    BOUNDARY = "Boundary"
    ENTERPRISE_BOUNDARY = "Enterprise_Boundary"
    SYSTEM_BOUNDARY = "System_Boundary"


TEMPLATE_SYSTEM = """
{kind}({alias}, "{label}", "{descr}")
"""

TEMPLATE_SYSTEM_BOUNDARY = """
{kind}({alias}, "{label}", "{type}")
"""

TEMPLATE_SYSTEM_XXX_BOUNDARY = """
{kind}({alias}, "{label}")
"""


class System(_BaseElement):
    """Person."""

    def __init__(
        self: "System",
        label: str,
        descr: str = "",
        boundary_type: str | None = None,
        kind: SystemKinds = SystemKinds.SYSTEM,
    ) -> None:
        """Создать Person.

        :param boundary_type: учитывается только при kind == Boundary
        """
        super().__init__(
            label=label,
        )
        self.__kind = kind
        self.__descr = descr
        self.__boundary_type = boundary_type

    def __repr__(self: "System") -> str:
        """Return string representation."""
        match self.__kind:
            case SystemKinds.BOUNDARY:
                return TEMPLATE_SYSTEM_BOUNDARY.format(
                    kind=self.__kind.value,
                    alias=self.alias,
                    label=self.label,
                    type=self.__boundary_type,
                )

            case SystemKinds.ENTERPRISE_BOUNDARY | SystemKinds.SYSTEM_BOUNDARY:
                return TEMPLATE_SYSTEM_XXX_BOUNDARY.format(
                    kind=self.__kind.value,
                    alias=self.alias,
                    label=self.label,
                )

            case _:
                return TEMPLATE_SYSTEM.format(
                    kind=self.__kind.value,
                    alias=self.alias,
                    label=self.label,
                    descr=self.__descr,
                )
        return ""


# Diagram ---------------------------------------------------------------------

TEMPLATE_DIAGRAM = """
@startuml

!include C4_Container.puml

title {title}
{persons}
{rels}
@enduml
"""


class C4(BaseDiagram):
    """Диаграмма C4."""

    def __init__(
        self: "C4",
        filename: str,
        title: str = "Diagram title",
        links_system: list[System] | None = None,
        links_rel: list[Relation] | None = None,
    ) -> None:
        """Создает объект диаграммы."""
        super().__init__(filename)
        self.__title = title
        self.__link_persons = links_system
        self.__link_rels = links_rel

    def get_images(self: "BaseDiagram") -> tuple[Image]:
        print(self)

    def __repr__(self: "C4") -> str:
        """Return string representation."""
        return TEMPLATE_DIAGRAM.format(
            title=self.__title,
            persons="".join(
                [repr(person) for person in (self.__link_persons or [])],
            ),
            rels="".join([repr(rel) for rel in (self.__link_rels or [])]),
        )

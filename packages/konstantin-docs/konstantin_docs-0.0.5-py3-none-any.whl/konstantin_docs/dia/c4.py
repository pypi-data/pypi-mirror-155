"""Модель C4.

Описание - https://c4model.com/
Реализация на PlantUML - https://github.com/plantuml-stdlib/C4-PlantUML
"""

import logging

from konstantin_docs.dia._c4 import container, context, rel, sprite
from konstantin_docs.dia._c4.base import BaseSprite as _BaseSprite
from konstantin_docs.dia.base import BaseDiagram as _BaseDiagram
from konstantin_docs.dia.base import Image
from konstantin_docs.service.kroki import (
    DiagramTypes,
    OutputFormats,
    get_image,
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


# Diagram ---------------------------------------------------------------------

TEMPLATE_DIAGRAM = """@startuml

!include C4_Container.puml
{sprites}
{title}
{context}
{container}
{rels}
@enduml
"""


class C4(_BaseDiagram):
    """Диаграмма C4."""

    def __init__(
        self: "C4",
        filename: str,
        title: str = "Diagram title",
        links_context: list[context.BaseContext] | None = None,
        links_container: list[container.BaseContainer] | None = None,
        links_rel: list[rel.BaseRelation] | None = None,
    ) -> None:
        """Создает объект диаграммы."""
        super().__init__(filename)
        self.__title = title
        self.__links_context = links_context
        self.__links_container = links_container
        self.__link_rels = links_rel
        # get all sprites
        self.__sprites: list[_BaseSprite] = []
        for link in self.__links_context or []:
            self.__sprites.extend(link.all_sprites)
        for link in self.__links_container or []:
            self.__sprites.extend(link.all_sprites)

    @property
    def _repr_sprites(self: "C4") -> str:
        """Возвращает все спрайты."""
        common: set[str] = set()
        sprites: set[str] = set()
        for spr in self.__sprites:
            common.add(spr.common)
            sprites.add(spr.sprite_full)
        out = ""
        if len(common) > 0:
            out += "\n".join(common) + "\n" + "\n".join(sprites)
        return out

    def get_images(self: "C4") -> tuple[Image]:
        """Возвращает кортеж изображений."""
        images: list[Image] = []
        text = repr(self)
        images.append(self._get_text_file(".puml"))
        try:
            for fmt in (OutputFormats.PNG, OutputFormats.SVG):
                images.append(
                    Image(
                        filename=self.filename + "." + fmt.value,
                        content=get_image(
                            source=text,
                            diagram_type=DiagramTypes.C4PLANTUML,
                            output_format=fmt,
                        ),
                    ),
                )
        except RuntimeError as exc:
            logger.exception(exc)
        return tuple(images)

    def __repr__(self: "C4") -> str:
        """Return string representation."""
        dia = TEMPLATE_DIAGRAM.format(
            sprites=self._repr_sprites,
            title=f"title {self.__title}" if self.__title != "" else "",
            context="".join(
                [repr(context) for context in (self.__links_context or [])],
            ),
            container="".join(
                [
                    repr(container)
                    for container in (self.__links_container or [])
                ],
            ),
            rels="".join([repr(rel) for rel in (self.__link_rels or [])]),
        )
        # logger.debug(dia)
        return dia


if __name__ == "__main__":
    _ = sprite.tupadr3.FontAwesome5(sprite.tupadr3.FontAwesome5Lib.AD)

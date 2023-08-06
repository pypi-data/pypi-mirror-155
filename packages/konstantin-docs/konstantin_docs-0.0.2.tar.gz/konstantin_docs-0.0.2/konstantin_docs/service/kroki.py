"""Interaction with https://kroki.io."""
import json
from enum import Enum, auto

import requests

URL = "https://kroki.io"


class DiagramTypes(Enum):
    """Diagram types."""

    GRAPHIZ = auto()
    NWDIAG = auto()


class OutputFormats(Enum):
    """Output formats."""

    PNG = auto()
    SVG = auto()


def get_image(
    source: str,
    diagram_type: DiagramTypes,
    output_format: OutputFormats,
) -> bytes:
    """Возвращает изображение."""
    response = requests.post(
        url=URL,
        data=json.dumps(
            {
                "diagram_source": source,
                "diagram_type": diagram_type.name.lower(),
                "output_format": output_format.name.lower(),
            },
        ),
    )
    if response.status_code != 200:
        raise RuntimeError(response.content)
    return response.content

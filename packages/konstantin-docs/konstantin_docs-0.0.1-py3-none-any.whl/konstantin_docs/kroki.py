"""Interaction with https://kroki.io."""
import json
from enum import Enum, auto

import requests

URL = 'https://kroki.io'


class DiagramType(Enum):
    """Diagram types."""

    graphviz = auto()


class OutputFormat(Enum):
    """Output formats."""

    png = auto()
    svg = auto()


class Diagram:
    """Class for diagram."""

    def __init__(
        self: 'Diagram',
        filename: str,
        diagram_source: str,
        diagram_type: DiagramType,
        output_formats: list[OutputFormat],
    ) -> None:
        """Create diagram."""
        self.filename = filename
        self.diagram_source = diagram_source
        self.diagram_type = diagram_type
        self.output_formats = output_formats

    def generate(self: 'Diagram') -> None:
        """Generate diagrams."""
        for output_format in self.output_formats:
            response = requests.post(
                url=URL,
                data=json.dumps(
                    {
                        'diagram_source': self.diagram_source,
                        'diagram_type': self.diagram_type.name,
                        'output_format': output_format.name,
                    },
                ),
            )
            with open(f'{self.filename}.{output_format.name}', 'wb') as f:
                f.write(response.content)
            print(response.text)

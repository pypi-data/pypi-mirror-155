import kroki

DIAGRAM_TYPE = kroki.DiagramType.graphviz
OUTPUT_FORMATS = [kroki.OutputFormat.svg, kroki.OutputFormat.png]

dia = kroki.Diagram(
    filename='test',
    diagram_source='digraph G {Hello->World}',
    diagram_type=DIAGRAM_TYPE,
    output_formats=OUTPUT_FORMATS,
)
dia.generate()

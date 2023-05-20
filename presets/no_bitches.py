from util.graph import Edge, Graph, Node
from util.types import Box


class NoBitchesGenerator(Graph):
    type = "no_bitches"

    def __init__(self):
        super().__init__(
            nodes=dict(
                paste=Node(type="fgpaste"),
                asset=Node(type="fromasset"),
                textgen=Node(type="text_smart"),
            ),
            edges=[
                # generate text
                Edge(source=None, signal=None, target="textgen", slot="text"),
                Edge(source=None, signal="box", target="textgen", slot="box"),
                Edge(source=None, signal="font", target="textgen", slot="font"),
                Edge(source=None, signal="fill_color", target="textgen", slot="fill_color"),
                Edge(source=None, signal="stroke_color", target="textgen", slot="stroke_color"),
                Edge(source=None, signal="stroke_width", target="textgen", slot="stroke_width"),
                # params to paster
                Edge(source="textgen", signal=None, target="paste", slot="image"),
                Edge(source=None, signal="assetname", target="asset", slot="name"),
                Edge(source="asset", signal=None, target="paste", slot="canvas"),
                Edge(source=None, signal="box", target="paste", slot="box"),
                # final edge
                Edge(source="paste", signal=None, target=None, slot=None)
            ],
            vars=dict(
                box=Box(x1=20, x2=519, y1=20, y2=120),
                assetname="megamind_no_bitches.png",
                font="impact",
                fill_color=(255, 255, 255),
                stroke_color=(0, 0, 0, 255),
                stroke_width=5,
            )
        )

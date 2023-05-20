from util.graph import Edge, Graph, Node


class TextEchoTest(Graph):
    type = "test"

    def __init__(self):
        super().__init__(
            nodes=dict(
                echo=Node(type="echo.text")
            ),
            edges=[
                Edge(source=None, signal=None, target="echo", slot="text"),
                Edge(source="echo", signal=None, target=None, slot=None)
            ]
        )

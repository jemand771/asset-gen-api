import inspect
from dataclasses import dataclass, field
from typing import Any

from . import loader
from .types import GeneratorBase


@dataclass
class SignalSlot:
    type: type
    name: str
    optional = False


@dataclass
class Node:
    type: str
    signals: list[SignalSlot] = field(default_factory=lambda: [])
    slots: list[SignalSlot] = field(default_factory=lambda: [])
    generator: GeneratorBase | None = None

    def __post_init__(self):
        self.generator = loader.registry.find_generator(self.type)
        sig = inspect.signature(self.generator.run)
        # TODO populate signals and slots
        # this will resolve the ugly [None]-indexing hack during execution
        # (don't just guess whether a generator returns a single value or multiple)

    @classmethod
    def from_json(cls, data):
        return cls(**data)


@dataclass
class Edge:
    source: str | None  # source none for input provider
    target: str | None  # target none for output provider
    signal: str | None  # signal none for default output (return value)
    slot: str | None  # slot none for default input (e.g. on final output stage)

    @classmethod
    def from_json(cls, data):
        return cls(**data)


@dataclass
class Graph:
    type: str | None = None  # possibly use a subgraph like a node
    nodes: dict[str, Node] = field(default_factory=lambda: {})
    edges: list[Edge] = field(default_factory=lambda: [])
    vars: dict[str, Any] = field(default_factory=lambda: {})

    @classmethod
    def from_json(cls, data):
        inst = cls()
        inst.nodes = {
            id_: Node.from_json(node)
            for id_, node in data.get("nodes", {}).items()
        }
        inst.edges = [
            Edge.from_json(edge)
            for edge in data.get("edges", [])
        ]
        inst.verify()
        return inst

    def verify(self):
        if self.count_nodes("io.output") != 1:
            raise ValueError("graph needs exactly one output node")
        if any(
            (
                edge.source is not None and edge.source not in self.nodes
                or edge.target is not None and edge.target not in self.nodes
            )
                for edge in self.edges
        ):
            raise ValueError("edge connected to unknown node")

    def count_nodes(self, type_: str):
        return sum(1 for node in self.nodes.values() if node.type == type_)

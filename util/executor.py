from dataclasses import dataclass, field
from typing import Any

from util.graph import Edge, Graph
from util.loader import Registry


@dataclass
class Executor:
    registry: Registry
    graph: Graph
    inputs: dict[str | None, Any] = field(default_factory=lambda: {})
    _cache: dict[str | None, Any] = field(default_factory=lambda: {})

    def __post_init__(self):
        self.inputs = {
            **self.graph.vars,
            **self.inputs
        }

    def execute(self):
        final_edges = [edge for edge in self.graph.edges if edge.target is None]
        if len(final_edges) != 1:
            raise ValueError("only one final edge is currently supported")  # TODO more?
        edge, = final_edges
        final_result_dict = self.follow_edges([edge])
        return final_result_dict[edge.slot]

    def follow_edges(self, edges: list[Edge]):
        slot_values = {}
        for edge in edges:
            source_node_result = self.execute_node(edge.source)
            picked_value = source_node_result if edge.signal is None and edge.source is not None else \
            source_node_result[edge.signal]
            slot_values[edge.slot] = picked_value
        return slot_values

    def execute_node(self, node_id: str) -> dict[str, Any]:
        if node_id in self._cache:
            return self._cache[node_id]
        if node_id is None:
            # resolving raw input
            return self.inputs
        node = self.graph.nodes[node_id]
        slot_values = self.follow_edges([edge for edge in self.graph.edges if edge.target == node_id])
        result = node.generator.run(**slot_values)
        self._cache[node_id] = result
        return result

from dataclasses import dataclass
from typing import Optional, List, Dict, Union

@dataclass
class Edge:
    u: int
    v: Optional[int]
    weight: float
    observable: int = 0

@dataclass
class CompressedEdge:
    source_a: int
    source_b: Optional[int]
    observable_mask: int

@dataclass
class Match:
    region_a: int
    region_b: int
    compressed_edge: CompressedEdge
    path_a: Optional[List[int]] = None
    path_b: Optional[List[int]] = None

@dataclass
class BoundaryMatch:
    region_id: int
    source_detector: int
    observable_mask: int
    path: Optional[List[int]] = None

class DetectorGraph:
    def __init__(self):
        self.adj: Dict[int, List[Edge]] = {}

    def add_node(self, node: int) -> None:
        if node not in self.adj:
            self.adj[node] = []

    def add_edge(self, edge: Edge) -> None:
        self.add_node(edge.u)
        self.adj[edge.u].append(edge)

        if edge.v is not None:
            self.add_node(edge.v)
            reverse = Edge(
                u=edge.v,
                v=edge.u,
                weight=edge.weight,
                observable=edge.observable,
            )
            self.adj[edge.v].append(reverse)

    def neighbors(self, node: int) -> List[Edge]:
        return self.adj.get(node, [])
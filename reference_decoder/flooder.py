import heapq
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Union
from graph import Edge, CompressedEdge, Match, BoundaryMatch

class Region:
    next_id = 0

    def __init__(self, source: int):
        self.id = Region.next_id
        Region.next_id += 1
        self.source = source
        self.growing = True
        self.matched = False
        self.nodes = {source}

@dataclass(order=True)
class Event:
    time: float
    event_id: int
    event_type: str = field(compare=False)
    node_u: int = field(compare=False)
    node_v: int = field(compare=False)
    region_a: int = field(compare=False)
    edge: Optional[Edge] = field(default=None, compare=False)

class Flooder:
    def __init__(self, graph: Any, verbose: bool = True):
        self.graph = graph
        self.verbose = verbose
        self.node_region: Dict[int, Region] = {}
        self.node_source: Dict[int, int] = {}
        self.node_observable: Dict[int, int] = {}
        self.parent: Dict[int, Optional[int]] = {}
        self.regions: Dict[int, Region] = {}
        self.matches: List[Union[Match, BoundaryMatch]] = []
        self.time: float = 0.0
        self.events: List[Event] = []
        self._event_counter: int = 0

    def log(self, msg: str) -> None:
        if self.verbose:
            print(f"[t={self.time:.1f}] {msg}")

    def push_event(
        self, 
        time: float, 
        event_type: str,
        node_u: int, 
        node_v: int, 
        region_a: int, 
        edge: Optional[Edge]
    ) -> None:
        self._event_counter += 1
        heapq.heappush(
            self.events,
            Event(
                time=time, 
                event_id=self._event_counter, 
                event_type=event_type,
                node_u=node_u, 
                node_v=node_v, 
                region_a=region_a, 
                edge=edge
            )
        )

    def create_region(self, source: int) -> Region:
        region = Region(source)
        self.node_region[source] = region
        self.node_source[source] = source
        self.node_observable[source] = 0
        self.parent[source] = None
        self.regions[region.id] = region

        self.log(f"Created Region {region.id} rooted at Detector {source}")
        self.schedule_growth(source, region)
        return region

    def schedule_growth(self, node: int, region: Region) -> None:
        for edge in self.graph.neighbors(node):
            arrival_time = self.time + edge.weight
            if edge.v is None:
                self.push_event(
                    time=arrival_time,
                    event_type="BOUNDARY",
                    node_u=node,
                    node_v=-1,
                    region_a=region.id,
                    edge=edge
                )
                self.log(f"Scheduled BOUNDARY event from Node {node} at t={arrival_time:.1f}")
            else:
                self.push_event(
                    time=arrival_time,
                    event_type="ARRIVE",
                    node_u=node,
                    node_v=edge.v,
                    region_a=region.id,
                    edge=edge
                )
                self.log(f"Scheduled ARRIVE event from Node {node} -> Node {edge.v} at t={arrival_time:.1f}")

    def reconstruct_path(self, node: int) -> List[int]:
        path = []
        current = node
        while current is not None:
            path.append(current)
            current = self.parent[current]
        return path

    def process_boundary(self, event: Event) -> Optional[BoundaryMatch]:
        r1 = self.regions[event.region_a]
        if r1.matched:
            return None

        edge_obs = event.edge.observable if event.edge else 0
        source = self.node_source[event.node_u]
        obs = self.node_observable[event.node_u] ^ edge_obs
        path = self.reconstruct_path(event.node_u)

        b_match = BoundaryMatch(
            region_id=event.region_a,
            source_detector=source,
            observable_mask=obs,
            path=path
        )
        r1.matched = True
        self.matches.append(b_match)
        self.log(f"[BOUNDARY COLLISION] Region {r1.id} (source={source}) hit boundary. Reconstructed Path: {path}")
        return b_match

    def process_arrive(self, event: Event) -> Optional[Match]:
        r1 = self.regions[event.region_a]
        if r1.matched:
            return None

        target = event.node_v
        edge_obs = event.edge.observable if event.edge else 0

        # Claim node (if unvisited)
        if target not in self.node_region:
            self.node_region[target] = r1
            self.node_source[target] = self.node_source[event.node_u]
            self.node_observable[target] = self.node_observable[event.node_u] ^ edge_obs
            self.parent[target] = event.node_u
            r1.nodes.add(target)

            self.log(f"Region {r1.id} claimed Node {target} (parent={event.node_u}, obs_mask={self.node_observable[target]})")
            self.schedule_growth(target, r1)

        # Region-to-region collision
        else:
            r2 = self.node_region[target]
            if r2.id != event.region_a and not r2.matched:
                obs = (
                    self.node_observable[event.node_u] 
                    ^ self.node_observable[target] 
                    ^ edge_obs
                )
                path_a = self.reconstruct_path(event.node_u)
                path_b = self.reconstruct_path(target)

                compressed = CompressedEdge(
                    source_a=self.node_source[event.node_u],
                    source_b=self.node_source[target],
                    observable_mask=obs,
                )
                match = Match(
                    region_a=event.region_a,
                    region_b=r2.id,
                    compressed_edge=compressed,
                    path_a=path_a,
                    path_b=path_b
                )
                r1.matched = True
                r2.matched = True
                self.matches.append(match)
                self.log(
                    f"[REGION COLLISION] Region {r1.id} (src={match.compressed_edge.source_a}) hit Region {r2.id} (src={match.compressed_edge.source_b}) "
                    f"at Node {target}. Path A: {path_a}, Path B: {path_b}, Obs Mask: {obs}"
                )
                return match

        return None

    def run(self) -> List[Union[Match, BoundaryMatch]]:
        self.log("--- Starting Flooder Event Loop ---")
        while self.events:
            event = heapq.heappop(self.events)
            self.time = event.time
            if event.event_type == "BOUNDARY":
                self.process_boundary(event)
            elif event.event_type == "ARRIVE":
                self.process_arrive(event)
        self.log("--- Flooder Event Loop Completed ---\n")

        return self.matches
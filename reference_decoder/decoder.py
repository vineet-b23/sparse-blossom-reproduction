from flooder import Flooder, Region
from graph import DetectorGraph, Match, BoundaryMatch
from typing import List, Union

class ReferenceDecoder:
    def __init__(self, graph: DetectorGraph):
        self.graph = graph

    def decode(self, syndrome: List[int], verbose: bool = True) -> List[Union[Match, BoundaryMatch]]:
        Region.next_id = 0
        flooder = Flooder(self.graph, verbose=verbose)

        for detector in syndrome:
            flooder.create_region(detector)

        return flooder.run()
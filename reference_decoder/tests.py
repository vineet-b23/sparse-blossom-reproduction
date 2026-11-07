from graph import Edge, DetectorGraph, Match, BoundaryMatch
from decoder import ReferenceDecoder

def test_phase6_path_reconstruction():
    print("  PHASE 6 TEST: LAZY PATH RECONSTRUCTION & LOGGING  ")
    
    # Boundary --- 0 --- 1 --- 2 --- Boundary
    graph = DetectorGraph()
    graph.add_edge(Edge(0, None, weight=2.0, observable=1)) # Left boundary
    graph.add_edge(Edge(0, 1, weight=1.0, observable=1))
    graph.add_edge(Edge(1, 2, weight=1.0, observable=0))
    graph.add_edge(Edge(2, None, weight=2.0, observable=0)) # Right boundary

    decoder = ReferenceDecoder(graph)

    print("\n--- Test Case 1: Region-to-Region Collision [0, 2] ---")
    matches_1 = decoder.decode([0, 2], verbose=True)
    
    for idx, m in enumerate(matches_1):
        print(f"Match {idx + 1}: {m}")
        if isinstance(m, Match):
            print(f"  -> Combined Path: {m.path_a} <-> {m.path_b[::-1]}")
            print(f"  -> Observable Mask: {m.compressed_edge.observable_mask}")

    assert len(matches_1) == 1, f"Expected 1 match, got {len(matches_1)}"
    m1 = matches_1[0]
    assert isinstance(m1, Match)
    assert m1.path_a is not None and m1.path_b is not None

    print("\n--- Test Case 2: Boundary Match [0] ---")
    matches_2 = decoder.decode([0], verbose=True)
    for idx, m in enumerate(matches_2):
        print(f"Match {idx + 1}: {m}")
        if isinstance(m, BoundaryMatch):
            print(f"  -> Path to Boundary: {m.path}")
            print(f"  -> Observable Mask: {m.observable_mask}")

    assert len(matches_2) == 1, f"Expected 1 boundary match, got {len(matches_2)}"
    m2 = matches_2[0]
    assert isinstance(m2, BoundaryMatch)

    print("\nPhase 6 Milestone complete!")

if __name__ == "__main__":
    test_phase6_path_reconstruction()
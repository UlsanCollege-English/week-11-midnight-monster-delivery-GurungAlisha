"""Week 11: Midnight Monster Delivery.

Implement Dijkstra's algorithm using a heap-based priority queue.

Rules:
- Use Python 3.11+.
- Use the standard library only.
- Use heapq for the priority queue.
- Edge weights must be positive.
"""

import heapq
from math import inf


HAUNTED_CITY = {
    "Crypt Kitchen": {
        "Fog Alley": 2,
        "Bone Bridge": 5,
    },
    "Fog Alley": {
        "Moon Bridge": 1,
        "Goblin Market": 6,
    },
    "Bone Bridge": {
        "Goblin Market": 2,
    },
    "Moon Bridge": {
        "Werewolf Den": 5,
        "Goblin Market": 3,
    },
    "Goblin Market": {
        "Vampire Tower": 5,
    },
    "Werewolf Den": {
        "Vampire Tower": 2,
    },
    "Vampire Tower": {},
}


def validate_haunted_map(graph: dict[str, dict[str, int]]) -> None:
    """Raise ValueError if the haunted map is invalid.

    A valid haunted map:
    - is a dictionary
    - each node maps to a dictionary of neighbors
    - every neighbor is also a node in the graph
    - every edge weight is positive

    Args:
        graph: Weighted graph represented as an adjacency dictionary.

    Raises:
        ValueError: If the graph is invalid.
    """
    if not isinstance(graph, dict):
        raise ValueError("Graph must be a dictionary.")

    for node, neighbors in graph.items():
        if not isinstance(neighbors, dict):
            raise ValueError(
                f"Node '{node}' must map to a dictionary of neighbors."
            )
        for neighbor, weight in neighbors.items():
            if neighbor not in graph:
                raise ValueError(
                    f"Neighbor '{neighbor}' of '{node}' is not a node in the graph."
                )
            if not isinstance(weight, (int, float)) or weight <= 0:
                raise ValueError(
                    f"Edge weight from '{node}' to '{neighbor}' must be positive, got {weight}."
                )


def monster_delivery_costs(
    graph: dict[str, dict[str, int]],
    start: str,
) -> dict[str, float]:
    """Return the cheapest delivery cost from start to every location.

    Use Dijkstra's algorithm with heapq.

    Args:
        graph: Weighted graph represented as an adjacency dictionary.
        start: Starting location.

    Returns:
        Dictionary mapping each location to its cheapest known cost.
        Unreachable locations should stay as math.inf.

    Raises:
        ValueError: If the graph is invalid or start is missing.
    """
    validate_haunted_map(graph)
    if start not in graph:
        raise ValueError(f"Start location '{start}' is not in the graph.")

    # Initialise all costs to infinity, then set start to 0.
    costs: dict[str, float] = {node: inf for node in graph}
    costs[start] = 0

    # Min-heap entries are (cost, node).
    heap: list[tuple[float, str]] = [(0, start)]

    while heap:
        current_cost, current_node = heapq.heappop(heap)

        # Skip if we already found a cheaper path to this node.
        if current_cost > costs[current_node]:
            continue

        for neighbor, weight in graph[current_node].items():
            new_cost = current_cost + weight
            if new_cost < costs[neighbor]:
                costs[neighbor] = new_cost
                heapq.heappush(heap, (new_cost, neighbor))

    return costs


def shortest_monster_delivery(
    graph: dict[str, dict[str, int]],
    start: str,
    target: str,
) -> tuple[float, list[str]]:
    """Return the cheapest cost and path from start to target.

    Use Dijkstra's algorithm with heapq and reconstruct the path using
    a previous-node map.

    Args:
        graph: Weighted graph represented as an adjacency dictionary.
        start: Starting location.
        target: Destination location.

    Returns:
        (cost, path), where path is in start-to-target order.
        If start or target is missing, return (math.inf, []).
        If target is unreachable, return (math.inf, []).
        If start equals target, return (0, [start]).
    """
    validate_haunted_map(graph)

    if start not in graph or target not in graph:
        return (inf, [])

    if start == target:
        return (0, [start])

    costs: dict[str, float] = {node: inf for node in graph}
    costs[start] = 0
    previous: dict[str, str | None] = {node: None for node in graph}

    heap: list[tuple[float, str]] = [(0, start)]

    while heap:
        current_cost, current_node = heapq.heappop(heap)

        if current_cost > costs[current_node]:
            continue

        for neighbor, weight in graph[current_node].items():
            new_cost = current_cost + weight
            if new_cost < costs[neighbor]:
                costs[neighbor] = new_cost
                previous[neighbor] = current_node
                heapq.heappush(heap, (new_cost, neighbor))

    # Target is unreachable.
    if costs[target] == inf:
        return (inf, [])

    # Reconstruct path by walking backwards through previous-node map.
    path: list[str] = []
    node: str | None = target
    while node is not None:
        path.append(node)
        node = previous[node]
    path.reverse()

    return (costs[target], path)


def best_next_monster_stop(
    graph: dict[str, dict[str, int]],
    start: str,
    targets: list[str],
) -> tuple[str, float]:
    """Return the reachable target with the cheapest delivery cost.

    Stretch challenge.

    Rules:
    - Ignore unreachable targets.
    - If no target is reachable, return ("", math.inf).
    - If there is a tie, return the target that appears first in targets.

    Args:
        graph: Weighted graph represented as an adjacency dictionary.
        start: Starting location.
        targets: Possible destination locations.

    Returns:
        A tuple of (target, cost).
    """
    validate_haunted_map(graph)
    if start not in graph:
        return ("", inf)

    # Run Dijkstra once from start, then check each target.
    costs = monster_delivery_costs(graph, start)

    best_target = ""
    best_cost: float = inf

    for target in targets:
        if target not in graph:
            continue
        cost = costs[target]
        if cost < best_cost:
            best_cost = cost
            best_target = target

    return (best_target, best_cost)
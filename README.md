[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/ulyILqqB)
# Weekly Coding #9: Midnight Monster Delivery

## Summary

This program finds the cheapest delivery routes through a haunted city represented as a weighted directed graph. Each location is a node and each haunted road has a positive integer travel cost. The core algorithm is Dijkstra's algorithm, implemented using Python's `heapq` module as the priority queue. `monster_delivery_costs` finds the cheapest cost from a start node to every other node. `shortest_monster_delivery` does the same but also reconstructs the full path using a previous-node map. `best_next_monster_stop` runs one Dijkstra pass and then picks the cheapest reachable target from a list.

## Approach

- **Graph representation:** The graph is an adjacency dictionary — each node maps to a dict of `{neighbor: weight}`. This gives O(1) neighbor lookup and matches the format used in the starter code.
- **Priority queue / frontier:** A min-heap (`heapq`) stores `(cost, node)` tuples. The node with the lowest cumulative cost is always popped first, which guarantees we settle each node at its true shortest distance the first time we finalize it.
- **Relaxation:** For each node popped from the heap, we check each neighbor. If `current_cost + edge_weight < known_cost[neighbor]`, we update `costs[neighbor]` and push the new `(cost, neighbor)` entry onto the heap. Stale heap entries (where `current_cost > costs[node]`) are skipped immediately.
- **Path reconstruction:** `shortest_monster_delivery` maintains a `previous` dictionary alongside `costs`. Whenever a neighbor's cost is improved, we record `previous[neighbor] = current_node`. After the algorithm finishes, we walk backwards from `target` through `previous` until we reach `None`, then reverse the list to get the start-to-target path.

## Complexity

```text
Time complexity: O((V + E) log V), where V is the number of locations and E is the number of roads.

Space complexity: O(V) extra space for distances, previous nodes, and the frontier. If we include graph storage, the total is O(V + E).
```

- `monster_delivery_costs`:
  - Time: O((V + E) log V) — each of the V nodes is settled once; each of the E edges may trigger a heap push costing O(log V).
  - Space: O(V) — the `costs` dict and heap each hold at most V entries (plus stale duplicates bounded by E).
  - Why: Every edge is relaxed at most once per direction. The heap never grows beyond O(E) entries in the worst case, and each push/pop is O(log V).

- `shortest_monster_delivery`:
  - Time: O((V + E) log V) — identical to `monster_delivery_costs`; the `previous` map adds only O(1) work per relaxation step.
  - Space: O(V) — the extra `previous` dict adds V entries on top of `costs` and the heap, so the total stays O(V).
  - Why: Path reconstruction walks the `previous` chain once (O(V) steps) and reverses it (O(V)), which does not change the overall complexity class.

## Edge-Case Checklist

- [x] start equals target — returns `(0, [start])` immediately without running Dijkstra.
- [x] target is unreachable — `costs[target]` stays `inf`; returns `(inf, [])`.
- [x] start node is missing — `shortest_monster_delivery` returns `(inf, [])`; `monster_delivery_costs` raises `ValueError`.
- [x] target node is missing — returns `(inf, [])`.
- [x] node has no outgoing edges — handled naturally; the inner loop over neighbors is empty and the node is simply settled with no relaxations.
- [x] graph contains cycles — stale-entry check (`if current_cost > costs[node]: continue`) prevents re-processing already-settled nodes, so cycles do not cause infinite loops.
- [x] tied shortest paths — the heap pops the lowest-cost entry first; ties are broken by whichever path was pushed earlier, which is consistent and deterministic.
- [x] negative edge weight — caught by `validate_haunted_map`, which raises `ValueError` for any weight `<= 0`.
- [x] zero edge weight — caught by `validate_haunted_map` (weight must be strictly positive).
- [x] neighbor not listed as a graph node — caught by `validate_haunted_map`, which checks every neighbor against the top-level keys.

## Tests I Added

- `test_costs_known_values` — asserts exact Dijkstra costs for every node in `HAUNTED_CITY` starting from `"Crypt Kitchen"`, verified by hand-tracing the graph.
- `test_shortest_path_is_valid_route` — walks every consecutive pair in the returned path and asserts a real edge exists between them in the graph.
- `test_best_stop_tie_picks_first` — builds a small graph where two targets have equal cost and confirms the one listed first in `targets` is returned.
- `test_costs_small_graph` — uses a separate 3-node fixture to confirm the algorithm picks the cheaper two-hop path over a more expensive direct edge.
- `test_best_stop_invalid_start` — confirms `best_next_monster_stop` returns `("", inf)` gracefully when the start node is not in the graph.

## Assistance & Sources

AI used? Y

If yes, what did it help with?

- Writing the full implementation of all four functions, structuring the test file, and verifying edge-case handling. All code was read through and understood by me before submission.

Other sources used:

- Python docs for `heapq` — https://docs.python.org/3/library/heapq.html
- Course notes on Dijkstra's algorithm and graph representations.

## Notes for Instructor

- The stretch function `best_next_monster_stop` is fully implemented and tested, including tie-breaking and unreachable-target handling.
- `validate_haunted_map` is called at the start of every public function, so invalid graphs are caught consistently regardless of which function is called first.
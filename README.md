[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/ulyILqqB)
# Weekly Coding #9: Midnight Monster Delivery

## Summary

Write 3–6 lines explaining what this program does.

Example starting point:

This program finds the cheapest delivery routes through a haunted city. Each location is a node, and each haunted road has a positive travel cost. The main algorithm is Dijkstra's algorithm using a heap-based priority queue.

## Approach

Explain your approach in bullets.

- How did you represent the graph?
- How did you use the priority queue/frontier?
- How did relaxation work in your solution?
- How did you reconstruct the final path?

## Complexity

Explain the time and space complexity of your Dijkstra functions.

Suggested format:

```text
Time complexity: O((V + E) log V), where V is the number of locations and E is the number of roads.

Space complexity: O(V) extra space for distances, previous nodes, and the frontier. If we include graph storage, the total is O(V + E).
```

Now write your own explanation:

- `monster_delivery_costs`:
  - Time:
  - Space:
  - Why:

- `shortest_monster_delivery`:
  - Time:
  - Space:
  - Why:

## Edge-Case Checklist

Check the cases your code handles.

- [ ] start equals target
- [ ] target is unreachable
- [ ] start node is missing
- [ ] target node is missing
- [ ] node has no outgoing edges
- [ ] graph contains cycles
- [ ] tied shortest paths
- [ ] negative edge weight
- [ ] zero edge weight
- [ ] neighbor not listed as a graph node

## Tests I Added

List any tests you added beyond the starter tests.

- 
- 
- 

## Assistance & Sources

AI used? Y/N:

If yes, what did it help with?

- 

Other sources used:

- 

## Notes for Instructor

Anything you want me to know before grading?

- 

"""
Greedy Best-First Search Implementation.
Unit 4: Informed and Local Search.
Evaluation function: f(n) = h(n), where h(n) is heuristic estimate to goal.
"""

import heapq
from typing import Dict, List, Any, Optional
from algorithms.bfs import DEFAULT_GRAPH
from algorithms.astar import DEFAULT_HEURISTICS

def greedy_best_first_search(
    start: str = 'A',
    goal: str = 'Goal',
    graph: Optional[Dict[str, List[tuple]]] = None,
    heuristics: Optional[Dict[str, float]] = None
) -> Dict[str, Any]:
    """
    Executes Greedy Best-First Search on graph using heuristic priority f(n) = h(n).
    """
    if graph is None:
        graph = DEFAULT_GRAPH
    if heuristics is None:
        heuristics = DEFAULT_HEURISTICS

    if start not in graph or goal not in graph:
        return {"error": f"Start node '{start}' or Goal node '{goal}' not present in graph."}

    # Priority queue stores tuples: (h_score, seq_id, path)
    pq = []
    seq = 0
    h_start = heuristics.get(start, 0)
    heapq.heappush(pq, (h_start, seq, [start]))

    explored_nodes = []
    visited = set()

    while pq:
        h_score, _, path = heapq.heappop(pq)
        current = path[-1]

        if current not in explored_nodes:
            explored_nodes.append(current)

        if current == goal:
            # Calculate total path cost
            total_cost = 0
            for i in range(len(path) - 1):
                u, v = path[i], path[i+1]
                for neighbor, weight in graph.get(u, []):
                    if neighbor == v:
                        total_cost += weight
                        break

            return {
                "algorithm": "Greedy Best-First Search",
                "type": "Informed Search (Heuristic-Driven)",
                "start": start,
                "goal": goal,
                "found": True,
                "path": path,
                "path_cost": total_cost,
                "explored_order": explored_nodes,
                "total_explored": len(explored_nodes),
                "evaluation_function": "f(n) = h(n)",
                "time_complexity": "O(b^m) (worst case)",
                "space_complexity": "O(b^m) (retains all nodes in memory)",
                "complete": "No (can get trapped in loops on infinite/cyclic graphs)",
                "optimal": "No (chooses nearest local heuristic step)",
                "uses_heuristic": True
            }

        if current not in visited:
            visited.add(current)
            for neighbor, _ in sorted(graph.get(current, []), key=lambda x: x[0]):
                if neighbor not in visited and neighbor not in path:
                    seq += 1
                    h_val = heuristics.get(neighbor, 0)
                    new_path = list(path)
                    new_path.append(neighbor)
                    heapq.heappush(pq, (h_val, seq, new_path))

    return {
        "algorithm": "Greedy Best-First Search",
        "found": False,
        "explored_order": explored_nodes,
        "total_explored": len(explored_nodes),
        "message": f"No path found from '{start}' to '{goal}'."
    }

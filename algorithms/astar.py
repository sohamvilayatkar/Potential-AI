"""
A* Search Algorithm Implementation.
Unit 4: Informed and Local Search.
Evaluation function: f(n) = g(n) + h(n), where g(n) is path cost and h(n) is admissible heuristic.
"""

import heapq
from typing import Dict, List, Any, Optional
from algorithms.bfs import DEFAULT_GRAPH

DEFAULT_HEURISTICS = {
    'A': 10,
    'B': 8,
    'C': 7,
    'D': 6,
    'E': 4,
    'F': 5,
    'G': 6,
    'H': 2,
    'I': 3,
    'Goal': 0
}

def astar_search(
    start: str = 'A',
    goal: str = 'Goal',
    graph: Optional[Dict[str, List[tuple]]] = None,
    heuristics: Optional[Dict[str, float]] = None
) -> Dict[str, Any]:
    """
    Executes A* heuristic search from start to goal.
    Returns optimal path, path cost, f-score evaluations, and complexity parameters.
    """
    if graph is None:
        graph = DEFAULT_GRAPH
    if heuristics is None:
        heuristics = DEFAULT_HEURISTICS

    if start not in graph or goal not in graph:
        return {"error": f"Start node '{start}' or Goal node '{goal}' not present in graph."}

    # Priority queue stores tuples: (f_score, g_cost, seq_id, path)
    pq = []
    seq = 0
    h_start = heuristics.get(start, 0)
    heapq.heappush(pq, (h_start, 0, seq, [start]))

    explored_nodes = []
    g_costs = {start: 0}

    while pq:
        f_score, g_cost, _, path = heapq.heappop(pq)
        current = path[-1]

        if current not in explored_nodes:
            explored_nodes.append(current)

        if current == goal:
            return {
                "algorithm": "A* Search",
                "type": "Informed / Heuristic Search",
                "start": start,
                "goal": goal,
                "found": True,
                "path": path,
                "path_cost": g_cost,
                "f_score": f_score,
                "explored_order": explored_nodes,
                "total_explored": len(explored_nodes),
                "evaluation_function": "f(n) = g(n) + h(n)",
                "time_complexity": "O(b^d) (worst case), much faster with good heuristic",
                "space_complexity": "O(b^d) (stores all generated nodes in memory)",
                "complete": "Yes (if step cost >= epsilon > 0)",
                "optimal": "Yes (if h(n) is admissible and consistent)",
                "uses_heuristic": True
            }

        for neighbor, edge_weight in graph.get(current, []):
            new_g = g_cost + edge_weight
            if neighbor not in g_costs or new_g < g_costs[neighbor]:
                g_costs[neighbor] = new_g
                h_val = heuristics.get(neighbor, 0)
                new_f = new_g + h_val
                seq += 1
                new_path = list(path)
                new_path.append(neighbor)
                heapq.heappush(pq, (new_f, new_g, seq, new_path))

    return {
        "algorithm": "A* Search",
        "found": False,
        "explored_order": explored_nodes,
        "total_explored": len(explored_nodes),
        "message": f"No path found from '{start}' to '{goal}'."
    }

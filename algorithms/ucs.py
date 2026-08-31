"""
Uniform Cost Search (UCS) Implementation.
Unit 3: Problem Solving & Uninformed Search.
Expands least-cost unexpanded node using priority queue (Dijkstra's search variant).
"""

import heapq
from typing import Dict, List, Any, Optional
from algorithms.bfs import DEFAULT_GRAPH

def uniform_cost_search(
    start: str = 'A',
    goal: str = 'Goal',
    graph: Optional[Dict[str, List[tuple]]] = None
) -> Dict[str, Any]:
    """
    Executes Uniform Cost Search on graph from start to goal.
    Returns optimal path, minimal cost, visited nodes, and complexity attributes.
    """
    if graph is None:
        graph = DEFAULT_GRAPH

    if start not in graph or goal not in graph:
        return {"error": f"Start node '{start}' or Goal node '{goal}' not present in graph."}

    # Priority queue stores tuples: (cumulative_cost, sequence_id, path)
    pq = []
    seq = 0
    heapq.heappush(pq, (0, seq, [start]))
    
    explored_nodes = []
    visited_costs = {}

    while pq:
        cost, _, path = heapq.heappop(pq)
        current = path[-1]

        if current not in explored_nodes:
            explored_nodes.append(current)

        if current == goal:
            return {
                "algorithm": "Uniform Cost Search (UCS)",
                "type": "Uninformed Search (Cost-Optimal)",
                "start": start,
                "goal": goal,
                "found": True,
                "path": path,
                "path_cost": cost,
                "explored_order": explored_nodes,
                "total_explored": len(explored_nodes),
                "time_complexity": "O(b^(1 + floor(C*/epsilon)))",
                "space_complexity": "O(b^(1 + floor(C*/epsilon)))",
                "complete": "Yes (if step cost >= epsilon > 0)",
                "optimal": "Yes (guaranteed minimum cost path)",
                "uses_heuristic": False
            }

        if current in visited_costs and visited_costs[current] <= cost:
            continue
        visited_costs[current] = cost

        for neighbor, edge_weight in graph.get(current, []):
            new_cost = cost + edge_weight
            if neighbor not in visited_costs or new_cost < visited_costs[neighbor]:
                seq += 1
                new_path = list(path)
                new_path.append(neighbor)
                heapq.heappush(pq, (new_cost, seq, new_path))

    return {
        "algorithm": "Uniform Cost Search (UCS)",
        "found": False,
        "explored_order": explored_nodes,
        "total_explored": len(explored_nodes),
        "message": f"No path found from '{start}' to '{goal}'."
    }

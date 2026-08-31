"""
Depth-First Search (DFS) Implementation.
Unit 3: Problem Solving & Uninformed Search.
"""

from typing import Dict, List, Any, Optional
from algorithms.bfs import DEFAULT_GRAPH

def depth_first_search(
    start: str = 'A',
    goal: str = 'Goal',
    graph: Optional[Dict[str, List[tuple]]] = None
) -> Dict[str, Any]:
    """
    Executes DFS search using LIFO stack exploration.
    Returns explored order, solution path, path cost, and complexity metadata.
    """
    if graph is None:
        graph = DEFAULT_GRAPH

    if start not in graph or goal not in graph:
        return {"error": f"Start node '{start}' or Goal node '{goal}' not present in graph."}

    stack = [[start]]
    visited = set()
    explored_nodes = []

    while stack:
        path = stack.pop()
        current = path[-1]

        if current not in explored_nodes:
            explored_nodes.append(current)

        if current == goal:
            total_cost = 0
            for i in range(len(path) - 1):
                u, v = path[i], path[i+1]
                for neighbor, weight in graph.get(u, []):
                    if neighbor == v:
                        total_cost += weight
                        break

            return {
                "algorithm": "Depth-First Search (DFS)",
                "type": "Uninformed Search",
                "start": start,
                "goal": goal,
                "found": True,
                "path": path,
                "path_cost": total_cost,
                "explored_order": explored_nodes,
                "total_explored": len(explored_nodes),
                "time_complexity": "O(b^m)",
                "space_complexity": "O(b*m)",
                "complete": "No (can get stuck in infinite loops if graph is cyclic)",
                "optimal": "No (may return non-optimal path)",
                "uses_heuristic": False
            }

        if current not in visited:
            visited.add(current)
            # Add neighbors in reverse sorted order so left-most is popped first
            for neighbor, _ in reversed(sorted(graph.get(current, []), key=lambda x: x[0])):
                if neighbor not in visited and neighbor not in path:
                    new_path = list(path)
                    new_path.append(neighbor)
                    stack.append(new_path)

    return {
        "algorithm": "Depth-First Search (DFS)",
        "found": False,
        "explored_order": explored_nodes,
        "total_explored": len(explored_nodes),
        "message": f"No path found from '{start}' to '{goal}'."
    }

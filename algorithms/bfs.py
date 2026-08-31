"""
Breadth-First Search (BFS) Implementation.
Unit 3: Problem Solving & Uninformed Search.
"""

from collections import deque
from typing import Dict, List, Any, Optional

DEFAULT_GRAPH = {
    'A': [('B', 4), ('C', 2)],
    'B': [('A', 4), ('D', 5), ('E', 10)],
    'C': [('A', 2), ('F', 4), ('G', 8)],
    'D': [('B', 5), ('H', 6)],
    'E': [('B', 10), ('H', 3)],
    'F': [('C', 4), ('I', 2)],
    'G': [('C', 8), ('I', 6)],
    'H': [('D', 6), ('E', 3), ('Goal', 2)],
    'I': [('F', 2), ('G', 6), ('Goal', 5)],
    'Goal': []
}

def breadth_first_search(
    start: str = 'A',
    goal: str = 'Goal',
    graph: Optional[Dict[str, List[tuple]]] = None
) -> Dict[str, Any]:
    """
    Executes BFS search on graph from start node to goal node.
    Returns visited order, solution path, path cost, and complexity metadata.
    """
    if graph is None:
        graph = DEFAULT_GRAPH

    if start not in graph or goal not in graph:
        return {"error": f"Start node '{start}' or Goal node '{goal}' not present in graph."}

    queue = deque([[start]])
    visited = []
    explored_nodes = []

    while queue:
        path = queue.popleft()
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
                "algorithm": "Breadth-First Search (BFS)",
                "type": "Uninformed Search",
                "start": start,
                "goal": goal,
                "found": True,
                "path": path,
                "path_cost": total_cost,
                "explored_order": explored_nodes,
                "total_explored": len(explored_nodes),
                "time_complexity": "O(b^d)",
                "space_complexity": "O(b^d)",
                "complete": "Yes (if branching factor b is finite)",
                "optimal": "Yes (if step costs are uniform)",
                "uses_heuristic": False
            }

        if current not in visited:
            visited.append(current)
            for neighbor, _ in sorted(graph.get(current, []), key=lambda x: x[0]):
                if neighbor not in visited and neighbor not in [p[-1] for p in queue]:
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append(new_path)

    return {
        "algorithm": "Breadth-First Search (BFS)",
        "found": False,
        "explored_order": explored_nodes,
        "total_explored": len(explored_nodes),
        "message": f"No path found from '{start}' to '{goal}'."
    }

"""
Missionaries and Cannibals State-Space Search Solver.
Unit 3: Problem Solving & Uninformed Search.
Finds the optimal sequence of river crossings using Breadth-First Search (BFS).
"""

from collections import deque
from typing import Dict, List, Tuple, Any

def is_valid_state(m: int, c: int, total_m: int = 3, total_c: int = 3) -> bool:
    """
    Checks if a state (m, c) on the left bank is safe and valid.
    Missionaries must never be outnumbered by cannibals on either bank (unless M == 0).
    """
    # Check boundaries
    if m < 0 or m > total_m or c < 0 or c > total_c:
        return False

    # Check left bank safety
    if m > 0 and m < c:
        return False

    # Check right bank safety
    m_right = total_m - m
    c_right = total_c - c
    if m_right > 0 and m_right < c_right:
        return False

    return True

def solve_missionaries_cannibals(
    total_missionaries: int = 3,
    total_cannibals: int = 3,
    boat_capacity: int = 2
) -> Dict[str, Any]:
    """
    Solves Missionaries & Cannibals river crossing using BFS.
    State representation: (m_left, c_left, boat_pos) where boat_pos: 1 = Left Bank, 0 = Right Bank.
    """
    start_state = (total_missionaries, total_cannibals, 1)
    goal_state = (0, 0, 0)

    # Possible boat loads (m, c) moving across
    possible_boat_moves = []
    for m in range(boat_capacity + 1):
        for c in range(boat_capacity + 1):
            if 1 <= (m + c) <= boat_capacity:
                if m == 0 or m >= c:  # Safe inside the boat
                    possible_boat_moves.append((m, c))

    queue = deque([
        (start_state, [{
            "state": start_state,
            "left_bank": f"{total_missionaries}M, {total_cannibals}C",
            "right_bank": "0M, 0C",
            "boat_location": "Left Bank",
            "action": "Initial State: All missionaries and cannibals on Left Bank"
        }])
    ])

    visited = {start_state}
    explored_states = [start_state]

    while queue:
        (curr_m, curr_c, boat), path = queue.popleft()

        if (curr_m, curr_c, boat) == goal_state:
            return {
                "algorithm": "Breadth-First Search (BFS)",
                "problem": "Missionaries & Cannibals Problem",
                "total_missionaries": total_missionaries,
                "total_cannibals": total_cannibals,
                "boat_capacity": boat_capacity,
                "solvable": True,
                "total_steps": len(path) - 1,
                "solution_path": path,
                "explored_states_count": len(explored_states),
                "rules_applied": [
                    "Boat carries 1 or 2 individuals",
                    "At least one person must row the boat",
                    "Missionaries cannot be outnumbered by Cannibals on any bank"
                ]
            }

        # Generate next states based on boat position
        for dm, dc in possible_boat_moves:
            if boat == 1:  # Moving from Left to Right
                next_m = curr_m - dm
                next_c = curr_c - dc
                next_boat = 0
                action_text = f"Send {dm} Missionaries and {dc} Cannibals from Left to Right Bank"
            else:  # Moving from Right to Left
                next_m = curr_m + dm
                next_c = curr_c + dc
                next_boat = 1
                action_text = f"Return {dm} Missionaries and {dc} Cannibals from Right to Left Bank"

            next_state = (next_m, next_c, next_boat)

            if is_valid_state(next_m, next_c, total_missionaries, total_cannibals):
                if next_state not in visited:
                    visited.add(next_state)
                    explored_states.append(next_state)
                    new_path = list(path)
                    new_path.append({
                        "state": next_state,
                        "left_bank": f"{next_m}M, {next_c}C",
                        "right_bank": f"{total_missionaries - next_m}M, {total_cannibals - next_c}C",
                        "boat_location": "Left Bank" if next_boat == 1 else "Right Bank",
                        "action": action_text
                    })
                    queue.append((next_state, new_path))

    return {
        "solvable": False,
        "error": "No valid state path found for the specified configuration."
    }

"""
Water Jug Problem State-Space Search Solver.
Unit 3: Problem Solving & Uninformed Search.
Solves the classical Water Jug problem using Breadth-First Search (BFS) state-space exploration.
"""

import math
from collections import deque
from typing import Dict, List, Tuple, Any

def solve_water_jug(
    cap_a: int = 4,
    cap_b: int = 3,
    target: int = 2
) -> Dict[str, Any]:
    """
    Finds the shortest sequence of state transitions to measure 'target' liters
    using Jug A (capacity cap_a) and Jug B (capacity cap_b).
    """
    cap_a, cap_b, target = int(cap_a), int(cap_b), int(target)

    # Solvability check using Extended Euclidean / Bezout's theorem
    gcd_val = math.gcd(cap_a, cap_b)
    if target > max(cap_a, cap_b):
        return {
            "solvable": False,
            "error": f"Target amount ({target}L) cannot exceed the maximum jug capacity ({max(cap_a, cap_b)}L)."
        }
    if target % gcd_val != 0:
        return {
            "solvable": False,
            "error": f"Target ({target}L) is not measurable with Jug A ({cap_a}L) and Jug B ({cap_b}L) because GCD({cap_a}, {cap_b}) = {gcd_val}, and {target} is not divisible by {gcd_val}."
        }

    # BFS state exploration: state = (a, b)
    # Queue stores: (state, path_of_actions_and_states)
    start_state = (0, 0)
    queue = deque([ (start_state, [{"state": (0, 0), "action": "Initial State: Both jugs empty"}]) ])
    visited = {start_state}
    explored_states = [start_state]

    while queue:
        (curr_a, curr_b), path = queue.popleft()

        # Check goal condition
        if curr_a == target or curr_b == target:
            return {
                "algorithm": "Breadth-First Search (State-Space Search)",
                "problem": "Water Jug Problem",
                "jug_a_capacity": cap_a,
                "jug_b_capacity": cap_b,
                "target_amount": target,
                "solvable": True,
                "solution_steps_count": len(path) - 1,
                "solution_path": path,
                "explored_states_count": len(explored_states),
                "explored_states": [f"({a}, {b})" for a, b in explored_states]
            }

        # Generate all 6 legal state transitions:
        next_transitions = []

        # 1. Fill Jug A completely
        if curr_a < cap_a:
            next_transitions.append(((cap_a, curr_b), f"Fill Jug A completely ({cap_a}L, {curr_b}L)"))

        # 2. Fill Jug B completely
        if curr_b < cap_b:
            next_transitions.append(((curr_a, cap_b), f"Fill Jug B completely ({curr_a}L, {cap_b}L)"))

        # 3. Empty Jug A completely
        if curr_a > 0:
            next_transitions.append(((0, curr_b), f"Empty Jug A on ground (0L, {curr_b}L)"))

        # 4. Empty Jug B completely
        if curr_b > 0:
            next_transitions.append(((curr_a, 0), f"Empty Jug B on ground ({curr_a}L, 0L)"))

        # 5. Pour from Jug A to Jug B until B is full or A is empty
        if curr_a > 0 and curr_b < cap_b:
            pour_amt = min(curr_a, cap_b - curr_b)
            next_transitions.append(((curr_a - pour_amt, curr_b + pour_amt), f"Pour from Jug A into Jug B ({curr_a - pour_amt}L, {curr_b + pour_amt}L)"))

        # 6. Pour from Jug B to Jug A until A is full or B is empty
        if curr_b > 0 and curr_a < cap_a:
            pour_amt = min(curr_b, cap_a - curr_a)
            next_transitions.append(((curr_a + pour_amt, curr_b - pour_amt), f"Pour from Jug B into Jug A ({curr_a + pour_amt}L, {curr_b - pour_amt}L)"))

        for next_state, action_desc in next_transitions:
            if next_state not in visited:
                visited.add(next_state)
                explored_states.append(next_state)
                new_path = list(path)
                new_path.append({"state": next_state, "action": action_desc})
                queue.append((next_state, new_path))

    return {
        "solvable": False,
        "error": "No solution path found in state space."
    }

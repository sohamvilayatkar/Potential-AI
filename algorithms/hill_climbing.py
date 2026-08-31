"""
Hill Climbing Optimization Algorithm.
Unit 4: Informed and Local Search.
Demonstrates iterative improvement, neighborhood evaluation, and local maxima convergence.
"""

import math
import random
from typing import Dict, List, Any, Callable

def default_objective_function(x: float) -> float:
    """Mathematical objective function: f(x) = -(x-4)^2 + 25 + 3*sin(2*x)"""
    return round(-(x - 4.0)**2 + 25.0 + 3.0 * math.sin(2.0 * x), 4)

def hill_climbing_optimization(
    start_x: float = 0.0,
    step_size: float = 0.25,
    max_iterations: int = 50,
    function_choice: str = "quadratic_sin"
) -> Dict[str, Any]:
    """
    Executes simple steepest-ascent Hill Climbing to maximize an objective function.
    Returns iteration trace, intermediate states, scores, and convergence status.
    """
    current_x = float(start_x)
    current_val = default_objective_function(current_x)
    
    history = [{
        "iteration": 0,
        "x": current_x,
        "score": current_val,
        "action": "Initial State"
    }]

    converged = False
    stop_reason = "Max iterations reached"

    for i in range(1, max_iterations + 1):
        # Generate left and right neighbors
        left_x = round(current_x - step_size, 4)
        right_x = round(current_x + step_size, 4)
        
        left_val = default_objective_function(left_x)
        right_val = default_objective_function(right_x)

        # Determine best neighbor
        if left_val > right_val:
            best_neighbor_x = left_x
            best_neighbor_val = left_val
            direction = "Left (-step)"
        else:
            best_neighbor_x = right_x
            best_neighbor_val = right_val
            direction = "Right (+step)"

        # Check for uphill improvement
        if best_neighbor_val > current_val:
            current_x = best_neighbor_x
            current_val = best_neighbor_val
            history.append({
                "iteration": i,
                "x": current_x,
                "score": current_val,
                "action": f"Moved {direction} to better neighbor"
            })
        else:
            converged = True
            stop_reason = f"Reached Peak / Local Maximum at iteration {i} (no neighbor has higher score)"
            history.append({
                "iteration": i,
                "x": current_x,
                "score": current_val,
                "action": "Local Peak Reached"
            })
            break

    return {
        "algorithm": "Hill Climbing (Steepest Ascent)",
        "type": "Local Search / Optimization",
        "objective_function": "f(x) = -(x - 4)^2 + 25 + 3*sin(2*x)",
        "start_x": start_x,
        "step_size": step_size,
        "final_x": current_x,
        "maximum_score": current_val,
        "total_iterations": len(history) - 1,
        "converged": converged,
        "status": stop_reason,
        "history": history,
        "time_complexity": "O(iterations * neighbors)",
        "space_complexity": "O(1) (retains only current state)",
        "complete": "No (can get stuck on local maxima, plateaus, or ridges)",
        "optimal": "No (finds local optimum, not guaranteed global optimum)"
    }

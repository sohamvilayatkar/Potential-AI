"""
Alpha-Beta Pruning Algorithm for Game Playing (Tic-Tac-Toe).
Unit 5: Game Playing.
Optimizes standard Minimax by pruning search branches that cannot influence the final decision.
Maintains alpha (best MAX value) and beta (best MIN value).
"""

import math
from typing import List, Dict, Any, Tuple
from algorithms.minimax import check_winner

def alphabeta(
    board: List[str],
    depth: int,
    alpha: float,
    beta: float,
    is_maximizing: bool,
    counter: Dict[str, int]
) -> int:
    """
    Recursive Alpha-Beta evaluation.
    Pruning condition: if beta <= alpha, break branch exploration.
    """
    counter["nodes_evaluated"] += 1
    winner = check_winner(board)

    if winner == 'O':
        return 10 - depth
    elif winner == 'X':
        return depth - 10
    elif winner == 'Draw':
        return 0

    if is_maximizing:
        max_eval = -math.inf
        for i in range(9):
            if board[i] == "":
                board[i] = 'O'
                score = alphabeta(board, depth + 1, alpha, beta, False, counter)
                board[i] = ""
                max_eval = max(max_eval, score)
                alpha = max(alpha, score)
                if beta <= alpha:
                    counter["pruned_branches"] += 1
                    break
        return max_eval
    else:
        min_eval = math.inf
        for i in range(9):
            if board[i] == "":
                board[i] = 'X'
                score = alphabeta(board, depth + 1, alpha, beta, True, counter)
                board[i] = ""
                min_eval = min(min_eval, score)
                beta = min(beta, score)
                if beta <= alpha:
                    counter["pruned_branches"] += 1
                    break
        return min_eval

def get_best_move_alphabeta(board: List[str]) -> Dict[str, Any]:
    """Finds the optimal move for AI ('O') using Alpha-Beta Pruning."""
    counter = {"nodes_evaluated": 0, "pruned_branches": 0}
    best_score = -math.inf
    best_move = -1
    alpha = -math.inf
    beta = math.inf
    evaluated_moves = []

    for i in range(9):
        if board[i] == "":
            board[i] = 'O'
            score = alphabeta(board, 0, alpha, beta, False, counter)
            board[i] = ""
            evaluated_moves.append({"index": i, "score": score})
            if score > best_score:
                best_score = score
                best_move = i
            alpha = max(alpha, best_score)

    return {
        "algorithm": "Alpha-Beta Pruning",
        "best_move": best_move,
        "best_score": best_score,
        "nodes_evaluated": counter["nodes_evaluated"],
        "pruned_branches": counter["pruned_branches"],
        "evaluated_moves": evaluated_moves,
        "efficiency_gain": f"Avoided redundant subtree evaluations via alpha-beta cutoffs."
    }

def alphabeta_tic_tac_toe(board: List[str]) -> Dict[str, Any]:
    """Public wrapper for AI Lab interface."""
    return get_best_move_alphabeta(board)

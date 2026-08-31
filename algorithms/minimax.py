"""
Minimax Game Playing Algorithm for Tic-Tac-Toe.
Unit 5: Game Playing.
Exhaustively explores game tree to find the optimal move for MAX player ('O') vs MIN player ('X').
"""

import math
from typing import List, Dict, Any, Tuple, Optional

def check_winner(board: List[str]) -> Optional[str]:
    """Check if 'X' or 'O' has won or if it's a draw."""
    win_patterns = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
        (0, 4, 8), (2, 4, 6)             # Diagonals
    ]
    for a, b, c in win_patterns:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a]
    if all(cell != "" for cell in board):
        return "Draw"
    return None

def minimax(
    board: List[str],
    depth: int,
    is_maximizing: bool,
    counter: Dict[str, int]
) -> int:
    """
    Minimax recursive evaluation function.
    'O' is Maximizer (+10 - depth), 'X' is Minimizer (-10 + depth), Draw is 0.
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
        best_score = -math.inf
        for i in range(9):
            if board[i] == "":
                board[i] = 'O'
                score = minimax(board, depth + 1, False, counter)
                board[i] = ""
                best_score = max(best_score, score)
        return best_score
    else:
        best_score = math.inf
        for i in range(9):
            if board[i] == "":
                board[i] = 'X'
                score = minimax(board, depth + 1, True, counter)
                board[i] = ""
                best_score = min(best_score, score)
        return best_score

def get_best_move_minimax(board: List[str]) -> Dict[str, Any]:
    """Finds the optimal move for AI ('O') using full standard Minimax."""
    counter = {"nodes_evaluated": 0}
    best_score = -math.inf
    best_move = -1
    evaluated_moves = []

    for i in range(9):
        if board[i] == "":
            board[i] = 'O'
            score = minimax(board, 0, False, counter)
            board[i] = ""
            evaluated_moves.append({"index": i, "score": score})
            if score > best_score:
                best_score = score
                best_move = i

    return {
        "algorithm": "Minimax",
        "best_move": best_move,
        "best_score": best_score,
        "nodes_evaluated": counter["nodes_evaluated"],
        "evaluated_moves": evaluated_moves
    }

def minimax_tic_tac_toe(board: List[str]) -> Dict[str, Any]:
    """Public wrapper for AI Lab interface."""
    return get_best_move_minimax(board)

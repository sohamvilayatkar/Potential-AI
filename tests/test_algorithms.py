import pytest
from algorithms import (
    breadth_first_search, depth_first_search, uniform_cost_search,
    astar_search, greedy_best_first_search, hill_climbing_optimization,
    genetic_algorithm_optimize, minimax_tic_tac_toe, alphabeta_tic_tac_toe,
    solve_water_jug, solve_missionaries_cannibals
)

def test_search_algorithms():
    bfs_res = breadth_first_search()
    assert bfs_res["found"] is True
    assert bfs_res["path"][-1] == "Goal"

    dfs_res = depth_first_search()
    assert dfs_res["found"] is True
    assert dfs_res["path"][-1] == "Goal"

    ucs_res = uniform_cost_search()
    assert ucs_res["found"] is True
    assert ucs_res["path_cost"] == 13

    astar_res = astar_search()
    assert astar_res["found"] is True
    assert astar_res["path_cost"] == 13

    greedy_res = greedy_best_first_search()
    assert greedy_res["found"] is True
    assert greedy_res["path"][-1] == "Goal"

def test_water_jug():
    res = solve_water_jug(4, 3, 2)
    assert res["solvable"] is True
    assert res["solution_steps_count"] == 4

def test_missionaries_cannibals():
    res = solve_missionaries_cannibals()
    assert res["solvable"] is True
    assert res["total_steps"] == 11

def test_tic_tac_toe_engines():
    board = ["X", "", "", "", "O", "", "", "", ""]
    mm_res = minimax_tic_tac_toe(board)
    assert 0 <= mm_res["best_move"] < 9

    ab_res = alphabeta_tic_tac_toe(board)
    assert 0 <= ab_res["best_move"] < 9
    assert ab_res["nodes_evaluated"] <= mm_res["nodes_evaluated"]

def test_optimizations():
    hc = hill_climbing_optimization()
    assert hc["converged"] is True

    ga = genetic_algorithm_optimize(population_size=10, generations=10)
    assert ga["optimal_fitness"] > 0

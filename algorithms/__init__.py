"""
Potential AI - Algorithm Modules for AI Lab
Demonstrates Uninformed Search, Informed Search, Optimization, Game Playing,
and Classic AI State-Space Search problems from the AI syllabus.
"""

from algorithms.bfs import breadth_first_search
from algorithms.dfs import depth_first_search
from algorithms.ucs import uniform_cost_search
from algorithms.astar import astar_search
from algorithms.greedy import greedy_best_first_search
from algorithms.hill_climbing import hill_climbing_optimization
from algorithms.genetic import genetic_algorithm_optimize
from algorithms.minimax import minimax_tic_tac_toe, get_best_move_minimax
from algorithms.alpha_beta import alphabeta_tic_tac_toe, get_best_move_alphabeta
from algorithms.water_jug import solve_water_jug
from algorithms.missionaries_cannibals import solve_missionaries_cannibals

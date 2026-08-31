# POTENTIAL AI - Algorithms Reference Manual
## Comprehensive Analysis of Search, Heuristic Optimization, and Game Playing AI

This document provides complete academic documentation for all 11 artificial intelligence algorithms implemented in the **POTENTIAL AI Laboratory**.

---

## Table of Contents
1. [Breadth-First Search (BFS)](#1-breadth-first-search-bfs)
2. [Depth-First Search (DFS)](#2-depth-first-search-dfs)
3. [Uniform Cost Search (UCS)](#3-uniform-cost-search-ucs)
4. [A* Search (Informed Heuristic Search)](#4-a-search)
5. [Greedy Best-First Search](#5-greedy-best-first-search)
6. [Hill Climbing Optimization](#6-hill-climbing-optimization)
7. [Genetic Algorithm (GA)](#7-genetic-algorithm)
8. [Minimax Algorithm](#8-minimax-algorithm)
9. [Alpha-Beta Pruning](#9-alpha-beta-pruning)
10. [Water Jug Problem Solver](#10-water-jug-problem-solver)
11. [Missionaries and Cannibals Problem Solver](#11-missionaries-and-cannibals-problem-solver)

---

### 1. Breadth-First Search (BFS)
* **File:** `algorithms/bfs.py`
* **Purpose:** Finds the shortest path in terms of number of edges on unweighted or uniform-cost graphs by exploring nodes layer by layer.
* **Input:** Graph adjacency list $G = (V, E)$, start node $S$, goal node $G$.
* **Output:** Explored nodes list, optimal path $[S, \dots, G]$, and total path cost.
* **Working:** Maintains a FIFO (First-In, First-Out) queue. Pop node from queue front, examine if goal; if not, add all unvisited neighbors to queue.
* **Pseudocode:**
  ```text
  function BFS(graph, start, goal):
      queue = FIFOQueue([ [start] ])
      visited = {start}
      while queue is not empty:
          path = queue.pop()
          node = path.last()
          if node == goal: return path
          for neighbor in graph.neighbors(node):
              if neighbor not in visited:
                  visited.add(neighbor)
                  queue.push(path + [neighbor])
      return failure
  ```
* **Time Complexity:** $O(b^d)$ where $b$ is branching factor and $d$ is goal depth.
* **Space Complexity:** $O(b^d)$ (stores all frontier nodes in memory).
* **Completeness:** Yes (if $b$ is finite).
* **Optimality:** Yes (if step costs are uniform/equal).
* **Advantages:** Guaranteed to find the shallowest goal.
* **Limitations:** Exponential memory growth makes it impractical for large search depths.
* **Applications:** Shortest path routing, social network connection degrees, web crawlers.

---

### 2. Depth-First Search (DFS)
* **File:** `algorithms/dfs.py`
* **Purpose:** Explores as deep as possible along each branch before backtracking.
* **Input:** Graph adjacency list, start node $S$, goal node $G$.
* **Output:** Explored order, path to goal.
* **Working:** Maintains a LIFO (Last-In, First-Out) stack. Expands the most recently discovered neighbor.
* **Pseudocode:**
  ```text
  function DFS(graph, start, goal):
      stack = LIFOStack([ [start] ])
      visited = set()
      while stack is not empty:
          path = stack.pop()
          node = path.last()
          if node == goal: return path
          if node not in visited:
              visited.add(node)
              for neighbor in reversed(graph.neighbors(node)):
                  if neighbor not in visited:
                      stack.push(path + [neighbor])
      return failure
  ```
* **Time Complexity:** $O(b^m)$ where $m$ is maximum search depth.
* **Space Complexity:** $O(b \cdot m)$ (linear memory requirement).
* **Completeness:** No (can get trapped in infinite/cyclic paths unless visited set is maintained).
* **Optimality:** No (may return a long suboptimal path).
* **Advantages:** Extremely low memory consumption compared to BFS.
* **Limitations:** Non-optimal, susceptible to deep or dead-end branches.
* **Applications:** Maze generation, topological sorting, connected component analysis.

---

### 3. Uniform Cost Search (UCS)
* **File:** `algorithms/ucs.py`
* **Purpose:** Finds the optimal lowest-cost path in weighted graphs with non-negative edge weights.
* **Input:** Weighted graph $G=(V, E, W)$, start node $S$, goal node $G$.
* **Output:** Lowest cost path and exact total numerical cost.
* **Working:** Priority Queue ordered by cumulative path cost $g(n)$. Always expands node with lowest $g(n)$.
* **Pseudocode:**
  ```text
  function UCS(graph, start, goal):
      frontier = PriorityQueue(order_by=g_cost)
      frontier.push(node=start, cost=0, path=[start])
      explored = set()
      while frontier is not empty:
          (cost, node, path) = frontier.pop_min()
          if node == goal: return (path, cost)
          if node not in explored:
              explored.add(node)
              for (neighbor, weight) in graph.neighbors(node):
                  if neighbor not in explored:
                      frontier.push(cost + weight, neighbor, path + [neighbor])
      return failure
  ```
* **Time Complexity:** $O(b^{1 + \lfloor C^* / \epsilon \rfloor})$ where $C^*$ is optimal cost and $\epsilon$ is minimum edge cost.
* **Space Complexity:** $O(b^{1 + \lfloor C^* / \epsilon \rfloor})$.
* **Completeness:** Yes (if step cost $\ge \epsilon > 0$).
* **Optimality:** Yes (guaranteed lowest total cost).
* **Advantages:** Optimal for general non-negative edge costs.
* **Limitations:** Explores blindly in all directions without goal awareness (no heuristic guidance).
* **Applications:** Dijkstra algorithm, GPS road routing.

---

### 4. A* Search
* **File:** `algorithms/astar.py`
* **Purpose:** Finds the optimal path using both actual path cost $g(n)$ and estimated heuristic distance to goal $h(n)$.
* **Evaluation Function:** $f(n) = g(n) + h(n)$
* **Input:** Weighted graph, heuristic table $h(n)$, start $S$, goal $G$.
* **Output:** Optimal path, path cost, and evaluated $f(n)$ values.
* **Working:** Priority queue ordered by lowest $f(n)$. Expands the most promising node that balances distance traveled with estimated distance remaining.
* **Pseudocode:**
  ```text
  function ASTAR(graph, heuristics, start, goal):
      frontier = PriorityQueue(order_by=f_cost)
      frontier.push(f=h(start), g=0, node=start, path=[start])
      explored = {}
      while frontier is not empty:
          (f, g, node, path) = frontier.pop_min()
          if node == goal: return (path, g)
          if node in explored and explored[node] <= g: continue
          explored[node] = g
          for (neighbor, weight) in graph.neighbors(node):
              new_g = g + weight
              new_f = new_g + heuristics[neighbor]
              frontier.push(new_f, new_g, neighbor, path + [neighbor])
      return failure
  ```
* **Time Complexity:** $O(b^d)$ in worst case; sub-exponential with an accurate heuristic.
* **Space Complexity:** $O(b^d)$ (stores all generated nodes in memory).
* **Completeness:** Yes.
* **Optimality:** Yes (if $h(n)$ is **admissible** and **consistent**).
* **Advantages:** Highly efficient; combines Dijkstra optimality with greedy speed.
* **Limitations:** High memory requirements for open list.
* **Applications:** Video game pathfinding (NavMesh), robotic path planning, logistics routing.

---

### 5. Greedy Best-First Search
* **File:** `algorithms/greedy.py`
* **Purpose:** Rapidly searches toward the goal by expanding the node estimated to be closest to the goal.
* **Evaluation Function:** $f(n) = h(n)$
* **Input:** Graph, heuristic table $h(n)$, start $S$, goal $G$.
* **Output:** Explored sequence, discovered path.
* **Time Complexity:** $O(b^m)$.
* **Space Complexity:** $O(b^m)$.
* **Completeness:** No (can get stuck in loops).
* **Optimality:** No.
* **Advantages:** Very fast when heuristic is accurate.
* **Limitations:** Easily misled by false local heuristic valleys.

---

### 6. Hill Climbing Optimization
* **File:** `algorithms/hill_climbing.py`
* **Purpose:** Local search algorithm that continuously moves in the direction of increasing value (steepest ascent).
* **Objective Function:** $f(x) = -(x-4)^2 + 25 + 3\sin(2x)$.
* **Input:** Starting coordinate $x_0$, step size $\Delta x$, max iterations.
* **Output:** Converged optimal $x^*$, maximum score $f(x^*)$, step trace.
* **Working:** Evaluates left neighbor $x - \Delta x$ and right neighbor $x + \Delta x$. If the best neighbor improves $f(x)$, moves to it; otherwise terminates at peak.
* **Pseudocode:**
  ```text
  function HillClimbing(f, start_x, step_size, max_iter):
      current_x = start_x
      current_score = f(current_x)
      for i in 1 to max_iter:
          neighbors = [current_x - step_size, current_x + step_size]
          best_neighbor = argmax_{x}(f(x) for x in neighbors)
          if f(best_neighbor) > current_score:
              current_x = best_neighbor
              current_score = f(best_neighbor)
          else:
              break # Peak reached
      return (current_x, current_score)
  ```
* **Failure Modes:** Local maxima, plateaus, ridges.
* **Applications:** Hyperparameter tuning, structural design optimization.

---

### 7. Genetic Algorithm
* **File:** `algorithms/genetic.py`
* **Purpose:** Global heuristic search inspired by natural biological evolution.
* **Chromosome:** 5-bit binary string representing integers $[0, 31]$.
* **Fitness Function:** $\text{Fitness}(x) = x^2$.
* **Operators:**
  1. **Selection:** Fitness-proportionate Roulette Wheel selection.
  2. **Crossover:** Single-point crossover recombining parent bitstrings.
  3. **Mutation:** Bit-flip mutation with rate $p_m = 0.05$.
* **Pseudocode:**
  ```text
  function GeneticAlgorithm(pop_size, generations, mutation_rate):
      population = RandomBinaryChromosomes(pop_size)
      for gen in 1 to generations:
          fitnesses = [Fitness(ind) for ind in population]
          new_population = []
          for i in 1 to pop_size / 2:
              parent1 = RouletteSelect(population, fitnesses)
              parent2 = RouletteSelect(population, fitnesses)
              child1, child2 = Crossover(parent1, parent2)
              new_population.append(Mutate(child1, mutation_rate))
              new_population.append(Mutate(child2, mutation_rate))
          population = new_population
      return BestIndividual(population)
  ```
* **Applications:** Traveling Salesperson Problem (TSP), scheduling, VLSI circuit layout.

---

### 8. Minimax Algorithm
* **File:** `algorithms/minimax.py`
* **Purpose:** Determines the optimal move for a player in a two-player zero-sum game assuming an optimal opponent.
* **Terminal Payoffs:** $+10 - \text{depth}$ (AI win), $\text{depth} - 10$ (Human win), $0$ (Draw).
* **Time Complexity:** $O(b^d)$.
* **Space Complexity:** $O(b \cdot d)$.
* **Completeness:** Yes (finite game tree).
* **Optimality:** Yes (against optimal play).

---

### 9. Alpha-Beta Pruning
* **File:** `algorithms/alpha_beta.py`
* **Purpose:** Optimizes Minimax by eliminating game tree branches that cannot influence the final decision.
* **Parameters:**
  * $\alpha$: Best score Maximizer is guaranteed so far.
  * $\beta$: Best score Minimizer is guaranteed so far.
* **Pruning Condition:** If $\beta \le \alpha$, prune remaining child nodes.
* **Performance Gain:** Reduces effective branching factor from $b$ to $\approx \sqrt{b}$, allowing search to twice the depth in the same compute time.

---

### 10. Water Jug Problem Solver
* **File:** `algorithms/water_jug.py`
* **Purpose:** Measures an exact target volume using two unmarked jugs of given capacities.
* **Solvability Condition:** Target $\le \max(A, B)$ and $\text{Target} \pmod{\gcd(A, B)} == 0$.
* **Operators (6 Transitions):**
  1. Fill Jug A: $(A, y)$
  2. Fill Jug B: $(x, B)$
  3. Empty Jug A: $(0, y)$
  4. Empty Jug B: $(x, 0)$
  5. Pour A into B: $(\max(0, x - (B - y)), \min(B, x + y))$
  6. Pour B into A: $(\min(A, x + y), \max(0, y - (A - x)))$
* **Algorithm:** BFS state-space search exploring reachable $(x, y)$ tuples.

---

### 11. Missionaries and Cannibals Problem Solver
* **File:** `algorithms/missionaries_cannibals.py`
* **Purpose:** Finds the optimal sequence of boat trips to move $N$ missionaries and $N$ cannibals across a river.
* **State Representation:** $(M_{left}, C_{left}, Boat_{pos})$.
* **Constraint:** On both banks, $M \ge C$ whenever $M > 0$.
* **Algorithm:** BFS exploring valid boat movements of 1 or 2 individuals.

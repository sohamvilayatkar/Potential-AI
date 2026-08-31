/**
 * POTENTIAL AI - AI Laboratory Interactive Engine
 * Handles Graph Search, Tic-Tac-Toe Game Playing, Water Jug, Missionaries & Cannibals,
 * Hill Climbing, and Genetic Algorithm simulations.
 */

function switchLabTab(evt, tabId) {
    document.querySelectorAll('.tabs-nav .tab-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.tab-pane').forEach(pane => pane.classList.remove('active'));
    evt.currentTarget.classList.add('active');
    document.getElementById(tabId).classList.add('active');
}

// ---------------- 1. Graph Search Simulator ----------------
async function runSearchAlgorithm() {
    const algo = document.getElementById('searchAlgoSelect').value;
    const start = document.getElementById('searchStartSelect').value;
    const goal = document.getElementById('searchGoalSelect').value;
    const resultBox = document.getElementById('searchResultBox');

    resultBox.innerHTML = `<span style="color: #38bdf8;">Running ${algo.toUpperCase()} from ${start} to ${goal}...</span>`;

    try {
        const res = await fetch('/api/ai-lab/search', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ algorithm: algo, start: start, goal: goal })
        });
        const data = await res.json();

        if (data.found) {
            resultBox.innerHTML = `
<strong style="color: #38bdf8;">=== ${data.algorithm} Execution Results ===</strong>
• <strong>Algorithm Type:</strong> ${data.type}
• <strong>Optimal / Goal Path:</strong> <span style="color: #4ade80; font-weight: bold;">${data.path.join(' ➔ ')}</span>
• <strong>Total Path Cost:</strong> ${data.path_cost}
• <strong>Explored Nodes Count:</strong> ${data.total_explored}
• <strong>Exploration Sequence:</strong> ${data.explored_order.join(', ')}
• <strong>Time Complexity:</strong> ${data.time_complexity}
• <strong>Space Complexity:</strong> ${data.space_complexity}
• <strong>Complete:</strong> ${data.complete}
• <strong>Optimal:</strong> ${data.optimal}
${data.evaluation_function ? `• <strong>Evaluation Function:</strong> ${data.evaluation_function}` : ''}
            `;
        } else {
            resultBox.innerHTML = `<span style="color: #f43f5e;">${data.message || data.error}</span>`;
        }
    } catch (e) {
        resultBox.innerHTML = `<span style="color: #f43f5e;">Error executing search: ${e}</span>`;
    }
}

// ---------------- 2. Tic-Tac-Toe Game Engine ----------------
let tttBoardState = ["", "", "", "", "", "", "", "", ""];
let tttGameOver = false;

function renderTTTBoard() {
    const cells = document.querySelectorAll('.ttt-cell');
    cells.forEach((cell, idx) => {
        cell.textContent = tttBoardState[idx];
        cell.className = 'ttt-cell';
        if (tttBoardState[idx] === 'X') cell.classList.add('x');
        if (tttBoardState[idx] === 'O') cell.classList.add('o');
    });
}

function resetTTTGame() {
    tttBoardState = ["", "", "", "", "", "", "", "", ""];
    tttGameOver = false;
    renderTTTBoard();
    document.getElementById('tttStatus').textContent = "Your turn! Click any cell to place X.";
    document.getElementById('tttStatus').style.color = "var(--text-accent)";
    document.getElementById('gameMetricsBox').innerHTML = "<div>Game reset. Make your move!</div>";
}

async function handleTTTCellClick(index) {
    if (tttGameOver || tttBoardState[index] !== "") return;

    // Human move (X)
    tttBoardState[index] = "X";
    renderTTTBoard();

    const winner = checkTTTWinner(tttBoardState);
    if (winner) {
        endTTTGame(winner);
        return;
    }

    document.getElementById('tttStatus').textContent = "AI is thinking (evaluating game tree)...";
    const algo = document.getElementById('gameAlgoSelect').value;

    try {
        const res = await fetch('/api/ai-lab/game', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ algorithm: algo, board: tttBoardState })
        });
        const data = await res.json();

        if (data.best_move !== undefined && data.best_move >= 0) {
            tttBoardState[data.best_move] = "O";
            renderTTTBoard();

            // Display metrics
            const metricsBox = document.getElementById('gameMetricsBox');
            metricsBox.innerHTML = `
<strong style="color: #38bdf8;">=== ${data.algorithm} Game Tree Evaluation ===</strong>
• <strong>AI Selected Move:</strong> Cell ${data.best_move}
• <strong>Game Tree Nodes Evaluated:</strong> <span style="color: #fbbf24; font-weight: bold;">${data.nodes_evaluated}</span>
${data.pruned_branches !== undefined ? `• <strong>Pruned Branches (Cutoffs):</strong> <span style="color: #34d399; font-weight: bold;">${data.pruned_branches}</span>` : ''}
• <strong>Best Minimax Score:</strong> ${data.best_score}
• <strong>Evaluated Candidate Moves:</strong>
${data.evaluated_moves.map(m => `   - Cell ${m.index}: Score ${m.score}`).join('\n')}
            `;

            const postWinner = checkTTTWinner(tttBoardState);
            if (postWinner) {
                endTTTGame(postWinner);
            } else {
                document.getElementById('tttStatus').textContent = "Your turn! Click any cell to place X.";
            }
        }
    } catch (e) {
        console.error("Game error:", e);
    }
}

function checkTTTWinner(board) {
    const winLines = [
        [0,1,2], [3,4,5], [6,7,8],
        [0,3,6], [1,4,7], [2,5,8],
        [0,4,8], [2,4,6]
    ];
    for (const [a, b, c] of winLines) {
        if (board[a] && board[a] === board[b] && board[a] === board[c]) {
            return board[a];
        }
    }
    if (board.every(cell => cell !== "")) return "Draw";
    return null;
}

function endTTTGame(winner) {
    tttGameOver = true;
    const status = document.getElementById('tttStatus');
    if (winner === "Draw") {
        status.textContent = "Game ended in a Draw! Well played.";
        status.style.color = "#fbbf24";
    } else if (winner === "X") {
        status.textContent = "Congratulations! You won!";
        status.style.color = "#34d399";
    } else {
        status.textContent = "AI ('O') won! Minimax played optimal defense.";
        status.style.color = "#f43f5e";
    }
}

// ---------------- 3. Classic AI Problems (Water Jug & Missionaries) ----------------
async function solveWaterJugProblem() {
    const capA = document.getElementById('jugACap').value;
    const capB = document.getElementById('jugBCap').value;
    const target = document.getElementById('jugTarget').value;
    const box = document.getElementById('waterJugResult');

    box.innerHTML = `<span style="color: #38bdf8;">Solving Water Jug (${capA}L, ${capB}L ➔ Target: ${target}L) via BFS...</span>`;

    try {
        const res = await fetch('/api/ai-lab/water-jug', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ jug_a: capA, jug_b: capB, target: target })
        });
        const data = await res.json();

        if (data.solvable) {
            let stepsHtml = data.solution_path.map((step, idx) => `
Step ${idx}: State (${step.state[0]}L, ${step.state[1]}L) ➔ ${step.action}
            `).join('');

            box.innerHTML = `
<strong style="color: #38bdf8;">=== Water Jug Problem Solution (BFS) ===</strong>
• <strong>Configuration:</strong> Jug A = ${data.jug_a_capacity}L, Jug B = ${data.jug_b_capacity}L, Target = ${data.target_amount}L
• <strong>Total Solution Steps:</strong> <span style="color: #34d399; font-weight: bold;">${data.solution_steps_count} steps</span>
• <strong>Total Explored States:</strong> ${data.explored_states_count}
• <strong>State Transitions:</strong>
${stepsHtml}
            `;
        } else {
            box.innerHTML = `<span style="color: #f43f5e;"><strong>Unsolvable:</strong> ${data.error}</span>`;
        }
    } catch (e) {
        box.innerHTML = `<span style="color: #f43f5e;">Error: ${e}</span>`;
    }
}

async function solveMissionariesCannibalsProblem() {
    const m = document.getElementById('mcMiss').value;
    const c = document.getElementById('mcCann').value;
    const b = document.getElementById('mcBoat').value;
    const box = document.getElementById('mcResult');

    box.innerHTML = `<span style="color: #38bdf8;">Finding safe river crossing sequence...</span>`;

    try {
        const res = await fetch('/api/ai-lab/missionaries-cannibals', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ missionaries: m, cannibals: c, boat_capacity: b })
        });
        const data = await res.json();

        if (data.solvable) {
            let stepsHtml = data.solution_path.map((step, idx) => `
Step ${idx}: [Left: ${step.left_bank}] [Boat: ${step.boat_location}] [Right: ${step.right_bank}]
        ➔ ${step.action}
            `).join('');

            box.innerHTML = `
<strong style="color: #38bdf8;">=== Missionaries & Cannibals River Crossing (BFS) ===</strong>
• <strong>Initial:</strong> ${data.total_missionaries} Missionaries, ${data.total_cannibals} Cannibals, Boat Capacity = ${data.boat_capacity}
• <strong>Total Safe Crossings:</strong> <span style="color: #34d399; font-weight: bold;">${data.total_steps} river trips</span>
• <strong>Explored States:</strong> ${data.explored_states_count}
• <strong>Step-by-Step Crossing Plan:</strong>
${stepsHtml}
            `;
        } else {
            box.innerHTML = `<span style="color: #f43f5e;"><strong>Unsolvable:</strong> ${data.error}</span>`;
        }
    } catch (e) {
        box.innerHTML = `<span style="color: #f43f5e;">Error: ${e}</span>`;
    }
}

// ---------------- 4. Optimization (Hill Climbing & Genetic Algorithm) ----------------
async function runHillClimbing() {
    const startX = document.getElementById('hcStartX').value;
    const step = document.getElementById('hcStep').value;
    const box = document.getElementById('hcResultBox');

    box.innerHTML = `<span style="color: #38bdf8;">Climbing hill from start x = ${startX}...</span>`;

    try {
        const res = await fetch('/api/ai-lab/optimize', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ algorithm: 'hill_climbing', start_x: startX, step_size: step })
        });
        const data = await res.json();

        let traceHtml = data.history.map(h => `
Iter ${h.iteration}: x = ${h.x.toFixed(4)}, Score f(x) = ${h.score.toFixed(4)} ➔ ${h.action}
        `).join('');

        box.innerHTML = `
<strong style="color: #38bdf8;">=== Hill Climbing (Steepest Ascent) Optimization ===</strong>
• <strong>Objective:</strong> ${data.objective_function}
• <strong>Initial X:</strong> ${data.start_x} | <strong>Step Size (Δx):</strong> ${data.step_size}
• <strong>Converged Maximum X:</strong> <span style="color: #34d399; font-weight: bold;">x = ${data.final_x}</span>
• <strong>Peak Objective Value:</strong> <span style="color: #38bdf8; font-weight: bold;">f(x) = ${data.maximum_score}</span>
• <strong>Status:</strong> ${data.status}
• <strong>Iteration Trace:</strong>
${traceHtml}
        `;
    } catch (e) {
        box.innerHTML = `<span style="color: #f43f5e;">Error: ${e}</span>`;
    }
}

async function runGeneticAlgorithm() {
    const pop = document.getElementById('gaPop').value;
    const gen = document.getElementById('gaGen').value;
    const box = document.getElementById('gaResultBox');

    box.innerHTML = `<span style="color: #38bdf8;">Simulating Genetic Algorithm evolution across ${gen} generations...</span>`;

    try {
        const res = await fetch('/api/ai-lab/optimize', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ algorithm: 'genetic', population_size: pop, generations: gen })
        });
        const data = await res.json();

        let genHtml = data.generation_history.map(g => `
Gen ${g.generation}: Best Chromosome [${g.best_chromosome}] ➔ Decoded x = ${g.best_x}, Max Fitness = ${g.max_fitness}, Avg Fitness = ${g.avg_fitness}
        `).join('');

        box.innerHTML = `
<strong style="color: #38bdf8;">=== Genetic Algorithm (GA) Evolutionary Optimization ===</strong>
• <strong>Objective:</strong> ${data.objective_function}
• <strong>Population:</strong> ${data.population_size} | <strong>Generations:</strong> ${data.generations}
• <strong>Optimal Solution:</strong> <span style="color: #34d399; font-weight: bold;">x = ${data.best_solution_x}</span> (Binary: ${data.best_chromosome})
• <strong>Maximum Fitness Reached:</strong> <span style="color: #38bdf8; font-weight: bold;">${data.optimal_fitness}</span>
• <strong>Generational Progression:</strong>
${genHtml}
        `;
    } catch (e) {
        box.innerHTML = `<span style="color: #f43f5e;">Error: ${e}</span>`;
    }
}

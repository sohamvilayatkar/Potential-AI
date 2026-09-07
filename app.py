"""
Potential AI - Main Flask Application.
An Intelligent Web-Based College Assistant Chatbot for:
P. R. Pote Patil College of Engineering & Management, Amravati (PRPCEM).
"""

import os
import sys
import json
from flask import Flask, render_template, request, jsonify

# Ensure root directory is in sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from config import Config
from database import (
    init_db, log_query, get_analytics_summary,
    get_intent_distribution, generate_analytics_chart_base64
)
from ai.response import get_response_generator
from ai.knowledge_graph import get_knowledge_graph
from ai.chatbot import get_chatbot_service
from platforms.telegram_service import handle_telegram_update
from platforms.telegram_bot import start_telegram_bot_background
from algorithms import (
    breadth_first_search, depth_first_search, uniform_cost_search,
    astar_search, greedy_best_first_search, hill_climbing_optimization,
    genetic_algorithm_optimize, minimax_tic_tac_toe, alphabeta_tic_tac_toe,
    solve_water_jug, solve_missionaries_cannibals
)

app = Flask(__name__)
app.config.from_object(Config)

# Initialize Database and AI components once at startup
init_db()
response_generator = get_response_generator()
knowledge_graph = get_knowledge_graph()
chatbot_service = get_chatbot_service()

# Automatically launch Telegram Bot background listener
if os.environ.get("WERKZEUG_RUN_MAIN") in ["true", None] or not Config.DEBUG:
    start_telegram_bot_background()

@app.context_processor
def inject_global_template_context():
    return {
        "telegram_bot_username": Config.TELEGRAM_BOT_USERNAME,
        "college_name": Config.COLLEGE_NAME,
        "bot_name": Config.BOT_NAME
    }

# ==========================================
#               WEB ROUTES
# ==========================================

@app.route("/")
def index():
    """Main Chatbot Page."""
    return render_template("index.html", title="Potential AI - Intelligent College Assistant")

@app.route("/college")
def college_explorer():
    """College Information Explorer Page."""
    data = response_generator.college_data
    return render_template("college.html", title="PRPCEM College Explorer", data=data)

@app.route("/ai-lab")
def ai_lab():
    """Interactive AI Algorithms Laboratory."""
    return render_template("ai_lab.html", title="Potential AI - AI Algorithms Lab")

@app.route("/dashboard")
def dashboard():
    """Analytics & Performance Dashboard."""
    summary = get_analytics_summary()
    chart_base64 = generate_analytics_chart_base64()
    sources_count = len(response_generator.college_data.get("sources", [])) or 8
    last_update = response_generator.college_data.get("metadata", {}).get("last_updated", "31 August 2026")
    return render_template(
        "dashboard.html",
        title="Potential AI - Analytics Dashboard",
        summary=summary,
        chart_base64=chart_base64,
        sources_count=sources_count,
        last_update=last_update
    )

@app.route("/about")
def about():
    """Project Overview, Architecture & Syllabus Concepts."""
    return render_template("about.html", title="About Potential AI - AI mini-project")

@app.route("/health")
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "ok",
        "service": "Potential AI",
        "college": "P. R. Pote Patil College of Engineering & Management, Amravati",
        "version": "1.0"
    }), 200

# ==========================================
#               API ROUTES
# ==========================================

@app.route("/api/chat", methods=["POST"])
def api_chat():
    """
    Primary Chatbot API Endpoint.
    Expects JSON: {"message": "..."}
    Returns structured JSON with response, intent, confidence, sources, and AI reasoning details.
    """
    try:
        data = request.get_json(silent=True)
        if not data or "message" not in data:
            return jsonify({
                "response": "Please provide a valid JSON request containing a 'message' field.",
                "intent": "malformed_request",
                "confidence": 0.0,
                "sources": []
            }), 400

        user_message = str(data.get("message", "")).strip()

        # Generate response via AI pipeline
        result = chatbot_service.process_message(user_message)

        # Log query to database for analytics
        status = "fallback" if result.get("intent") == "fallback" else "success"
        log_query(user_message, result.get("intent", "unknown"), result.get("confidence", 0.0), status)

        return jsonify(result), 200

    except Exception as e:
        print(f"[API Error] /api/chat exception: {e}")
        return jsonify({
            "response": "I encountered an internal processing issue. Please ask your question again.",
            "intent": "error",
            "confidence": 0.0,
            "sources": []
        }), 500

@app.route("/api/ai-lab/search", methods=["POST"])
def api_search_algorithm():
    """Runs Uninformed / Informed Search algorithms (BFS, DFS, UCS, A*, Greedy)."""
    try:
        data = request.get_json(silent=True) or {}
        algo = data.get("algorithm", "bfs").lower()
        start = data.get("start", "A")
        goal = data.get("goal", "Goal")

        if algo == "bfs":
            result = breadth_first_search(start, goal)
        elif algo == "dfs":
            result = depth_first_search(start, goal)
        elif algo == "ucs":
            result = uniform_cost_search(start, goal)
        elif algo == "astar":
            result = astar_search(start, goal)
        elif algo == "greedy":
            result = greedy_best_first_search(start, goal)
        else:
            return jsonify({"error": f"Unknown search algorithm: {algo}"}), 400

        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/ai-lab/optimize", methods=["POST"])
def api_optimize():
    """Runs Optimization algorithms (Hill Climbing, Genetic Algorithm)."""
    try:
        data = request.get_json(silent=True) or {}
        algo = data.get("algorithm", "hill_climbing").lower()

        if algo == "hill_climbing":
            start_x = float(data.get("start_x", 0.0))
            step_size = float(data.get("step_size", 0.25))
            result = hill_climbing_optimization(start_x=start_x, step_size=step_size)
        elif algo == "genetic":
            pop_size = int(data.get("population_size", 10))
            generations = int(data.get("generations", 15))
            result = genetic_algorithm_optimize(population_size=pop_size, generations=generations)
        else:
            return jsonify({"error": f"Unknown optimization algorithm: {algo}"}), 400

        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/ai-lab/game", methods=["POST"])
def api_game():
    """Runs Game Playing algorithms (Minimax vs Alpha-Beta Pruning for Tic-Tac-Toe)."""
    try:
        data = request.get_json(silent=True) or {}
        algo = data.get("algorithm", "alphabeta").lower()
        board = data.get("board", [""] * 9)

        if len(board) != 9:
            return jsonify({"error": "Board must contain exactly 9 cells."}), 400

        if algo == "minimax":
            result = minimax_tic_tac_toe(board)
        else:
            result = alphabeta_tic_tac_toe(board)

        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/ai-lab/water-jug", methods=["POST"])
def api_water_jug():
    """Solves the Water Jug Problem."""
    try:
        data = request.get_json(silent=True) or {}
        cap_a = int(data.get("jug_a", 4))
        cap_b = int(data.get("jug_b", 3))
        target = int(data.get("target", 2))

        result = solve_water_jug(cap_a, cap_b, target)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/ai-lab/missionaries-cannibals", methods=["POST"])
def api_missionaries_cannibals():
    """Solves the Missionaries and Cannibals river crossing."""
    try:
        data = request.get_json(silent=True) or {}
        m = int(data.get("missionaries", 3))
        c = int(data.get("cannibals", 3))
        b = int(data.get("boat_capacity", 2))

        result = solve_missionaries_cannibals(m, c, b)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/dashboard/data", methods=["GET"])
def api_dashboard_data():
    """Returns updated analytics summary and Matplotlib chart."""
    try:
        summary = get_analytics_summary()
        chart_base64 = generate_analytics_chart_base64()
        distribution = get_intent_distribution()
        return jsonify({
            "summary": summary,
            "chart_base64": chart_base64,
            "distribution": distribution
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==========================================
#          TELEGRAM BOT INTEGRATION
# ==========================================

@app.route("/api/telegram/webhook", methods=["POST"])
def telegram_webhook():
    """
    Telegram Bot Webhook endpoint.
    Receives JSON updates from Telegram and replies using Potential AI inference engine.
    """
    try:
        update = request.get_json(force=True, silent=True)
        if not update:
            return jsonify({"ok": False, "error": "Invalid JSON payload"}), 400

        result = handle_telegram_update(update)
        return jsonify(result), 200
    except Exception as e:
        print(f"[Telegram Webhook Error] {e}")
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route("/api/telegram/status", methods=["GET"])
def telegram_status():
    """
    Returns Telegram bot configuration and status.
    """
    return jsonify({
        "configured": bool(Config.TELEGRAM_BOT_TOKEN),
        "bot_username": Config.TELEGRAM_BOT_USERNAME,
        "bot_link": f"https://t.me/{Config.TELEGRAM_BOT_USERNAME}",
        "webhook_url": f"{request.host_url.rstrip('/')}/api/telegram/webhook"
    }), 200

# ==========================================
#               ERROR HANDLERS
# ==========================================

@app.errorhandler(404)
def page_not_found(e):
    return render_template("base.html", not_found=True), 404

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify({"error": "An internal server error occurred."}), 500

if __name__ == "__main__":
    host = Config.HOST
    port = Config.PORT
    debug = Config.DEBUG
    print(f"Starting Potential AI Flask server on http://{host}:{port} ...")
    app.run(host=host, port=port, debug=debug)

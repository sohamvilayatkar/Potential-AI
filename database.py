"""
Database & Analytics Module for Potential AI.
Provides SQLite storage for conversational queries, parameterized execution,
analytics aggregation with Pandas, and Matplotlib chart generation for the Dashboard.
"""

import os
import sqlite3
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for web servers
import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime
from typing import Dict, List, Any, Optional

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "potential_ai.db")

def get_db_connection():
    """Establish connection to SQLite database with row factory."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Create database tables if they do not exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS queries_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            user_message TEXT NOT NULL,
            intent TEXT NOT NULL,
            confidence REAL NOT NULL,
            response_status TEXT NOT NULL
        )
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_intent ON queries_log(intent)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON queries_log(timestamp)")
    conn.commit()
    conn.close()

def log_query(user_message: str, intent: str, confidence: float, response_status: str = "success") -> bool:
    """Safely log user query with parameterized SQL query."""
    if not user_message:
        return False
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO queries_log (user_message, intent, confidence, response_status)
            VALUES (?, ?, ?, ?)
        """, (user_message[:500], intent, float(confidence), response_status))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"[Database Error] Failed to log query: {e}")
        return False

def get_analytics_summary() -> Dict[str, Any]:
    """Calculate aggregated analytics metrics using Pandas and SQL."""
    conn = get_db_connection()
    try:
        df = pd.read_sql_query("SELECT * FROM queries_log", conn)
    except Exception:
        df = pd.DataFrame()
    finally:
        conn.close()

    if df.empty:
        return {
            "total_queries": 0,
            "successful_queries": 0,
            "fallback_queries": 0,
            "success_rate": 100.0,
            "average_confidence": 0.0,
            "top_intent": "None",
            "recent_queries": []
        }

    total_queries = len(df)
    successful = len(df[df['response_status'] == 'success'])
    fallbacks = len(df[df['response_status'] == 'fallback'])
    avg_conf = float(df['confidence'].mean()) * 100.0 if not df['confidence'].empty else 0.0
    
    # Most popular intent
    top_intent = df['intent'].mode()[0] if not df['intent'].empty else "None"
    success_rate = (successful / total_queries * 100.0) if total_queries > 0 else 100.0

    recent_queries = df.tail(10).to_dict(orient="records")
    recent_queries.reverse()

    return {
        "total_queries": total_queries,
        "successful_queries": successful,
        "fallback_queries": fallbacks,
        "success_rate": round(success_rate, 1),
        "average_confidence": round(avg_conf, 1),
        "top_intent": top_intent,
        "recent_queries": recent_queries
    }

def get_intent_distribution() -> List[Dict[str, Any]]:
    """Return count and percentage per intent."""
    conn = get_db_connection()
    try:
        df = pd.read_sql_query("SELECT intent, COUNT(*) as count FROM queries_log GROUP BY intent ORDER BY count DESC", conn)
        return df.to_dict(orient="records")
    except Exception:
        return []
    finally:
        conn.close()

def generate_analytics_chart_base64() -> str:
    """Generate Matplotlib bar chart for intent distribution and return base64 encoded PNG."""
    conn = get_db_connection()
    try:
        df = pd.read_sql_query("SELECT intent, COUNT(*) as count FROM queries_log GROUP BY intent ORDER BY count DESC LIMIT 8", conn)
    except Exception:
        df = pd.DataFrame()
    finally:
        conn.close()

    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    fig, ax = plt.subplots(figsize=(8, 4), dpi=100)
    fig.patch.set_facecolor('#0f172a')
    ax.set_facecolor('#1e293b')

    if not df.empty:
        colors = ['#38bdf8', '#818cf8', '#c084fc', '#34d399', '#f472b6', '#fbbf24', '#fb7185', '#a78bfa']
        bars = ax.bar(df['intent'], df['count'], color=colors[:len(df)], edgecolor='#0284c7', width=0.6)
        ax.set_title("Most Inquired College Topics (Intent Distribution)", fontsize=13, fontweight='bold', color='#f8fafc', pad=15)
        ax.set_xlabel("Query Topic / Intent", fontsize=10, color='#94a3b8', labelpad=8)
        ax.set_ylabel("Total Inquiries", fontsize=10, color='#94a3b8', labelpad=8)
        ax.tick_params(colors='#cbd5e1', labelsize=9)
        plt.xticks(rotation=25, ha='right')

        # Add value labels on top of bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=9, fontweight='bold', color='#38bdf8')
    else:
        ax.text(0.5, 0.5, "No query data recorded yet", horizontalalignment='center', verticalalignment='center', color='#94a3b8', fontsize=12)
        ax.set_title("Query Analytics", color='#f8fafc')

    plt.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format='png', facecolor=fig.get_facecolor(), edgecolor='none')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close(fig)
    return img_base64

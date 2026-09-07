"""
Telegram Bot Service for Potential AI.
Handles Telegram webhook updates, response formatting, and outgoing messages
using official Telegram Bot HTTP API with zero extra dependencies.
"""

import json
import logging
import urllib.request
import urllib.parse
from typing import Dict, Any, Optional

from config import Config
from database import log_query
from ai.chatbot import get_chatbot_service

logger = logging.getLogger(__name__)

def send_telegram_message(chat_id: int, text: str, parse_mode: Optional[str] = "Markdown") -> bool:
    """
    Sends a message to a Telegram chat using Telegram Bot HTTP API.
    """
    token = Config.TELEGRAM_BOT_TOKEN
    if not token:
        logger.warning("[Telegram] TELEGRAM_BOT_TOKEN is not configured.")
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "disable_web_page_preview": False
    }
    if parse_mode:
        payload["parse_mode"] = parse_mode

    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.status == 200
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="ignore")
        logger.error(f"[Telegram HTTP Error] {e.code}: {err_body}")
        # If markdown formatting failed, fallback to plain text
        if parse_mode:
            return send_telegram_message(chat_id, text, parse_mode=None)
        return False
    except Exception as e:
        logger.error(f"[Telegram Error] Failed to send message: {e}")
        return False

def format_telegram_reply(result: Dict[str, Any]) -> str:
    """
    Converts Potential AI structured response into Telegram-friendly text.
    """
    response_text = result.get("response", "").strip()
    sources = result.get("sources", [])
    academic_year = result.get("academic_year")

    lines = [response_text]

    # Append official source links
    if sources:
        lines.append("\n\n🔗 *Official Source Attribution:*")
        for s in sources:
            title = s.get("title", "Official Portal")
            url = s.get("url", "")
            if url:
                lines.append(f"• [{title}]({url})")

    if academic_year:
        lines.append(f"\n📅 _Academic Session: {academic_year}_")

    return "\n".join(lines)

def handle_telegram_update(update: Dict[str, Any]) -> Dict[str, Any]:
    """
    Processes an incoming update from Telegram Webhook or Polling.
    """
    message = update.get("message") or update.get("edited_message")
    if not message:
        return {"ok": True, "action": "ignored_non_message"}

    chat = message.get("chat", {})
    chat_id = chat.get("id")
    user_text = str(message.get("text", "")).strip()

    if not chat_id or not user_text:
        return {"ok": True, "action": "empty_text"}

    first_name = message.get("from", {}).get("first_name", "Student")

    # Command: /start or /help
    if user_text.lower() in ["/start", "/help", "start", "help"]:
        welcome_reply = (
            f"👋 *Hello {first_name}! Welcome to Potential AI.*\n\n"
            f"I am the intelligent college assistant for *P. R. Pote Patil College of Engineering & Management (PRPCEM), Amravati*.\n\n"
            f"💬 *You can ask me anything about:*\n"
            f"• *Degree Programs:* B.Tech, M.Tech, MBA, MCA\n"
            f"• *Departments & HODs:* CSE, AIML, AI&DS, EXTC, EE, ME, CE\n"
            f"• *Admissions:* CAP rounds, DTE Code 1107, eligibility\n"
            f"• *Leadership:* Principal, Chairman, Dean Academics\n"
            f"• *Fees & Scholarships:* FRA structure, MahaDBT, EBC, TFWS\n"
            f"• *Campus Facilities:* Central Library, Hostels, Sports, Labs\n\n"
            f"Try asking:\n"
            f"👉 _Who is the principal?_\n"
            f"👉 _What courses are offered?_\n"
            f"👉 _Who is the HOD of Computer Engineering?_\n"
            f"👉 _What documents are needed for admission?_"
        )
        send_telegram_message(chat_id, welcome_reply)
        log_query(user_text, "greeting", 1.0, "success")
        return {"ok": True, "action": "sent_welcome"}

    # Process via Potential AI Chatbot Engine
    chatbot = get_chatbot_service()
    result = chatbot.process_message(user_text)

    # Format reply
    reply_text = format_telegram_reply(result)
    send_telegram_message(chat_id, reply_text)

    # Log to SQLite telemetry database
    status = "fallback" if result.get("intent") == "fallback" else "success"
    log_query(user_text, result.get("intent", "telegram"), result.get("confidence", 0.0), status)

    return {
        "ok": True,
        "action": "sent_reply",
        "intent": result.get("intent"),
        "confidence": result.get("confidence")
    }

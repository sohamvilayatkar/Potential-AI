"""
Standalone & Background Telegram Bot Runner for Potential AI.
Uses long-polling to receive and respond to Telegram messages concurrently with Flask.

Usage:
    # 1. Automatic with Flask (python app.py)
    # 2. Standalone:
    set TELEGRAM_BOT_TOKEN=your_token_here
    python platforms/telegram_bot.py
"""

import os
import sys
import time
import json
import logging
import threading
import urllib.request
import urllib.parse
from typing import Optional

# Ensure project root is on sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from config import Config
from platforms.telegram_service import handle_telegram_update

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("TelegramBot")

_bot_thread: Optional[threading.Thread] = None
_stop_event = threading.Event()

def _polling_worker():
    """Worker loop that polls Telegram getUpdates until stop event is set."""
    token = Config.TELEGRAM_BOT_TOKEN
    if not token:
        logger.info("[Telegram Bot] No TELEGRAM_BOT_TOKEN set. Background listener idle.")
        return

    logger.info(f"🤖 [Telegram Bot] Background listener active for @{Config.TELEGRAM_BOT_USERNAME}")
    offset = 0

    while not _stop_event.is_set():
        try:
            url = f"https://api.telegram.org/bot{token}/getUpdates?offset={offset}&timeout=15"
            req = urllib.request.Request(url, headers={"User-Agent": "PotentialAI-Telegram/1.0"})

            with urllib.request.urlopen(req, timeout=25) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode("utf-8"))
                    updates = data.get("result", [])

                    for update in updates:
                        if _stop_event.is_set():
                            break
                        update_id = update.get("update_id", 0)
                        offset = max(offset, update_id + 1)

                        # Process message through AI engine
                        handle_telegram_update(update)

        except urllib.error.HTTPError as e:
            if e.code == 409:
                logger.warning("[Telegram Bot] Conflict (409): Another instance or webhook is active. Waiting 5s...")
                _stop_event.wait(5)
            elif e.code == 401 or e.code == 404:
                logger.error(f"[Telegram Bot] Invalid Bot Token ({e.code}). Please verify TELEGRAM_BOT_TOKEN.")
                _stop_event.wait(5)
            else:
                logger.error(f"[Telegram Bot] HTTP Error {e.code}: {e.reason}")
                _stop_event.wait(3)
        except urllib.error.URLError as e:
            logger.debug(f"[Telegram Bot] Connection error: {e.reason}. Retrying in 3s...")
            _stop_event.wait(3)
        except Exception as e:
            logger.error(f"[Telegram Bot] Unexpected error in polling loop: {e}")
            _stop_event.wait(2)

def start_telegram_bot_background() -> Optional[threading.Thread]:
    """
    Launches the Telegram polling loop in a background daemon thread.
    Automatically called when Flask app starts.
    """
    global _bot_thread
    token = Config.TELEGRAM_BOT_TOKEN
    if not token:
        print("[Telegram Bot] Notice: TELEGRAM_BOT_TOKEN is not set. The bot web interface is live, but Telegram polling is disabled until TELEGRAM_BOT_TOKEN is set in environment.")
        return None

    if _bot_thread and _bot_thread.is_alive():
        return _bot_thread

    _stop_event.clear()
    _bot_thread = threading.Thread(target=_polling_worker, name="TelegramBotWorker", daemon=True)
    _bot_thread.start()
    return _bot_thread

def stop_telegram_bot_background():
    """Signals the background Telegram bot thread to stop."""
    global _bot_thread
    _stop_event.set()
    if _bot_thread and _bot_thread.is_alive():
        _bot_thread.join(timeout=2)
        _bot_thread = None

def run_polling():
    """CLI runner function for standalone execution."""
    token = Config.TELEGRAM_BOT_TOKEN
    if not token:
        logger.error(
            "TELEGRAM_BOT_TOKEN is not set!\n"
            "To run the Telegram bot, obtain a token from @BotFather on Telegram, then set:\n"
            "   set TELEGRAM_BOT_TOKEN=your_token_here\n"
            "and run this script again."
        )
        sys.exit(1)

    print(f"Starting Potential AI Telegram Bot (@{Config.TELEGRAM_BOT_USERNAME}) in standalone mode. Press Ctrl+C to exit.")
    _stop_event.clear()
    try:
        _polling_worker()
    except KeyboardInterrupt:
        logger.info("Stopping Telegram Bot...")
        stop_telegram_bot_background()

if __name__ == "__main__":
    run_polling()

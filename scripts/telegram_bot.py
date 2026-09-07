"""
Backward-compatibility wrapper for Potential AI Telegram Bot.
The Telegram integration files have been shifted to the 'platforms/' directory.

Usage:
    set TELEGRAM_BOT_TOKEN=your_token_here
    python -m platforms.telegram_bot
    or
    python scripts/telegram_bot.py
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from platforms.telegram_bot import run_polling

if __name__ == "__main__":
    run_polling()

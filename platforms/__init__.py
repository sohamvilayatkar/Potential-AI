"""
Platforms package for Potential AI.
Houses multi-platform integrations (e.g. Telegram, external bots, messaging clients).
"""

from .telegram_service import (
    send_telegram_message,
    format_telegram_reply,
    handle_telegram_update
)
from .telegram_bot import (
    start_telegram_bot_background,
    stop_telegram_bot_background,
    run_polling
)

__all__ = [
    "send_telegram_message",
    "format_telegram_reply",
    "handle_telegram_update",
    "start_telegram_bot_background",
    "stop_telegram_bot_background",
    "run_polling"
]

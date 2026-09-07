"""
Unit and Integration Tests for Telegram Bot Integration.
"""

import pytest
from app import app
from platforms.telegram_service import format_telegram_reply
from platforms import send_telegram_message, handle_telegram_update

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_telegram_status_api(client):
    res = client.get('/api/telegram/status')
    assert res.status_code == 200
    data = res.get_json()
    assert 'bot_username' in data
    assert 'bot_link' in data
    assert 'https://t.me/' in data['bot_link']

def test_telegram_webhook_invalid_payload(client):
    res = client.post('/api/telegram/webhook', data="not json", content_type="text/plain")
    assert res.status_code == 400

def test_telegram_webhook_start_command(client):
    payload = {
        "update_id": 10001,
        "message": {
            "message_id": 1,
            "chat": {"id": 987654321, "type": "private"},
            "from": {"first_name": "Soham"},
            "text": "/start"
        }
    }
    res = client.post('/api/telegram/webhook', json=payload)
    assert res.status_code == 200
    data = res.get_json()
    assert data["ok"] is True
    assert data["action"] == "sent_welcome"

def test_telegram_webhook_college_query(client):
    payload = {
        "update_id": 10002,
        "message": {
            "message_id": 2,
            "chat": {"id": 987654321, "type": "private"},
            "from": {"first_name": "Soham"},
            "text": "Who is the principal?"
        }
    }
    res = client.post('/api/telegram/webhook', json=payload)
    assert res.status_code == 200
    data = res.get_json()
    assert data["ok"] is True
    assert data["action"] == "sent_reply"
    assert data["intent"] == "principal"

def test_telegram_format_reply():
    mock_result = {
        "response": "The Principal is Dr. P. M. Jawandhiya.",
        "sources": [{"title": "PRPCEM Portal", "url": "https://prpotepatilengg.ac.in/"}],
        "academic_year": "2025-26"
    }
    text = format_telegram_reply(mock_result)
    assert "Dr. P. M. Jawandhiya" in text
    assert "Official Source Attribution" in text
    assert "https://prpotepatilengg.ac.in/" in text
    assert "2025-26" in text

def test_flying_telegram_button_rendered(client):
    res = client.get('/')
    assert res.status_code == 200
    html = res.get_data(as_text=True)
    assert 'flying-telegram-container' in html
    assert 'flyingTelegramBtn' in html
    assert 'https://t.me/' in html

def test_telegram_background_lifecycle(monkeypatch):
    import time
    from platforms.telegram_bot import start_telegram_bot_background, stop_telegram_bot_background
    from config import Config

    # When token is empty, should return None safely
    monkeypatch.setattr(Config, "TELEGRAM_BOT_TOKEN", "")
    t = start_telegram_bot_background()
    assert t is None

    # Mock urllib.request.urlopen to return an empty updates list without external network call
    class MockResponse:
        status = 200
        def read(self):
            return b'{"ok": true, "result": []}'
        def __enter__(self):
            return self
        def __exit__(self, *args):
            pass

    monkeypatch.setattr("urllib.request.urlopen", lambda *args, **kwargs: MockResponse())
    monkeypatch.setattr(Config, "TELEGRAM_BOT_TOKEN", "mock_token_12345")

    t = start_telegram_bot_background()
    assert t is not None
    assert t.is_alive()
    time.sleep(0.1)
    stop_telegram_bot_background()
    assert not t.is_alive()

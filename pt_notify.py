import requests


def send_telegram_message(bot_token: str, chat_id: str, text: str, timeout: float = 4.0) -> bool:
    """Best-effort Telegram send that never raises to callers."""
    try:
        token = str(bot_token or "").strip()
        chat = str(chat_id or "").strip()
        body = str(text or "").strip()
        if not token or not chat or not body:
            return False

        url = f"https://api.telegram.org/bot{token}/sendMessage"
        resp = requests.post(
            url,
            json={
                "chat_id": chat,
                "text": body,
                "disable_web_page_preview": True,
            },
            timeout=float(timeout),
        )
        if resp.status_code != 200:
            return False
        data = resp.json()
        return bool(data.get("ok", False)) if isinstance(data, dict) else False
    except Exception:
        return False

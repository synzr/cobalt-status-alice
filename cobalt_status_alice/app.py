from flask import Flask
from .status import fetch_status

app = Flask(__name__)


@app.post("/cobalt_status_alice/")
def handle_skill() -> dict:
    status = fetch_status()

    pinned_issues = "Проблемы: " + ", ".join(status["pinned_issues"])
    text = "Кобальт в порядке!" if status["is_alright"] else f"У кобальта есть некоторые проблемы! {pinned_issues}"

    return {
        "response": {"text": text, "tts": text, "end_session": True},
        "version": "1.0"
    }

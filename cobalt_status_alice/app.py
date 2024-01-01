from flask import Flask

app = Flask(__name__)


@app.post("/cobalt_status_alice/")
def handle_skill() -> dict:
    return {
        "response": {
            "text": "Привет мир!",
            "tts": "Привет мир!",
            "end_session": True
        },
        "version": "1.0"
    }

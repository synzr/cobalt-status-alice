from datetime import datetime
import requests

COBALT_STATUS_URL = "https://status.cobalt.tools/index.json"

SIMPLYTRANSLATE_API_URL = "https://simplytranslate.org/api/translate"
SIMPLYTRANSLATE_BASE_REQUEST_DATA = {"engine": "reverso", "to": "ru"}


def _translate_string_to_russian(source_text: str, source_language: str) -> str:
    data = SIMPLYTRANSLATE_BASE_REQUEST_DATA
    data.update({"text": source_text, "from": source_language})

    with requests.post(SIMPLYTRANSLATE_API_URL, data=data) as simplytranslate_response:
        simplytranslate_response.raise_for_status()
        return simplytranslate_response.json().get("translated_text", source_text)


def _convert_pinned_issue_to_string(pinned_issue: dict, source_language: str) -> str:
    translated_title = _translate_string_to_russian(pinned_issue["title"], source_language).capitalize()

    created_at = pinned_issue["createdAt"].split("+")[0].strip()
    created_at = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
    created_at = created_at.strftime("%d.%m.%Y %H:%M")

    return f'"{translated_title}" с {created_at}'



def fetch_status() -> dict:
    with requests.get(COBALT_STATUS_URL) as status_response:
        status_response.raise_for_status()
        status_data = status_response.json()

        return {
            "is_alright": status_data["summaryStatus"] == "ok",
            "pinned_issues": [
                _convert_pinned_issue_to_string(pinned_issue, status_data["languageCode"])
                for pinned_issue in status_data["pinnedIssues"]
            ]
        }

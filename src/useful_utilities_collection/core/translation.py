import json
from pathlib import Path
from typing import Any

# Resolve path to the languages folder
LANGUAGES_DIR = Path(__file__).resolve().parent.parent / "languages"

TRANSLATIONS: dict[str, Any] = {}
_current_language = "en"


def load_translations() -> None:
    """Dynamically loads all JSON language files from the languages directory."""
    global TRANSLATIONS
    TRANSLATIONS = {}
    if not LANGUAGES_DIR.exists():
        return
    for lang_file in LANGUAGES_DIR.glob("*.json"):
        lang_code = lang_file.stem
        try:
            with open(lang_file, "r", encoding="utf-8") as f:
                TRANSLATIONS[lang_code] = json.load(f)
        except Exception as e:
            print(f"Error loading translation for {lang_code}: {e}")


def get_available_languages() -> list[str]:
    """Returns a list of all available language codes."""
    return list(TRANSLATIONS.keys())


# Initialize translation dictionaries
load_translations()


def set_language(lang: str) -> None:
    global _current_language
    if lang in TRANSLATIONS:
        _current_language = lang


def get_language() -> str:
    return _current_language


def t(key: str, default: str = None, **kwargs: Any) -> str:
    lang_dict = TRANSLATIONS.get(_current_language, TRANSLATIONS.get("en", {}))

    # Traverse nested dictionary using dot notation (e.g. "app.title")
    parts = key.split(".")
    current: Any = lang_dict
    for part in parts:
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            current = None
            break

    if current is None or not isinstance(current, str):
        text = default or key
    else:
        text = current

    if kwargs:
        try:
            return text.format(**kwargs)
        except Exception:
            return text
    return text

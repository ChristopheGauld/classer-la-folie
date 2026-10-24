"""Contenus éditoriaux : chapitres et lexique."""
import json
from pathlib import Path
_DATA = json.loads(Path(__file__).with_name("content.json").read_text(encoding="utf-8"))
LESSONS = _DATA["lessons"]
GLOSSARY = _DATA["glossary"]

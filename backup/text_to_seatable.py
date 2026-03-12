import json
from seatable_api import Base

# =========================
# DEINE DATEN
# =========================
BASE_TOKEN = "59034c7e8324e8741474125ff155d17236cc5c50"
SEATABLE_URL = "https://cloud.seatable.io"
TABLE_NAME = "Texts"
JSON_FILE = "texts.json"

def import_data():
    base = Base(BASE_TOKEN, SEATABLE_URL)
    base.auth()
    
    # 1. JSON-Datei laden
    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"❌ Datei '{JSON_FILE}' nicht gefunden!")
        return

    # 2. Daten für den Batch-Import vorbereiten
    rows = []
    for item in data:
        row = {
            "id": item.get("id"),
            "title": item.get("title"),
            "type": item.get("type"),
            "world": item.get("world"),
            "cr": item.get("cr"),
            "xp": item.get("xp"),
            "unit": 1, # Standardwert für deine Fortschrittsanzeige
            "text": item.get("text"),
            # Wir wandeln die Listen in Strings um, damit SeaTable sie schluckt
            "vocab": json.dumps(item.get("vocab", []), ensure_ascii=False),
            "questions": json.dumps(item.get("questions", []), ensure_ascii=False)
        }
        rows.append(row)

    # 3. Batch-Update (alle Zeilen auf einmal)
    try:
        base.batch_append_rows(TABLE_NAME, rows)
        print(f"✅ Erfolgreich {len(rows)} Texte in '{TABLE_NAME}' importiert!")
    except Exception as e:
        print(f"❌ Fehler beim Import: {e}")

if __name__ == "__main__":
    import_data()
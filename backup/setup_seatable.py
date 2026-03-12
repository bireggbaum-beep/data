from seatable_api import Base
from seatable_api.constants import ColumnTypes

# =========================
# NUR HIER EINTRAGEN
# =========================
BASE_TOKEN = "59034c7e8324e8741474125ff155d17236cc5c50"
SEATABLE_URL = "https://cloud.seatable.io"

TABLE_NAME = "Texts"

# Wichtig: ColumnTypes.TEXT statt "text", ColumnTypes.NUMBER statt "number" etc.
COLUMNS = [
    ("id", ColumnTypes.TEXT),
    ("title", ColumnTypes.TEXT),
    ("type", ColumnTypes.TEXT),
    ("world", ColumnTypes.TEXT),
    ("cr", ColumnTypes.NUMBER),
    ("xp", ColumnTypes.NUMBER),
    ("unit", ColumnTypes.NUMBER),
    ("text", ColumnTypes.LONG_TEXT),
    ("vocab", ColumnTypes.LONG_TEXT),
    ("questions", ColumnTypes.LONG_TEXT),
]


def main():
    base = Base(BASE_TOKEN, SEATABLE_URL)
    base.auth()
    print("✅ Authentifizierung erfolgreich!\n")

    # Tabelle erstellen
    try:
        base.add_table(TABLE_NAME)
        print(f"✅ Tabelle '{TABLE_NAME}' angelegt.")
    except Exception as e:
        if "exist" in str(e).lower():
            print(f"ℹ️ Tabelle '{TABLE_NAME}' existiert bereits.")
        else:
            print(f"❌ Tabelle erstellen fehlgeschlagen: {e}")
            return

    # Spalten erstellen
    print("\nErstelle Spalten...")
    for name, ctype in COLUMNS:
        try:
            base.insert_column(TABLE_NAME, name, ctype)
            print(f"  ✅ '{name}' ({ctype})")
        except Exception as e:
            if "exist" in str(e).lower() or "duplicate" in str(e).lower():
                print(f"  ℹ️ '{name}' existiert bereits.")
            else:
                print(f"  ❌ '{name}' fehlgeschlagen: {e}")

    print("\n🎉 Fertig!")


if __name__ == "__main__":
    main()

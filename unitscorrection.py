import json
import os
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEXTS_PATH = os.path.join(SCRIPT_DIR, "texts.json")

# ALLE 18 Texte → U2 (wie besprochen)
UNIT_MAP = {
    "tunnel_rat":           "YW3_U2",
    "broken_lantern":       "YW3_U2",
    "school_bell":          "YW3_U2",
    "mimic_warning":        "YW3_U2",
    "whispering_moss":      "YW3_U2",
    "spartan_checkpoint":   "YW3_U2",
    "brainrot":             "YW3_U2",
    "bone_collector":       "YW3_U2",
    "ambush_ruins":         "YW3_U2",
    "ring_fallen_knight":   "YW3_U2",
    "contract_wolf":        "YW3_U2",
    "group_project":        "YW3_U2",
    "drowned_temple":       "YW3_U2",
    "mad_wizard_note":      "YW3_U2",
    "rust_monster":         "YW3_U2",
    "oracle_delphi":        "YW3_U2",
    "margrath":             "YW3_U2",
    "beholder":             "YW3_U2",
}

# Saubere XP: exakt CR × 100, keine Variation
XP_BY_CR = {
    0.25: 25,
    0.5:  50,
    1:    100,
    2:    200,
    3:    300,
}


def compact_json(obj, indent=2):
    raw = json.dumps(obj, indent=indent, ensure_ascii=False)
    pattern = re.compile(
        r'\[\s*\n\s+'
        r'((?:"(?:[^"\\]|\\.)*"|[\d.]+)'
        r'(?:\s*,\s*\n\s+'
        r'(?:"(?:[^"\\]|\\.)*"|[\d.]+))*'
        r')\s*\n\s*\]',
        re.DOTALL
    )
    def replacer(m):
        collapsed = re.sub(r'\s*\n\s*', ' ', m.group(0))
        collapsed = re.sub(r'\s+', ' ', collapsed)
        collapsed = collapsed.replace('[ ', '[').replace(' ]', ']')
        return collapsed
    prev = None
    while prev != raw:
        prev = raw
        raw = pattern.sub(replacer, raw)
    return raw


def main():
    print(f"Lese: {TEXTS_PATH}")

    if not os.path.exists(TEXTS_PATH):
        print(f"❌ Datei nicht gefunden: {TEXTS_PATH}")
        return

    with open(TEXTS_PATH, "r", encoding="utf-8") as f:
        texts = json.load(f)

    print(f"Geladen: {len(texts)} Texte\n")

    for text in texts:
        tid = text["id"]
        cr = text["cr"]

        # Unit zuweisen
        if tid in UNIT_MAP:
            old_unit = text.get("unit", "—")
            text["unit"] = UNIT_MAP[tid]
            if old_unit != UNIT_MAP[tid]:
                print(f"  🔄 {tid:25s} unit: {old_unit} → {UNIT_MAP[tid]}")
            else:
                print(f"  ✅ {tid:25s} unit: {UNIT_MAP[tid]}")

        # XP standardisieren
        if cr in XP_BY_CR:
            old_xp = text["xp"]
            new_xp = XP_BY_CR[cr]
            if old_xp != new_xp:
                text["xp"] = new_xp
                print(f"     ↳ XP: {old_xp} → {new_xp}")

    # Felder sortieren
    field_order = ["id", "title", "type", "world", "unit", "cr", "xp", "text", "vocab", "questions"]
    ordered_texts = []
    for text in texts:
        ordered = {}
        for key in field_order:
            if key in text:
                ordered[key] = text[key]
        for key in text:
            if key not in ordered:
                ordered[key] = text[key]
        ordered_texts.append(ordered)

    output = compact_json(ordered_texts)
    with open(TEXTS_PATH, "w", encoding="utf-8") as f:
        f.write(output + "\n")

    print(f"\n✅ Gespeichert: {TEXTS_PATH}")

    # Zusammenfassung
    print("\n--- XP pro CR ---")
    cr_summary = {}
    for t in ordered_texts:
        cr = t["cr"]
        cr_summary.setdefault(cr, {"count": 0, "xp": 0})
        cr_summary[cr]["count"] += 1
        cr_summary[cr]["xp"] += t["xp"]

    total_xp = 0
    for cr in sorted(cr_summary.keys()):
        s = cr_summary[cr]
        total_xp += s["xp"]
        print(f"  CR {cr:5.2f}: {s['count']} Texte × {XP_BY_CR.get(cr, '?')} = {s['xp']} XP")
    print(f"  Total: {total_xp} XP")

    # Schwellen-Check
    print("\n--- Schwellen-Check (skip 1 pro Tier) ---")
    thresholds = [(2, 50), (3, 200), (4, 600), (5, 1400)]
    cumulative = 0
    for cr in sorted(cr_summary.keys()):
        s = cr_summary[cr]
        skip1_xp = s["xp"] - XP_BY_CR.get(cr, 0)  # minus 1 Text
        cumulative += skip1_xp
        print(f"  Nach CR {cr:.2f} (skip 1): kumulativ {cumulative} XP")
        for lvl, threshold in thresholds:
            if cumulative >= threshold:
                print(f"    → Level {lvl} ({threshold} XP) ✅")
                thresholds.remove((lvl, threshold))
                break

    if thresholds:
        print(f"\n  ⚠️ Nicht erreichbar mit U2 allein: {thresholds}")
        print(f"     → By Design: braucht U3-Texte")


if __name__ == "__main__":
    main()

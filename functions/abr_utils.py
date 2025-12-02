import os
import json

def choose_resolution(json_path, bandwidth):
    """Choisit la résolution en lisant les règles ABR depuis le JSON"""

    if not os.path.exists(json_path):
        return {"ready": False}

    with open(json_path, "r") as f:
        data = json.load(f)

    # Récupération des segments et règles ABR
    abr_rules = data.get("abr_rules", [])
    segments_data = data.get("segments", [])

    # 1️⃣ Trouver la résolution qui correspond au débit mesuré
    selected_res = None
    for rule in abr_rules:
        if rule["min_kbps"] <= bandwidth < rule["max_kbps"]:
            selected_res = rule["resolution"]
            break

    # Si aucune règle ne correspond (fallback)
    if selected_res is None:
        selected_res = abr_rules[-1]["resolution"]

    # 2️⃣ Récupérer les liens des segments à la bonne résolution
    segments_links = [seg["versions"][selected_res] for seg in segments_data]

    return {
        "resolution": selected_res,
        "segments": segments_links,
        "ready": True
    }

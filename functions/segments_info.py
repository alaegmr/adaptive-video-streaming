import os, json

# Définir les règles ABR globalement
ABR_RULES = [
    { "resolution": "360p", "min_kbps": 0, "max_kbps": 800 },
    { "resolution": "480p", "min_kbps": 800, "max_kbps": 1500 },
    { "resolution": "720p", "min_kbps": 1500, "max_kbps": 3500 },
    { "resolution": "1080p", "min_kbps": 3500, "max_kbps": 8000 },
    { "resolution": "4k", "min_kbps": 8000, "max_kbps": 999999 }
]

def save_segments_info(segments_versions, json_path):
    """
    Enregistre les infos des segments dans un JSON complet 
    avec abr_rules et segments.
    segments_versions doit être une liste de dicts :
    [{"name": "segment_1.mp4", "versions": {...}}, ...]
    """
    data = {
        "abr_rules": ABR_RULES,
        "segments": segments_versions
    }
    with open(json_path, "w") as f:
        json.dump(data, f, indent=4)


def get_segments_info(json_path, segments_folder):
    """Récupère la liste des segments existants"""
    if not os.path.exists(json_path):
        return {"ready": False, "segments": []}

    with open(json_path, "r") as f:
        data = json.load(f)

    # extraire la liste des segments
    segments = data.get("segments", [])

    existing_segments = []
    for seg in segments:
        # Vérifie si le fichier segment existe
        name = seg.get("name") if isinstance(seg, dict) else seg
        if os.path.exists(os.path.join(segments_folder, name)):
            existing_segments.append(name)
        else:
            existing_segments.append(None)

    return {"ready": True, "segments": existing_segments}

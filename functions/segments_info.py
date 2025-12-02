import os
import json

def save_segments_info(segments_versions, json_path):
    """Enregistre les infos des segments dans un JSON complet"""
    data = {
        "abr_rules": [
            {"resolution": "360p", "min_kbps": 0, "max_kbps": 800},
            {"resolution": "480p", "min_kbps": 800, "max_kbps": 1500},
            {"resolution": "720p", "min_kbps": 1500, "max_kbps": 3500},
            {"resolution": "1080p", "min_kbps": 3500, "max_kbps": 8000},
            {"resolution": "4k", "min_kbps": 8000, "max_kbps": 999999}
        ],
        "segments": segments_versions
    }
    with open(json_path, "w") as f:
        json.dump(data, f, indent=4)

def get_segments_info(json_path, segments_folder):
    """Récupère les segments existants et leur disponibilité"""
    if not os.path.exists(json_path):
        return {"ready": False}

    with open(json_path, "r") as f:
        data = json.load(f)

    segments = data.get("segments", [])
    existing_segments = []
    for seg in segments:
        name = seg.get("name")
        seg_path = os.path.join(segments_folder, name)
        if os.path.exists(seg_path):
            existing_segments.append(name)
        else:
            existing_segments.append(None)

    return {"ready": True, "segments": existing_segments}

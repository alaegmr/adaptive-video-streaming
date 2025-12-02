import os
import threading
from .segment_video import split_video
from .resize_video import fast_convert
from .segments_info import save_segments_info

def process_video(video_path, segments_folder, resized_folder, json_path, duration=10):
    """Découpe et crée toutes les résolutions d’une vidéo par résolution d’abord"""
    segments = split_video(video_path, segments_folder, duration)

    resolutions = ["4k", "1080p", "720p", "480p", "360p"]  # ordre souhaité
    resolution_map = {
        "360p": "640x360",
        "480p": "854x480",
        "720p": "1280x720",
        "1080p": "1920x1080",
        "4k": "3840x2160"
    }

    # Initialise la liste des versions par segment
    segments_versions = [{"name": os.path.basename(seg), "versions": {}} for seg in segments]

    for res in resolutions:
        threads = []
        for idx, seg in enumerate(segments):
            out_name = f"{os.path.splitext(os.path.basename(seg))[0]}_{res}.mp4"
            out_path = os.path.join(resized_folder, out_name)

            # Lance la conversion dans un thread
            res_dim = resolution_map[res]
            t = threading.Thread(target=fast_convert, args=(seg, out_path, res_dim))
            t.start()
            threads.append((t, idx, res, out_path))

        # Attend toutes les conversions pour cette résolution
        for t, idx, label, path in threads:
            t.join()
            segments_versions[idx]["versions"][label] = f"static/segments_resized/{os.path.basename(path)}"

    # Sauvegarde le JSON final
    save_segments_info(segments_versions, json_path)

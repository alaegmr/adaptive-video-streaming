import os, threading
from .ffmpeg_utils import fast_convert

def create_resolutions(segment_path, resized_folder):
    """Crée toutes les versions d’un segment"""
    resolutions = {
        "360p": "640x360",
        "480p": "854x480",
        "720p": "1280x720",
        "1080p": "1920x1080",
        "4k": "3840x2160"
    }

    versions = {}
    threads = []

    for label, res in resolutions.items():
        out_name = f"{os.path.splitext(os.path.basename(segment_path))[0]}_{label}.mp4"
        out_path = os.path.join(resized_folder, out_name)
        t = threading.Thread(target=fast_convert, args=(segment_path, out_path, res))
        t.start()
        threads.append(t)
        versions[label] = f"static/segments_resized/{out_name}"

    for t in threads: t.join()
    return versions

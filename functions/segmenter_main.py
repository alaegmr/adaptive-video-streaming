import os
from .segment_video import split_video
from .resize_video import create_resolutions
from .segments_info import save_segments_info

def process_video(video_path, segments_folder, resized_folder, json_path, duration=10):
    """Découpe et crée toutes les résolutions d’une vidéo"""
    segments = split_video(video_path, segments_folder, duration)
    segments_versions = []
    for seg in segments:
        versions = create_resolutions(seg, resized_folder)
        segments_versions.append({"name": os.path.basename(seg), "versions": versions})
    save_segments_info(segments_versions, json_path)

import os, math, subprocess
from .ffmpeg_utils import run_ffmpeg

def split_video(video_path, segments_folder, duration=10):
    """Découpe une vidéo en segments"""
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", video_path],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    total_duration = float(result.stdout.strip())
    num_segments = math.ceil(total_duration / duration)

    segment_paths = []

    for i in range(num_segments):
        start = i * duration
        segment_name = f"segment_{i+1}.mp4"
        segment_path = os.path.join(segments_folder, segment_name)

        run_ffmpeg([
            "ffmpeg", "-y", "-i", video_path,
            "-ss", str(start),
            "-t", str(duration),
            "-c", "copy",
            segment_path
        ])

        segment_paths.append(segment_path)

    return segment_paths

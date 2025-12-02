import subprocess

def run_ffmpeg(cmd):
    """Exécute une commande ffmpeg"""
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def fast_convert(input_path, output_path, resolution):
    """Convertit une vidéo à une résolution spécifique"""
    run_ffmpeg([
        "ffmpeg", "-y", "-i", input_path,
        "-vf", f"scale={resolution}",
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-crf", "23",
        output_path
    ])

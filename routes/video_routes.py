from flask import Blueprint, request, jsonify, render_template, send_from_directory
import os, threading
from functions.segmenter_main import process_video
from functions.segments_info import get_segments_info
from functions.abr_utils import choose_resolution
from functions.testfile import create_testfile

video_bp = Blueprint("video_bp", __name__)

# ----------------- Chemins globaux -----------------
UPLOAD_FOLDER = os.path.join("static", "uploads")
SEGMENTS_FOLDER = os.path.join("static", "segments")
RESIZED_FOLDER = os.path.join("static", "segments_resized")
JSON_PATH = os.path.join("static", "segments_info.json")


# ----------------- Pages HTML -----------------
@video_bp.route("/")
def root_redirect():
    """Redirige vers la page de segmentation au démarrage de l'app."""
    return render_template("segmentation.html")

@video_bp.route("/segmentation")
def segmentation_page():
    """Page pour uploader et segmenter la vidéo."""
    return render_template("segmentation.html")

@video_bp.route("/player")
def player_page():
    """Page du lecteur vidéo (après segmentation)."""
    return render_template("index.html")


# ----------------- API Segmentation -----------------
@video_bp.route("/segment", methods=["POST"])
def segment_video_route():
    """Lance la segmentation d'une vidéo uploadée."""
    file = request.files.get("video")
    duration = int(request.form.get("duration", 10))

    if not file:
        return jsonify({"success": False, "error": "Aucune vidéo envoyée"}), 400

    video_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(video_path)

    # Nettoyage des dossiers segments et resized
    for folder in [SEGMENTS_FOLDER, RESIZED_FOLDER]:
        for f in os.listdir(folder):
            os.remove(os.path.join(folder, f))

    # Lancement de la segmentation dans un thread
    threading.Thread(
        target=process_video,
        args=(video_path, SEGMENTS_FOLDER, RESIZED_FOLDER, JSON_PATH, duration)
    ).start()

    return jsonify({"success": True, "message": "Segmentation lancée ✅"})


@video_bp.route("/segments_info")
def segments_info_route():
    """Retourne l'état des segments existants pour le front."""
    return jsonify(get_segments_info(JSON_PATH, SEGMENTS_FOLDER))


@video_bp.route("/abr", methods=["POST"])
def abr_route():
    """Choisit la résolution en fonction de la bande passante."""
    data = request.json
    bandwidth = data.get("bandwidth", 2000)
    return jsonify(choose_resolution(JSON_PATH, bandwidth))


# ----------------- Fichiers statiques / Test -----------------
@video_bp.route("/static/testfile_1MB.bin")
def testfile_route():
    create_testfile("static")
    return send_from_directory("static", "testfile_1MB.bin")

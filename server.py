from flask import Flask
import os
from routes import register_routes  # <== vérifie que routes/__init__.py existe

app = Flask(__name__, static_folder="static", template_folder="templates")

# Création des dossiers
for folder in ["uploads", "segments", "segments_resized"]:
    os.makedirs(os.path.join(app.static_folder, folder), exist_ok=True)

# Enregistrement des routes
register_routes(app)

if __name__ == "__main__":
    app.run(debug=True)

from routes.video_routes import video_bp  # import absolu

def register_routes(app):
    """Enregistre toutes les routes du Blueprint dans l'application Flask"""
    app.register_blueprint(video_bp)

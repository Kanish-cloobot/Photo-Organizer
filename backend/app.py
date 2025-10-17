from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from database import init_db
from routes.albums import albums_bp
from routes.photos import photos_bp
import os

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key-here'
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
    
    # Enable CORS for frontend
    CORS(app)
    
    # Create upload directories
    os.makedirs('uploads/originals', exist_ok=True)
    os.makedirs('uploads/compressed', exist_ok=True)
    
    # Initialize database
    init_db()
    
    # Register blueprints
    app.register_blueprint(albums_bp, url_prefix='/api')
    app.register_blueprint(photos_bp, url_prefix='/api')
    
    @app.route('/api/health')
    def health_check():
        return jsonify({'status': 'healthy', 'message': 'Photo Organizer API is running'})
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)

import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///photo_organizer.db'
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'heic', 'heif'}
    
    # Image compression settings
    MAX_WIDTH = 1920
    JPEG_QUALITY = 85
    PNG_COMPRESS_LEVEL = 6
    
    # File storage paths
    ORIGINALS_FOLDER = 'uploads/originals'
    COMPRESSED_FOLDER = 'uploads/compressed'

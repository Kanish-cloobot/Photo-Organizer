import os
from config import Config

def get_file_path(relative_path):
    """Get absolute path for compressed files"""
    return os.path.join(Config.COMPRESSED_FOLDER, os.path.basename(relative_path))

def get_original_file_path(relative_path):
    """Get absolute path for original files"""
    return os.path.join(Config.ORIGINALS_FOLDER, os.path.basename(relative_path))

def ensure_directories():
    """Ensure upload directories exist"""
    os.makedirs(Config.ORIGINALS_FOLDER, exist_ok=True)
    os.makedirs(Config.COMPRESSED_FOLDER, exist_ok=True)

def cleanup_file(file_path):
    """Delete file if it exists"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
    except Exception:
        pass
    return False

def get_file_size(file_path):
    """Get file size in bytes"""
    try:
        return os.path.getsize(file_path)
    except Exception:
        return 0

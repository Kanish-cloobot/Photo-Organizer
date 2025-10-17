from flask import Blueprint, request, jsonify, send_file
import os
from database import get_photos_by_album, create_photo, delete_photo, get_photo_by_id
from services.image_processor import process_uploaded_photos
from services.file_manager import get_file_path, get_original_file_path

photos_bp = Blueprint('photos', __name__)

@photos_bp.route('/albums/<int:album_id>/photos', methods=['GET'])
def get_album_photos(album_id):
    """Get all photos in album"""
    try:
        photos = get_photos_by_album(album_id)
        photos_data = []
        
        for photo in photos:
            photo_data = {
                'id': photo['id'],
                'filename': photo['filename'],
                'original_filename': photo['original_filename'],
                'file_format': photo['file_format'],
                'original_size': photo['original_size'],
                'compressed_size': photo['compressed_size'],
                'width': photo['width'],
                'height': photo['height'],
                'compression_ratio': photo['compression_ratio'],
                'created_at': photo['created_at']
            }
            photos_data.append(photo_data)
        
        return jsonify(photos_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@photos_bp.route('/albums/<int:album_id>/photos', methods=['POST'])
def upload_photos(album_id):
    """Upload photos to album"""
    try:
        if 'files' not in request.files:
            return jsonify({'error': 'No files provided'}), 400
        
        files = request.files.getlist('files')
        
        if not files or all(file.filename == '' for file in files):
            return jsonify({'error': 'No files selected'}), 400
        
        # Process uploaded photos
        result = process_uploaded_photos(album_id, files)
        
        if result['failed'] > 0:
            return jsonify({
                'uploaded': result['uploaded'],
                'failed': result['failed'],
                'photos': result['photos'],
                'errors': result.get('errors', []),
                'message': f"Uploaded {result['uploaded']} photos, {result['failed']} failed"
            }), 207  # Multi-status
        
        return jsonify({
            'uploaded': result['uploaded'],
            'failed': result['failed'],
            'photos': result['photos'],
            'message': f"Successfully uploaded {result['uploaded']} photos"
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@photos_bp.route('/photos/<int:photo_id>', methods=['DELETE'])
def delete_photo_route(photo_id):
    """Delete photo (soft delete)"""
    try:
        success = delete_photo(photo_id)
        
        if not success:
            return jsonify({'error': 'Photo not found'}), 404
        
        return jsonify({'message': 'Photo deleted successfully'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@photos_bp.route('/photos/<int:photo_id>/download', methods=['GET'])
def download_photo(photo_id):
    """Download original photo"""
    try:
        photo = get_photo_by_id(photo_id)
        
        if not photo:
            return jsonify({'error': 'Photo not found'}), 404
        
        original_path = get_original_file_path(photo['original_path'])
        
        if not os.path.exists(original_path):
            return jsonify({'error': 'Original file not found'}), 404
        
        return send_file(
            original_path,
            as_attachment=True,
            download_name=photo['original_filename']
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@photos_bp.route('/photos/<int:photo_id>/view', methods=['GET'])
def view_photo(photo_id):
    """View compressed photo"""
    try:
        photo = get_photo_by_id(photo_id)
        
        if not photo:
            return jsonify({'error': 'Photo not found'}), 404
        
        compressed_path = get_file_path(photo['compressed_path'])
        
        if not os.path.exists(compressed_path):
            return jsonify({'error': 'Compressed file not found'}), 404
        
        return send_file(compressed_path)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

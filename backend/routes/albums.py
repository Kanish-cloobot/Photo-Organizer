from flask import Blueprint, request, jsonify
from database import (
    get_all_albums, get_album_by_id, create_album, 
    update_album, delete_album, get_photos_by_album
)

albums_bp = Blueprint('albums', __name__)

@albums_bp.route('/albums', methods=['GET'])
def get_albums():
    """Get all active albums"""
    try:
        albums = get_all_albums()
        albums_data = []
        
        for album in albums:
            album_data = {
                'id': album['id'],
                'name': album['name'],
                'description': album['description'],
                'photo_count': album['photo_count'],
                'created_at': album['created_at'],
                'updated_at': album['updated_at']
            }
            albums_data.append(album_data)
        
        return jsonify(albums_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@albums_bp.route('/albums/<int:album_id>', methods=['GET'])
def get_album(album_id):
    """Get album details with photos"""
    try:
        album = get_album_by_id(album_id)
        if not album:
            return jsonify({'error': 'Album not found'}), 404
        
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
        
        album_data = {
            'id': album['id'],
            'name': album['name'],
            'description': album['description'],
            'photo_count': album['photo_count'],
            'photos': photos_data,
            'created_at': album['created_at'],
            'updated_at': album['updated_at']
        }
        
        return jsonify(album_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@albums_bp.route('/albums', methods=['POST'])
def create_new_album():
    """Create new album"""
    try:
        data = request.get_json()
        
        if not data or 'name' not in data:
            return jsonify({'error': 'Album name is required'}), 400
        
        name = data['name'].strip()
        description = data.get('description', '').strip() if data.get('description') else None
        
        if not name:
            return jsonify({'error': 'Album name cannot be empty'}), 400
        
        album_id = create_album(name, description)
        
        return jsonify({
            'id': album_id,
            'name': name,
            'description': description,
            'photo_count': 0,
            'message': 'Album created successfully'
        }), 201
        
    except Exception as e:
        if 'UNIQUE constraint failed' in str(e):
            return jsonify({'error': 'Album name already exists'}), 409
        return jsonify({'error': str(e)}), 500

@albums_bp.route('/albums/<int:album_id>', methods=['PUT'])
def update_album_details(album_id):
    """Update album"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        name = data.get('name')
        description = data.get('description')
        
        if name is not None:
            name = name.strip()
            if not name:
                return jsonify({'error': 'Album name cannot be empty'}), 400
        
        if description is not None:
            description = description.strip() if description else None
        
        success = update_album(album_id, name, description)
        
        if not success:
            return jsonify({'error': 'Album not found'}), 404
        
        return jsonify({'message': 'Album updated successfully'})
        
    except Exception as e:
        if 'UNIQUE constraint failed' in str(e):
            return jsonify({'error': 'Album name already exists'}), 409
        return jsonify({'error': str(e)}), 500

@albums_bp.route('/albums/<int:album_id>', methods=['DELETE'])
def delete_album_route(album_id):
    """Delete album (soft delete)"""
    try:
        success = delete_album(album_id)
        
        if not success:
            return jsonify({'error': 'Album not found'}), 404
        
        return jsonify({'message': 'Album deleted successfully'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

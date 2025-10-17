import sqlite3
import os
from datetime import datetime

DATABASE_PATH = 'photo_organizer.db'

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database with tables and triggers"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create albums table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS albums (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT,
            cover_photo_id INTEGER,
            status TEXT DEFAULT 'active' CHECK(status IN ('active', 'archived', 'deleted')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (cover_photo_id) REFERENCES photos(id) ON DELETE SET NULL
        )
    ''')
    
    # Create photos table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS photos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            album_id INTEGER NOT NULL,
            filename TEXT NOT NULL,
            original_filename TEXT NOT NULL,
            file_format TEXT NOT NULL CHECK(file_format IN ('PNG', 'JPEG', 'HEIC')),
            original_path TEXT NOT NULL,
            compressed_path TEXT NOT NULL,
            original_size INTEGER NOT NULL,
            compressed_size INTEGER NOT NULL,
            width INTEGER,
            height INTEGER,
            compression_ratio REAL,
            status TEXT DEFAULT 'active' CHECK(status IN ('active', 'deleted')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (album_id) REFERENCES albums(id) ON DELETE CASCADE
        )
    ''')
    
    # Create indexes
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_albums_status ON albums(status)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_albums_created_at ON albums(created_at DESC)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_photos_album_id ON photos(album_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_photos_status ON photos(status)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_photos_created_at ON photos(created_at DESC)')
    
    # Create triggers for updated_at
    cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS update_albums_timestamp 
        AFTER UPDATE ON albums
        FOR EACH ROW
        BEGIN
            UPDATE albums SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
        END
    ''')
    
    cursor.execute('''
        CREATE TRIGGER IF NOT EXISTS update_photos_timestamp 
        AFTER UPDATE ON photos
        FOR EACH ROW
        BEGIN
            UPDATE photos SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
        END
    ''')
    
    conn.commit()
    conn.close()

def get_album_by_id(album_id):
    """Get album by ID with photo count"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT a.*, 
               COUNT(p.id) as photo_count
        FROM albums a
        LEFT JOIN photos p ON a.id = p.album_id AND p.status = 'active'
        WHERE a.id = ? AND a.status = 'active'
        GROUP BY a.id
    ''', (album_id,))
    
    album = cursor.fetchone()
    conn.close()
    return album

def get_all_albums():
    """Get all active albums with photo counts"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT a.*, 
               COUNT(p.id) as photo_count
        FROM albums a
        LEFT JOIN photos p ON a.id = p.album_id AND p.status = 'active'
        WHERE a.status = 'active'
        GROUP BY a.id
        ORDER BY a.created_at DESC
    ''')
    
    albums = cursor.fetchall()
    conn.close()
    return albums

def create_album(name, description=None):
    """Create new album"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO albums (name, description)
        VALUES (?, ?)
    ''', (name, description))
    
    album_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return album_id

def update_album(album_id, name=None, description=None):
    """Update album"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    updates = []
    params = []
    
    if name is not None:
        updates.append('name = ?')
        params.append(name)
    
    if description is not None:
        updates.append('description = ?')
        params.append(description)
    
    if updates:
        params.append(album_id)
        cursor.execute(f'''
            UPDATE albums 
            SET {', '.join(updates)}
            WHERE id = ? AND status = 'active'
        ''', params)
        
        conn.commit()
        success = cursor.rowcount > 0
    else:
        success = True
    
    conn.close()
    return success

def delete_album(album_id):
    """Soft delete album"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE albums 
        SET status = 'deleted'
        WHERE id = ? AND status = 'active'
    ''', (album_id,))
    
    success = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return success

def get_photos_by_album(album_id):
    """Get all active photos in album"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM photos
        WHERE album_id = ? AND status = 'active'
        ORDER BY created_at DESC
    ''', (album_id,))
    
    photos = cursor.fetchall()
    conn.close()
    return photos

def create_photo(album_id, filename, original_filename, file_format, 
                original_path, compressed_path, original_size, compressed_size,
                width=None, height=None):
    """Create photo record"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    compression_ratio = ((original_size - compressed_size) / original_size * 100) if original_size > 0 else 0
    
    cursor.execute('''
        INSERT INTO photos (album_id, filename, original_filename, file_format,
                          original_path, compressed_path, original_size, compressed_size,
                          width, height, compression_ratio)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (album_id, filename, original_filename, file_format,
          original_path, compressed_path, original_size, compressed_size,
          width, height, compression_ratio))
    
    photo_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return photo_id

def delete_photo(photo_id):
    """Soft delete photo"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE photos 
        SET status = 'deleted'
        WHERE id = ? AND status = 'active'
    ''', (photo_id,))
    
    success = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return success

def get_photo_by_id(photo_id):
    """Get photo by ID"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM photos
        WHERE id = ? AND status = 'active'
    ''', (photo_id,))
    
    photo = cursor.fetchone()
    conn.close()
    return photo

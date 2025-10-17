import os
import time
import random
from PIL import Image
import pillow_heif
from config import Config

# Register HEIF opener with Pillow
pillow_heif.register_heif_opener()

def generate_filename(original_filename, file_format):
    """Generate unique filename with timestamp"""
    timestamp = int(time.time())
    random_suffix = random.randint(1000, 9999)
    name, _ = os.path.splitext(original_filename)
    safe_name = "".join(c for c in name if c.isalnum() or c in (' ', '-', '_')).rstrip()
    safe_name = safe_name.replace(' ', '_')
    return f"photo_{timestamp}_{random_suffix}.{file_format.lower()}"

def compress_image(input_path, output_path, file_format):
    """Compress image with specified format"""
    try:
        # Handle HEIC files
        if file_format.upper() == 'HEIC':
            heif_file = pillow_heif.read_heif(input_path)
            image = Image.frombytes(
                heif_file.mode, 
                heif_file.size, 
                heif_file.data
            )
            # Convert HEIC to JPEG
            file_format = 'JPEG'
        else:
            image = Image.open(input_path)
        
        # Get image dimensions
        width, height = image.size
        
        # Resize if width > max_width
        if width > Config.MAX_WIDTH:
            ratio = Config.MAX_WIDTH / width
            new_size = (Config.MAX_WIDTH, int(height * ratio))
            image = image.resize(new_size, Image.Resampling.LANCZOS)
            width, height = new_size
        
        # Save with compression
        if file_format.upper() == 'JPEG':
            # Convert to RGB if necessary (for PNG with transparency)
            if image.mode in ('RGBA', 'LA', 'P'):
                # Create white background
                background = Image.new('RGB', image.size, (255, 255, 255))
                if image.mode == 'P':
                    image = image.convert('RGBA')
                background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
                image = background
            
            image.save(output_path, 'JPEG', quality=Config.JPEG_QUALITY, optimize=True)
        else:  # PNG
            image.save(output_path, 'PNG', optimize=True, compress_level=Config.PNG_COMPRESS_LEVEL)
        
        return os.path.getsize(output_path), width, height
        
    except Exception as e:
        raise Exception(f"Image compression failed: {str(e)}")

def process_uploaded_photos(album_id, files):
    """Process multiple uploaded photos"""
    uploaded_photos = []
    failed_uploads = []
    errors = []
    
    for file in files:
        try:
            # Validate file
            if not file or file.filename == '':
                continue
            
            # Get file extension
            filename = file.filename
            file_ext = os.path.splitext(filename)[1].lower().lstrip('.')
            
            if file_ext not in Config.ALLOWED_EXTENSIONS:
                errors.append(f"File {filename}: Unsupported format")
                failed_uploads.append(filename)
                continue
            
            # Determine file format
            if file_ext in ['heic', 'heif']:
                file_format = 'HEIC'
            elif file_ext in ['jpg', 'jpeg']:
                file_format = 'JPEG'
            elif file_ext == 'png':
                file_format = 'PNG'
            else:
                errors.append(f"File {filename}: Unknown format")
                failed_uploads.append(filename)
                continue
            
            # Generate unique filename
            compressed_filename = generate_filename(filename, file_format)
            original_filename = generate_filename(filename, file_format)
            
            # Create file paths
            original_path = os.path.join(Config.ORIGINALS_FOLDER, original_filename)
            compressed_path = os.path.join(Config.COMPRESSED_FOLDER, compressed_filename)
            
            # Save original file
            file.save(original_path)
            original_size = os.path.getsize(original_path)
            
            # Compress image
            compressed_size, width, height = compress_image(original_path, compressed_path, file_format)
            
            # Import here to avoid circular import
            from database import create_photo
            
            # Save to database
            photo_id = create_photo(
                album_id=album_id,
                filename=compressed_filename,
                original_filename=filename,
                file_format=file_format,
                original_path=original_path,
                compressed_path=compressed_path,
                original_size=original_size,
                compressed_size=compressed_size,
                width=width,
                height=height
            )
            
            # Calculate compression ratio
            compression_ratio = ((original_size - compressed_size) / original_size * 100) if original_size > 0 else 0
            
            uploaded_photos.append({
                'id': photo_id,
                'filename': compressed_filename,
                'original_filename': filename,
                'file_format': file_format,
                'original_size': original_size,
                'compressed_size': compressed_size,
                'width': width,
                'height': height,
                'compression_ratio': round(compression_ratio, 2)
            })
            
        except Exception as e:
            error_msg = f"File {filename}: {str(e)}"
            errors.append(error_msg)
            failed_uploads.append(filename)
    
    return {
        'uploaded': len(uploaded_photos),
        'failed': len(failed_uploads),
        'photos': uploaded_photos,
        'errors': errors
    }

# Import will be done at function call to avoid circular import

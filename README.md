# 📷 Photo Organizer MVP

A lightweight, local web-based photo organizer with album management and automatic image compression.

## ✨ Features

- **Album Management**: Create, edit, and delete photo albums
- **Photo Upload**: Drag & drop or click to upload multiple photos
- **Image Compression**: Automatic compression with HEIC support
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Local Storage**: All data stored locally using SQLite
- **Format Support**: JPEG, PNG, and HEIC/HEIF formats

## 🏗️ Architecture

- **Frontend**: React 18 + Vite
- **Backend**: Flask (Python 3.9+)
- **Database**: SQLite3
- **Image Processing**: Pillow (PIL) + pillow-heif

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- Node.js 16 or higher
- npm or yarn

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Photo-Organizer
   ```

2. **Set up the backend**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Set up the frontend**
   ```bash
   cd ../frontend
   npm install
   ```

### Running the Application

1. **Start the backend server**
   ```bash
   cd backend
   python app.py
   ```
   The API will be available at `http://localhost:5000`

2. **Start the frontend development server**
   ```bash
   cd frontend
   npm run dev
   ```
   The web app will be available at `http://localhost:3000`

## 📁 Project Structure

```
Photo-Organizer/
├── backend/
│   ├── app.py                 # Flask application entry point
│   ├── config.py              # Configuration settings
│   ├── database.py            # Database operations
│   ├── requirements.txt       # Python dependencies
│   ├── routes/
│   │   ├── albums.py          # Album API endpoints
│   │   └── photos.py          # Photo API endpoints
│   ├── services/
│   │   ├── image_processor.py # Image compression logic
│   │   └── file_manager.py    # File operations
│   └── uploads/               # Upload directories
│       ├── originals/         # Original photos
│       └── compressed/        # Compressed photos
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── pages/            # Page components
│   │   ├── services/         # API service
│   │   ├── App.jsx           # Main app component
│   │   ├── main.jsx          # App entry point
│   │   └── index.css         # Global styles
│   ├── package.json          # Node.js dependencies
│   └── vite.config.js        # Vite configuration
│
└── README.md
```

## 🔧 API Endpoints

### Albums
- `GET /api/albums` - List all albums
- `GET /api/albums/:id` - Get album with photos
- `POST /api/albums` - Create new album
- `PUT /api/albums/:id` - Update album
- `DELETE /api/albums/:id` - Delete album

### Photos
- `GET /api/albums/:id/photos` - Get photos in album
- `POST /api/albums/:id/photos` - Upload photos
- `DELETE /api/photos/:id` - Delete photo
- `GET /api/photos/:id/view` - View compressed photo
- `GET /api/photos/:id/download` - Download original photo

## 🖼️ Image Processing

The application automatically compresses uploaded images:

- **Max Width**: 1920px (maintains aspect ratio)
- **JPEG Quality**: 85%
- **PNG**: Optimized with compression level 6
- **HEIC/HEIF**: Converted to JPEG format

## 🎨 UI Components

- **Album Grid**: Responsive grid showing all albums
- **Album Detail**: Photo grid with upload functionality
- **Photo Upload**: Drag & drop interface
- **Modal Forms**: Create/edit album forms
- **Responsive Design**: Mobile-first approach

## 🗄️ Database Schema

### Albums Table
- `id` - Primary key
- `name` - Album name (unique)
- `description` - Optional description
- `cover_photo_id` - Reference to cover photo
- `status` - active/archived/deleted
- `created_at` - Creation timestamp
- `updated_at` - Last update timestamp

### Photos Table
- `id` - Primary key
- `album_id` - Foreign key to albums
- `filename` - Compressed filename
- `original_filename` - Original filename
- `file_format` - PNG/JPEG/HEIC
- `original_path` - Path to original file
- `compressed_path` - Path to compressed file
- `original_size` - Original file size
- `compressed_size` - Compressed file size
- `width` - Image width
- `height` - Image height
- `compression_ratio` - Compression percentage
- `status` - active/deleted
- `created_at` - Creation timestamp
- `updated_at` - Last update timestamp

## 🧪 Testing

The application includes comprehensive test cases:

1. **Album Management**
   - Create, edit, delete albums
   - Unique name validation
   - Soft delete functionality

2. **Photo Upload**
   - Multiple file upload
   - Format validation (JPEG, PNG, HEIC)
   - Compression verification
   - Error handling

3. **Image Processing**
   - HEIC to JPEG conversion
   - Size optimization
   - Quality preservation
   - Transparency handling

## 🔒 Security Features

- **File Validation**: Only image files allowed
- **Size Limits**: 16MB max file size
- **Path Sanitization**: Secure file handling
- **Soft Deletes**: Data recovery capability

## 🚀 Performance

- **Lazy Loading**: Images loaded on demand
- **Compression**: Reduced storage requirements
- **Indexing**: Database indexes for fast queries
- **Caching**: Efficient file serving

## 🛠️ Development

### Backend Development
```bash
cd backend
python app.py
```

### Frontend Development
```bash
cd frontend
npm run dev
```

### Building for Production
```bash
cd frontend
npm run build
```

## 📝 Configuration

Edit `backend/config.py` to customize:
- Upload limits
- Image compression settings
- File storage paths
- Database configuration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
1. Check the existing issues
2. Create a new issue with detailed description
3. Include error logs and steps to reproduce

## 🔮 Future Enhancements

- Search functionality
- Photo tagging
- Cloud storage integration
- User authentication
- Batch operations
- Photo editing tools
- Export functionality
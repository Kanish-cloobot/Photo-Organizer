import React from 'react'

const PhotoGrid = ({ photos, onDelete, isLoading }) => {
  if (isLoading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
        Loading photos...
      </div>
    )
  }

  if (photos.length === 0) {
    return (
      <div className="empty-state">
        <div className="empty-state-icon">🖼️</div>
        <h3 className="empty-state-title">No photos yet</h3>
        <p className="empty-state-text">
          Upload your first photo to get started
        </p>
      </div>
    )
  }

  return (
    <div className="photo-grid">
      {photos.map((photo) => (
        <div key={photo.id} className="photo-item">
          <img
            src={`/api/photos/${photo.id}/view`}
            alt={photo.original_filename}
            loading="lazy"
            onError={(e) => {
              e.target.style.display = 'none'
            }}
          />
          <div className="photo-overlay">
            <button
              className="btn btn-sm btn-danger"
              onClick={() => {
                if (window.confirm(`Delete "${photo.original_filename}"?`)) {
                  onDelete(photo.id)
                }
              }}
              title="Delete photo"
            >
              🗑️
            </button>
          </div>
        </div>
      ))}
    </div>
  )
}

export default PhotoGrid

import React from 'react'

const AlbumCard = ({ album, onEdit, onDelete, onView }) => {
  const handleCardClick = (e) => {
    // Don't navigate if clicking on action buttons
    if (e.target.closest('.album-actions')) {
      return
    }
    onView(album.id)
  }

  const handleEdit = (e) => {
    e.stopPropagation()
    onEdit(album)
  }

  const handleDelete = (e) => {
    e.stopPropagation()
    if (window.confirm(`Are you sure you want to delete "${album.name}"? This action cannot be undone.`)) {
      onDelete(album.id)
    }
  }

  return (
    <div className="card album-card" onClick={handleCardClick}>
      <div className="album-cover">
        {album.cover_photo ? (
          <img 
            src={`/api/photos/${album.cover_photo}/view`} 
            alt={album.name}
            onError={(e) => {
              e.target.style.display = 'none'
            }}
          />
        ) : (
          <div>📷</div>
        )}
      </div>
      
      <div className="album-info">
        <h3 className="album-name">{album.name}</h3>
        {album.description && (
          <p className="album-description">{album.description}</p>
        )}
        <div className="album-stats">
          {album.photo_count} {album.photo_count === 1 ? 'photo' : 'photos'}
        </div>
      </div>
      
      <div className="album-actions">
        <button
          className="btn btn-sm btn-secondary"
          onClick={handleEdit}
          title="Edit album"
        >
          ✏️
        </button>
        <button
          className="btn btn-sm btn-danger"
          onClick={handleDelete}
          title="Delete album"
        >
          🗑️
        </button>
      </div>
    </div>
  )
}

export default AlbumCard

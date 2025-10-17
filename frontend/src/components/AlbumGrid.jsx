import React from 'react'
import AlbumCard from './AlbumCard'

const AlbumGrid = ({ albums, onEdit, onDelete, onView, isLoading }) => {
  if (isLoading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
        Loading albums...
      </div>
    )
  }

  if (albums.length === 0) {
    return (
      <div className="empty-state">
        <div className="empty-state-icon">📷</div>
        <h3 className="empty-state-title">No albums yet</h3>
        <p className="empty-state-text">
          Create your first album to start organizing your photos
        </p>
      </div>
    )
  }

  return (
    <div className="grid grid-cols-3">
      {albums.map((album) => (
        <AlbumCard
          key={album.id}
          album={album}
          onEdit={onEdit}
          onDelete={onDelete}
          onView={onView}
        />
      ))}
    </div>
  )
}

export default AlbumGrid

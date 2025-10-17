import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { albumsAPI } from '../services/api'
import AlbumGrid from '../components/AlbumGrid'
import AlbumForm from '../components/AlbumForm'
import Modal from '../components/Modal'

const Albums = () => {
  const [albums, setAlbums] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [editingAlbum, setEditingAlbum] = useState(null)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState(null)
  
  const navigate = useNavigate()

  useEffect(() => {
    loadAlbums()
  }, [])

  const loadAlbums = async () => {
    try {
      setIsLoading(true)
      setError(null)
      const response = await albumsAPI.getAll()
      setAlbums(response.data)
    } catch (err) {
      setError('Failed to load albums. Please try again.')
      console.error('Error loading albums:', err)
    } finally {
      setIsLoading(false)
    }
  }

  const handleCreateAlbum = () => {
    setEditingAlbum(null)
    setIsModalOpen(true)
  }

  const handleEditAlbum = (album) => {
    setEditingAlbum(album)
    setIsModalOpen(true)
  }

  const handleSubmitAlbum = async (formData) => {
    try {
      setIsSubmitting(true)
      setError(null)

      if (editingAlbum) {
        // Update existing album
        await albumsAPI.update(editingAlbum.id, formData)
        await loadAlbums() // Reload to get updated data
      } else {
        // Create new album
        await albumsAPI.create(formData)
        await loadAlbums() // Reload to get new album
      }

      setIsModalOpen(false)
      setEditingAlbum(null)
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to save album. Please try again.')
      console.error('Error saving album:', err)
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleDeleteAlbum = async (albumId) => {
    try {
      setError(null)
      await albumsAPI.delete(albumId)
      await loadAlbums() // Reload to remove deleted album
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to delete album. Please try again.')
      console.error('Error deleting album:', err)
    }
  }

  const handleViewAlbum = (albumId) => {
    navigate(`/album/${albumId}`)
  }

  const handleCloseModal = () => {
    if (!isSubmitting) {
      setIsModalOpen(false)
      setEditingAlbum(null)
      setError(null)
    }
  }

  return (
    <div className="container">
      <header className="header">
        <div className="header-content">
          <h1>Photo Organizer</h1>
          <button
            className="btn btn-primary"
            onClick={handleCreateAlbum}
          >
            + New Album
          </button>
        </div>
      </header>

      {error && (
        <div className="mb-4" style={{ 
          background: '#fed7d7', 
          color: '#c53030', 
          padding: '12px', 
          borderRadius: '8px',
          textAlign: 'center'
        }}>
          {error}
        </div>
      )}

      <AlbumGrid
        albums={albums}
        onEdit={handleEditAlbum}
        onDelete={handleDeleteAlbum}
        onView={handleViewAlbum}
        isLoading={isLoading}
      />

      <Modal
        isOpen={isModalOpen}
        onClose={handleCloseModal}
        title={editingAlbum ? 'Edit Album' : 'Create New Album'}
      >
        <AlbumForm
          album={editingAlbum}
          onSubmit={handleSubmitAlbum}
          onCancel={handleCloseModal}
          isLoading={isSubmitting}
        />
      </Modal>
    </div>
  )
}

export default Albums

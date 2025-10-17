import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { albumsAPI, photosAPI } from '../services/api'
import PhotoUpload from '../components/PhotoUpload'
import PhotoGrid from '../components/PhotoGrid'
import AlbumForm from '../components/AlbumForm'
import Modal from '../components/Modal'

const AlbumDetail = () => {
  const { id } = useParams()
  const navigate = useNavigate()
  
  const [album, setAlbum] = useState(null)
  const [photos, setPhotos] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [isUploading, setIsUploading] = useState(false)
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState(null)
  const [uploadProgress, setUploadProgress] = useState(null)

  useEffect(() => {
    loadAlbum()
  }, [id])

  const loadAlbum = async () => {
    try {
      setIsLoading(true)
      setError(null)
      const response = await albumsAPI.getById(id)
      const albumData = response.data
      setAlbum(albumData)
      setPhotos(albumData.photos || [])
    } catch (err) {
      setError('Failed to load album. Please try again.')
      console.error('Error loading album:', err)
    } finally {
      setIsLoading(false)
    }
  }

  const handleUpload = async (files) => {
    try {
      setIsUploading(true)
      setError(null)
      setUploadProgress({ uploaded: 0, total: files.length })

      const formData = new FormData()
      files.forEach(file => {
        formData.append('files', file)
      })

      const response = await photosAPI.upload(id, formData)
      const result = response.data

      setUploadProgress({
        uploaded: result.uploaded,
        total: files.length,
        failed: result.failed
      })

      // Reload album to get updated photos
      await loadAlbum()

      // Clear progress after a delay
      setTimeout(() => {
        setUploadProgress(null)
      }, 3000)

    } catch (err) {
      setError(err.response?.data?.error || 'Failed to upload photos. Please try again.')
      console.error('Error uploading photos:', err)
      setUploadProgress(null)
    } finally {
      setIsUploading(false)
    }
  }

  const handleDeletePhoto = async (photoId) => {
    try {
      setError(null)
      await photosAPI.delete(photoId)
      await loadAlbum() // Reload to remove deleted photo
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to delete photo. Please try again.')
      console.error('Error deleting photo:', err)
    }
  }

  const handleEditAlbum = () => {
    setIsModalOpen(true)
  }

  const handleSubmitAlbum = async (formData) => {
    try {
      setIsSubmitting(true)
      setError(null)
      await albumsAPI.update(album.id, formData)
      await loadAlbum() // Reload to get updated data
      setIsModalOpen(false)
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to update album. Please try again.')
      console.error('Error updating album:', err)
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleCloseModal = () => {
    if (!isSubmitting) {
      setIsModalOpen(false)
      setError(null)
    }
  }

  if (isLoading) {
    return (
      <div className="container">
        <div className="loading">
          <div className="spinner"></div>
          Loading album...
        </div>
      </div>
    )
  }

  if (!album) {
    return (
      <div className="container">
        <div className="empty-state">
          <div className="empty-state-icon">❌</div>
          <h3 className="empty-state-title">Album not found</h3>
          <p className="empty-state-text">
            The album you're looking for doesn't exist or has been deleted.
          </p>
          <button
            className="btn btn-primary"
            onClick={() => navigate('/')}
          >
            Back to Albums
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="container">
      <header className="header">
        <div className="header-content">
          <div className="flex items-center gap-4">
            <button
              className="btn btn-secondary"
              onClick={() => navigate('/')}
            >
              ← Back
            </button>
            <div>
              <h1>{album.name}</h1>
              {album.description && (
                <p style={{ color: '#718096', marginTop: '4px' }}>
                  {album.description}
                </p>
              )}
            </div>
          </div>
          <button
            className="btn btn-primary"
            onClick={handleEditAlbum}
          >
            ✏️ Edit
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

      {uploadProgress && (
        <div className="mb-4" style={{ 
          background: '#c6f6d5', 
          color: '#22543d', 
          padding: '12px', 
          borderRadius: '8px',
          textAlign: 'center'
        }}>
          Uploaded {uploadProgress.uploaded} of {uploadProgress.total} photos
          {uploadProgress.failed > 0 && ` (${uploadProgress.failed} failed)`}
        </div>
      )}

      <PhotoUpload
        onUpload={handleUpload}
        isLoading={isUploading}
      />

      <div className="mb-4" style={{ color: '#718096', fontSize: '14px' }}>
        Showing {photos.length} {photos.length === 1 ? 'photo' : 'photos'}
      </div>

      <PhotoGrid
        photos={photos}
        onDelete={handleDeletePhoto}
        isLoading={false}
      />

      <Modal
        isOpen={isModalOpen}
        onClose={handleCloseModal}
        title="Edit Album"
      >
        <AlbumForm
          album={album}
          onSubmit={handleSubmitAlbum}
          onCancel={handleCloseModal}
          isLoading={isSubmitting}
        />
      </Modal>
    </div>
  )
}

export default AlbumDetail

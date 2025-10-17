import React, { useState } from 'react'

const AlbumForm = ({ album, onSubmit, onCancel, isLoading }) => {
  const [formData, setFormData] = useState({
    name: album?.name || '',
    description: album?.description || ''
  })

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    if (formData.name.trim()) {
      onSubmit(formData)
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <div className="form-group">
        <label htmlFor="name" className="form-label">
          Album Name *
        </label>
        <input
          type="text"
          id="name"
          name="name"
          value={formData.name}
          onChange={handleChange}
          className="form-input"
          placeholder="Enter album name"
          required
          disabled={isLoading}
        />
      </div>
      
      <div className="form-group">
        <label htmlFor="description" className="form-label">
          Description
        </label>
        <textarea
          id="description"
          name="description"
          value={formData.description}
          onChange={handleChange}
          className="form-input form-textarea"
          placeholder="Enter album description (optional)"
          disabled={isLoading}
        />
      </div>
      
      <div className="modal-footer">
        <button
          type="button"
          onClick={onCancel}
          className="btn btn-secondary"
          disabled={isLoading}
        >
          Cancel
        </button>
        <button
          type="submit"
          className="btn btn-primary"
          disabled={isLoading || !formData.name.trim()}
        >
          {isLoading ? (
            <>
              <div className="spinner"></div>
              {album ? 'Updating...' : 'Creating...'}
            </>
          ) : (
            album ? 'Update Album' : 'Create Album'
          )}
        </button>
      </div>
    </form>
  )
}

export default AlbumForm

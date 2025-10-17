import React, { useState, useRef } from 'react'

const PhotoUpload = ({ onUpload, isLoading }) => {
  const [isDragOver, setIsDragOver] = useState(false)
  const fileInputRef = useRef(null)

  const handleDragOver = (e) => {
    e.preventDefault()
    setIsDragOver(true)
  }

  const handleDragLeave = (e) => {
    e.preventDefault()
    setIsDragOver(false)
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setIsDragOver(false)
    
    const files = Array.from(e.dataTransfer.files)
    if (files.length > 0) {
      handleFiles(files)
    }
  }

  const handleFileSelect = (e) => {
    const files = Array.from(e.target.files)
    if (files.length > 0) {
      handleFiles(files)
    }
  }

  const handleFiles = (files) => {
    // Filter for image files
    const imageFiles = files.filter(file => 
      file.type.startsWith('image/') && 
      ['image/jpeg', 'image/jpg', 'image/png', 'image/heic', 'image/heif'].includes(file.type)
    )

    if (imageFiles.length === 0) {
      alert('Please select valid image files (JPEG, PNG, HEIC)')
      return
    }

    if (imageFiles.length !== files.length) {
      alert(`Selected ${imageFiles.length} valid images out of ${files.length} files`)
    }

    onUpload(imageFiles)
  }

  const handleClick = () => {
    fileInputRef.current?.click()
  }

  return (
    <div className="mb-6">
      <div
        className={`upload-area ${isDragOver ? 'dragover' : ''}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={handleClick}
      >
        <div className="upload-icon">📤</div>
        <div className="upload-text">
          {isLoading ? 'Uploading photos...' : 'Drop photos here or click to select'}
        </div>
        <div className="upload-hint">
          Supports JPEG, PNG, and HEIC formats
        </div>
      </div>
      
      <input
        ref={fileInputRef}
        type="file"
        multiple
        accept="image/jpeg,image/jpg,image/png,image/heic,image/heif"
        onChange={handleFileSelect}
        style={{ display: 'none' }}
        disabled={isLoading}
      />
    </div>
  )
}

export default PhotoUpload

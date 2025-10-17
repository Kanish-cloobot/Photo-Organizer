import axios from 'axios'

const API_BASE_URL = '/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Albums API
export const albumsAPI = {
  // Get all albums
  getAll: () => api.get('/albums'),
  
  // Get album by ID with photos
  getById: (id) => api.get(`/albums/${id}`),
  
  // Create new album
  create: (data) => api.post('/albums', data),
  
  // Update album
  update: (id, data) => api.put(`/albums/${id}`, data),
  
  // Delete album
  delete: (id) => api.delete(`/albums/${id}`),
}

// Photos API
export const photosAPI = {
  // Get photos in album
  getByAlbum: (albumId) => api.get(`/albums/${albumId}/photos`),
  
  // Upload photos to album
  upload: (albumId, formData) => api.post(`/albums/${albumId}/photos`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  }),
  
  // Delete photo
  delete: (id) => api.delete(`/photos/${id}`),
  
  // Download original photo
  download: (id) => api.get(`/photos/${id}/download`, {
    responseType: 'blob',
  }),
  
  // View compressed photo
  view: (id) => api.get(`/photos/${id}/view`, {
    responseType: 'blob',
  }),
}

// Health check
export const healthCheck = () => api.get('/health')

export default api

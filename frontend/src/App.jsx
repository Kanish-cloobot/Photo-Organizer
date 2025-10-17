import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Albums from './pages/Albums'
import AlbumDetail from './pages/AlbumDetail'

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Albums />} />
          <Route path="/album/:id" element={<AlbumDetail />} />
        </Routes>
      </div>
    </Router>
  )
}

export default App

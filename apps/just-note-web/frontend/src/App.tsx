import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import HomePage from './pages/Home'
import NotesPage from './pages/Notes'
import DiaryPage from './pages/Diary'
import StatsPage from './pages/Stats'
import NoteDetailPage from './pages/NoteDetail'

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-bg-secondary">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/notes" element={<NotesPage />} />
          <Route path="/notes/:id" element={<NoteDetailPage />} />
          <Route path="/diary" element={<DiaryPage />} />
          <Route path="/diary/:date" element={<DiaryPage />} />
          <Route path="/stats" element={<StatsPage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </div>
    </BrowserRouter>
  )
}

export default App

import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useNoteStore } from '@/stores/noteStore'
import { NOTE_TYPES, type NoteType } from '@/types'
import NoteCard from '@/components/NoteCard'

export default function NotesPage() {
  const navigate = useNavigate()
  const { filteredNotes, setFilter, filter } = useNoteStore()
  const [searchQuery, setSearchQuery] = useState('')

  const handleSearch = (value: string) => {
    setSearchQuery(value)
    setFilter({ search: value })
  }

  const handleTypeFilter = (type: NoteType | 'all') => {
    setFilter({ type })
  }

  return (
    <div className="max-w-2xl mx-auto px-4 py-6 pb-24">
      {/* Header */}
      <header className="flex items-center justify-between mb-6">
        <button
          onClick={() => navigate('/')}
          className="p-2 hover:bg-bg-secondary rounded-full transition-colors"
        >
          ←
        </button>
        <h1 className="text-xl font-bold text-text-primary">全部记录</h1>
        <div className="w-10" />
      </header>

      {/* Search */}
      <div className="mb-4">
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => handleSearch(e.target.value)}
          placeholder="搜索笔记..."
          className="input-base"
        />
      </div>

      {/* Type Filter */}
      <div className="flex gap-2 overflow-x-auto pb-2 mb-4 scrollbar-hide">
        <button
          onClick={() => handleTypeFilter('all')}
          className={`px-3 py-1.5 rounded-full text-sm whitespace-nowrap transition-colors ${
            filter.type === 'all'
              ? 'bg-primary text-white'
              : 'bg-white text-text-secondary hover:bg-bg-secondary'
          }`}
        >
          全部
        </button>
        {NOTE_TYPES.map((type) => (
          <button
            key={type.id}
            onClick={() => handleTypeFilter(type.id)}
            className={`px-3 py-1.5 rounded-full text-sm whitespace-nowrap transition-colors ${
              filter.type === type.id
                ? 'bg-primary text-white'
                : 'bg-white text-text-secondary hover:bg-bg-secondary'
            }`}
          >
            {type.icon} {type.name}
          </button>
        ))}
      </div>

      {/* Notes List */}
      <div className="space-y-3">
        {filteredNotes.length > 0 ? (
          filteredNotes.map((note) => (
            <NoteCard
              key={note.id}
              note={note}
              onClick={() => navigate(`/notes/${note.id}`)}
            />
          ))
        ) : (
          <div className="text-center py-12 text-text-weak">
            <div className="text-4xl mb-4">🔍</div>
            <p>没有找到笔记</p>
          </div>
        )}
      </div>
    </div>
  )
}

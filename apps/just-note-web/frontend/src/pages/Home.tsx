import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useNoteStore } from '@/stores/noteStore'
import { NOTE_TYPES, type NoteType } from '@/types'
import NoteCard from '@/components/NoteCard'
import { format } from 'date-fns'
import { zhCN } from 'date-fns/locale'

export default function HomePage() {
  const navigate = useNavigate()
  const { filteredNotes, createNote, loading } = useNoteStore()
  const [content, setContent] = useState('')
  const [selectedType, setSelectedType] = useState<NoteType>('other')
  const [showTypeSelector, setShowTypeSelector] = useState(false)

  const handleSubmit = async () => {
    if (!content.trim()) return
    
    try {
      await createNote({
        type: selectedType,
        title: content.slice(0, 50),
        content: content.trim(),
        tags: [],
        dayId: format(new Date(), 'yyyy-MM-dd'),
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      })
      setContent('')
      setShowTypeSelector(false)
    } catch (error) {
      console.error('Failed to create note:', error)
    }
  }

  const recentNotes = filteredNotes.slice(0, 10)

  return (
    <div className="max-w-2xl mx-auto px-4 py-6 pb-24">
      {/* Header */}
      <header className="flex items-center justify-between mb-8">
        <h1 className="text-2xl font-bold text-text-primary">记一下</h1>
        <div className="flex items-center gap-4">
          <button 
            onClick={() => navigate('/stats')}
            className="p-2 hover:bg-bg-secondary rounded-full transition-colors"
          >
            📊
          </button>
          <div className="w-8 h-8 bg-primary rounded-full flex items-center justify-center text-white font-medium">
            U
          </div>
        </div>
      </header>

      {/* Quick Input */}
      <div className="mb-8">
        <div 
          className="bg-white rounded-lg shadow-md p-4 focus-within:ring-2 focus-within:ring-primary transition-all"
          onClick={() => setShowTypeSelector(true)}
        >
          <textarea
            value={content}
            onChange={(e) => setContent(e.target.value)}
            placeholder="💡 今天有什么想记录的？"
            className="w-full resize-none focus:outline-none text-text-primary placeholder-text-weak"
            rows={3}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault()
                handleSubmit()
              }
            }}
          />
          
          {showTypeSelector && (
            <div className="mt-4 pt-4 border-t border-border">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm text-text-secondary">选择类型</span>
                <button
                  onClick={() => setShowTypeSelector(false)}
                  className="text-sm text-text-weak hover:text-text-secondary"
                >
                  取消
                </button>
              </div>
              <div className="grid grid-cols-5 gap-2">
                {NOTE_TYPES.map((type) => (
                  <button
                    key={type.id}
                    onClick={() => {
                      setSelectedType(type.id)
                      setShowTypeSelector(false)
                    }}
                    className={`p-2 rounded-md text-center transition-all ${
                      selectedType === type.id
                        ? 'ring-2 ring-primary'
                        : 'hover:bg-bg-secondary'
                    }`}
                    style={{ backgroundColor: type.bgColor }}
                  >
                    <div className="text-xl mb-1">{type.icon}</div>
                    <div className="text-xs text-text-primary">{type.name}</div>
                  </button>
                ))}
              </div>
            </div>
          )}
          
          <div className="flex items-center justify-between mt-4">
            <div className="flex items-center gap-2">
              {selectedType !== 'other' && (
                <span 
                  className="px-2 py-1 rounded text-sm"
                  style={{ 
                    backgroundColor: NOTE_TYPES.find(t => t.id === selectedType)?.bgColor,
                    color: NOTE_TYPES.find(t => t.id === selectedType)?.color
                  }}
                >
                  {NOTE_TYPES.find(t => t.id === selectedType)?.icon}
                  {NOTE_TYPES.find(t => t.id === selectedType)?.name}
                </span>
              )}
            </div>
            <button
              onClick={handleSubmit}
              disabled={!content.trim() || loading}
              className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? '保存中...' : '记录'}
            </button>
          </div>
        </div>
      </div>

      {/* Recent Notes */}
      <div>
        <h2 className="text-lg font-semibold text-text-primary mb-4">最近记录</h2>
        {recentNotes.length > 0 ? (
          <div className="space-y-3">
            {recentNotes.map((note) => (
              <NoteCard
                key={note.id}
                note={note}
                onClick={() => navigate(`/notes/${note.id}`)}
              />
            ))}
          </div>
        ) : (
          <div className="text-center py-12 text-text-weak">
            <div className="text-4xl mb-4">📝</div>
            <p>还没有记录</p>
            <p className="text-sm mt-2">在上方输入框记录你的第一个想法吧！</p>
          </div>
        )}
      </div>
    </div>
  )
}

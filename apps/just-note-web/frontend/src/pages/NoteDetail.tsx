import { useParams, useNavigate } from 'react-router-dom'
import { useNoteStore } from '@/stores/noteStore'
import { NOTE_TYPES } from '@/types'
import { format } from 'date-fns'
import { useState } from 'react'

export default function NoteDetailPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { notes, updateNote, deleteNote } = useNoteStore()
  const [isEditing, setIsEditing] = useState(false)
  const [editContent, setEditContent] = useState('')

  const note = notes.find(n => n.id === id)

  if (!note) {
    return (
      <div className="min-h-screen flex items-center justify-center text-text-weak">
        笔记不存在
      </div>
    )
  }

  const typeConfig = NOTE_TYPES.find(t => t.id === note.type)

  const handleDelete = () => {
    if (confirm('确定要删除这条笔记吗？')) {
      deleteNote(note.id)
      navigate('/')
    }
  }

  const handleSave = () => {
    updateNote(note.id, {
      content: editContent,
      title: editContent.slice(0, 50),
    })
    setIsEditing(false)
  }

  return (
    <div className="max-w-2xl mx-auto px-4 py-6 pb-24">
      {/* Header */}
      <header className="flex items-center justify-between mb-6">
        <button
          onClick={() => navigate(-1)}
          className="p-2 hover:bg-bg-secondary rounded-full transition-colors"
        >
          ←
        </button>
        <div className="flex items-center gap-2">
          {isEditing ? (
            <>
              <button
                onClick={handleSave}
                className="btn-primary text-sm py-1.5"
              >
                保存
              </button>
              <button
                onClick={() => setIsEditing(false)}
                className="px-3 py-1.5 text-sm text-text-secondary hover:bg-bg-secondary rounded-md"
              >
                取消
              </button>
            </>
          ) : (
            <>
              <button
                onClick={() => {
                  setEditContent(note.content)
                  setIsEditing(true)
                }}
                className="px-3 py-1.5 text-sm text-text-secondary hover:bg-bg-secondary rounded-md"
              >
                编辑
              </button>
              <button
                onClick={handleDelete}
                className="px-3 py-1.5 text-sm text-danger hover:bg-bg-secondary rounded-md"
              >
                删除
              </button>
            </>
          )}
        </div>
      </header>

      {/* Content */}
      <article className="bg-white rounded-lg shadow-md p-6">
        {/* Type Badge */}
        <div className="flex items-center gap-2 mb-4">
          <span className="text-2xl">{typeConfig?.icon}</span>
          <span 
            className="text-sm font-medium px-3 py-1 rounded-full"
            style={{ 
              backgroundColor: typeConfig?.bgColor,
              color: typeConfig?.color
            }}
          >
            {typeConfig?.name}
          </span>
        </div>

        {/* Title */}
        <h1 className="text-2xl font-bold text-text-primary mb-4">
          {note.title}
        </h1>

        {/* Content */}
        {isEditing ? (
          <textarea
            value={editContent}
            onChange={(e) => setEditContent(e.target.value)}
            className="w-full h-64 p-4 border border-border rounded-md focus:outline-none focus:ring-2 focus:ring-primary resize-none"
          />
        ) : (
          <div className="prose max-w-none text-text-primary">
            <p className="whitespace-pre-wrap">{note.content}</p>
          </div>
        )}

        {/* Meta */}
        <div className="mt-6 pt-6 border-t border-border">
          <div className="text-sm text-text-weak">
            <div>创建于：{format(new Date(note.createdAt), 'yyyy-MM-dd HH:mm', { locale: zhCN })}</div>
            <div>更新于：{format(new Date(note.updatedAt), 'yyyy-MM-dd HH:mm', { locale: zhCN })}</div>
          </div>
          
          {note.tags.length > 0 && (
            <div className="flex flex-wrap gap-2 mt-4">
              {note.tags.map((tag, index) => (
                <span
                  key={index}
                  className="text-sm text-text-secondary bg-bg-secondary px-3 py-1 rounded-full"
                >
                  #{tag}
                </span>
              ))}
            </div>
          )}
        </div>
      </article>
    </div>
  )
}

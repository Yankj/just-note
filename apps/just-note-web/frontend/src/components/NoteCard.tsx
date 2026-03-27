import { format } from 'date-fns'
import { zhCN } from 'date-fns/locale'
import type { Note } from '@/types'
import { NOTE_TYPES } from '@/types'
import { clsx } from 'clsx'

interface NoteCardProps {
  note: Note
  onClick?: () => void
}

export default function NoteCard({ note, onClick }: NoteCardProps) {
  const typeConfig = NOTE_TYPES.find(t => t.id === note.type)
  
  const formatTime = (dateString: string) => {
    const date = new Date(dateString)
    const now = new Date()
    const diff = now.getTime() - date.getTime()
    const minutes = Math.floor(diff / 60000)
    const hours = Math.floor(diff / 3600000)
    const days = Math.floor(diff / 86400000)
    
    if (minutes < 1) return '刚刚'
    if (minutes < 60) return `${minutes}分钟前`
    if (hours < 24) return `${hours}小时前`
    if (days < 7) return `${days}天前`
    return format(date, 'MM-dd HH:mm', { locale: zhCN })
  }

  return (
    <div
      onClick={onClick}
      className={clsx(
        'note-card',
        'hover:scale-[1.02] active:scale-[0.98]'
      )}
      style={{
        borderLeft: `4px solid ${typeConfig?.color}`,
      }}
    >
      <div className="flex items-start justify-between mb-2">
        <div className="flex items-center gap-2">
          <span className="text-xl">{typeConfig?.icon}</span>
          <span 
            className="text-sm font-medium px-2 py-0.5 rounded"
            style={{ 
              backgroundColor: typeConfig?.bgColor,
              color: typeConfig?.color
            }}
          >
            {typeConfig?.name}
          </span>
        </div>
        <span className="text-xs text-text-weak">
          {formatTime(note.createdAt)}
        </span>
      </div>
      
      <h3 className="text-text-primary font-medium mb-1 line-clamp-1">
        {note.title}
      </h3>
      
      <p className="text-text-secondary text-sm line-clamp-2 mb-3">
        {note.content}
      </p>
      
      {note.tags.length > 0 && (
        <div className="flex flex-wrap gap-1.5">
          {note.tags.slice(0, 3).map((tag, index) => (
            <span
              key={index}
              className="text-xs text-text-weak bg-bg-secondary px-2 py-0.5 rounded"
            >
              #{tag}
            </span>
          ))}
        </div>
      )}
      
      {note.amount && (
        <div className="mt-2 text-sm font-medium" style={{ color: typeConfig?.color }}>
          {note.type === 'expense' ? '-' : '+'}¥{note.amount}
        </div>
      )}
    </div>
  )
}

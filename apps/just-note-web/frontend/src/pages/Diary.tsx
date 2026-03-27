import { useParams, useNavigate } from 'react-router-dom'
import { useNoteStore } from '@/stores/noteStore'
import { NOTE_TYPES } from '@/types'
import { format, parseISO } from 'date-fns'
import { zhCN } from 'date-fns/locale'

export default function DiaryPage() {
  const { date } = useParams<{ date: string }>()
  const navigate = useNavigate()
  const { notes } = useNoteStore()

  const selectedDate = date ? parseISO(date) : new Date()
  const dayId = format(selectedDate, 'yyyy-MM-dd')
  
  const dayNotes = notes.filter(note => note.dayId === dayId)
  
  // Group by hour
  const notesByHour = dayNotes.reduce((acc, note) => {
    const hour = format(parseISO(note.createdAt), 'HH:00')
    if (!acc[hour]) acc[hour] = []
    acc[hour].push(note)
    return acc
  }, {} as Record<string, typeof dayNotes>)

  const hours = Object.keys(notesByHour).sort()

  const changeDate = (days: number) => {
    const newDate = new Date(selectedDate)
    newDate.setDate(newDate.getDate() + days)
    navigate(`/diary/${format(newDate, 'yyyy-MM-dd')}`)
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
        <div className="flex items-center gap-4">
          <button
            onClick={() => changeDate(-1)}
            className="p-2 hover:bg-bg-secondary rounded-full"
          >
            ‹
          </button>
          <h1 className="text-xl font-bold text-text-primary">
            {format(selectedDate, 'yyyy 年 M 月 d 日', { locale: zhCN })}
          </h1>
          <button
            onClick={() => changeDate(1)}
            className="p-2 hover:bg-bg-secondary rounded-full"
          >
            ›
          </button>
        </div>
        <div className="w-10" />
      </header>

      {/* Overview */}
      <div className="bg-white rounded-lg shadow-md p-4 mb-6">
        <h2 className="text-sm font-medium text-text-secondary mb-2">今日概览</h2>
        <div className="text-2xl font-bold text-text-primary mb-2">
          共 {dayNotes.length} 条记录
        </div>
        <div className="flex flex-wrap gap-2">
          {NOTE_TYPES.map(type => {
            const count = dayNotes.filter(n => n.type === type.id).length
            if (count === 0) return null
            return (
              <div
                key={type.id}
                className="flex items-center gap-1 px-2 py-1 rounded text-sm"
                style={{ backgroundColor: type.bgColor }}
              >
                <span>{type.icon}</span>
                <span className="text-text-primary">{count}</span>
              </div>
            )
          })}
        </div>
      </div>

      {/* Timeline */}
      <div>
        <h2 className="text-lg font-semibold text-text-primary mb-4">时间线</h2>
        
        {hours.length > 0 ? (
          <div className="space-y-6">
            {hours.map(hour => (
              <div key={hour}>
                <div className="flex items-center gap-3 mb-3">
                  <div className="text-sm font-medium text-text-secondary">
                    🕐 {hour}
                  </div>
                  <div className="flex-1 h-px bg-border" />
                </div>
                <div className="space-y-3">
                  {notesByHour[hour].map(note => {
                    const typeConfig = NOTE_TYPES.find(t => t.id === note.type)
                    return (
                      <div
                        key={note.id}
                        onClick={() => navigate(`/notes/${note.id}`)}
                        className="bg-white rounded-lg shadow-sm p-4 cursor-pointer hover:shadow-md transition-shadow"
                      >
                        <div className="flex items-center gap-2 mb-2">
                          <span className="text-lg">{typeConfig?.icon}</span>
                          <span 
                            className="text-xs px-2 py-0.5 rounded"
                            style={{ 
                              backgroundColor: typeConfig?.bgColor,
                              color: typeConfig?.color
                            }}
                          >
                            {typeConfig?.name}
                          </span>
                          <span className="text-xs text-text-weak ml-auto">
                            {format(parseISO(note.createdAt), 'HH:mm')}
                          </span>
                        </div>
                        <p className="text-text-primary text-sm line-clamp-2">
                          {note.content}
                        </p>
                      </div>
                    )
                  })}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-12 text-text-weak">
            <div className="text-4xl mb-4">📅</div>
            <p>今日暂无记录</p>
          </div>
        )}
      </div>
    </div>
  )
}

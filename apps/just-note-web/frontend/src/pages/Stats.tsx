import { useNavigate } from 'react-router-dom'
import { useNoteStore } from '@/stores/noteStore'
import { NOTE_TYPES } from '@/types'
import { format } from 'date-fns'
import { zhCN } from 'date-fns/locale'

export default function StatsPage() {
  const navigate = useNavigate()
  const { notes } = useNoteStore()

  const total = notes.length
  
  const byType = NOTE_TYPES.map(type => ({
    ...type,
    count: notes.filter(n => n.type === type.id).length,
  })).filter(t => t.count > 0)

  // Calculate streak
  const uniqueDays = new Set(notes.map(n => n.dayId))
  const sortedDays = Array.from(uniqueDays).sort().reverse()
  
  let streak = 0
  const today = format(new Date(), 'yyyy-MM-dd')
  let currentDate = new Date()
  
  for (const day of sortedDays) {
    const expectedDate = format(currentDate, 'yyyy-MM-dd')
    if (day === expectedDate) {
      streak++
      currentDate.setDate(currentDate.getDate() - 1)
    } else {
      break
    }
  }

  // This week
  const weekAgo = new Date()
  weekAgo.setDate(weekAgo.getDate() - 7)
  const weekNotes = notes.filter(n => new Date(n.createdAt) >= weekAgo)

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
        <h1 className="text-xl font-bold text-text-primary">数据统计</h1>
        <div className="w-10" />
      </header>

      {/* Overview */}
      <div className="grid grid-cols-2 gap-4 mb-6">
        <div className="bg-white rounded-lg shadow-md p-4">
          <div className="text-sm text-text-secondary mb-1">总记录</div>
          <div className="text-3xl font-bold text-text-primary">{total}</div>
        </div>
        <div className="bg-white rounded-lg shadow-md p-4">
          <div className="text-sm text-text-secondary mb-1">连续记录</div>
          <div className="text-3xl font-bold text-text-primary">{streak}天</div>
        </div>
      </div>

      {/* This Week */}
      <div className="bg-white rounded-lg shadow-md p-4 mb-6">
        <h2 className="text-sm font-medium text-text-secondary mb-3">本周</h2>
        <div className="text-2xl font-bold text-text-primary mb-1">
          {weekNotes.length} 条记录
        </div>
        <div className="text-sm text-text-weak">
          平均每天 {(weekNotes.length / 7).toFixed(1)} 条
        </div>
      </div>

      {/* Type Distribution */}
      <div className="bg-white rounded-lg shadow-md p-4 mb-6">
        <h2 className="text-sm font-medium text-text-secondary mb-3">类型分布</h2>
        <div className="space-y-3">
          {byType.map(type => (
            <div key={type.id}>
              <div className="flex items-center justify-between mb-1">
                <div className="flex items-center gap-2">
                  <span className="text-lg">{type.icon}</span>
                  <span className="text-sm text-text-primary">{type.name}</span>
                </div>
                <span className="text-sm font-medium text-text-primary">
                  {type.count}
                </span>
              </div>
              <div className="h-2 bg-bg-secondary rounded-full overflow-hidden">
                <div
                  className="h-full rounded-full transition-all"
                  style={{
                    width: `${(type.count / total) * 100}%`,
                    backgroundColor: type.color,
                  }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Recent Activity */}
      <div className="bg-white rounded-lg shadow-md p-4">
        <h2 className="text-sm font-medium text-text-secondary mb-3">最近活动</h2>
        {notes.slice(0, 5).map((note, index) => (
          <div
            key={note.id}
            className={`flex items-center gap-3 py-2 ${
              index < notes.slice(0, 5).length - 1 ? 'border-b border-border' : ''
            }`}
          >
            <span className="text-lg">
              {NOTE_TYPES.find(t => t.id === note.type)?.icon}
            </span>
            <div className="flex-1 min-w-0">
              <div className="text-sm text-text-primary truncate">
                {note.title}
              </div>
              <div className="text-xs text-text-weak">
                {format(new Date(note.createdAt), 'MM-dd HH:mm', { locale: zhCN })}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

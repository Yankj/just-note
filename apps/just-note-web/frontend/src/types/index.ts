export type NoteType = 
  | 'inspiration'
  | 'idea'
  | 'knowledge'
  | 'expense'
  | 'income'
  | 'diary'
  | 'task'
  | 'quote'
  | 'other';

export interface Note {
  id: string;
  type: NoteType;
  title: string;
  content: string;
  tags: string[];
  amount?: number;
  currency?: string;
  createdAt: string;
  updatedAt: string;
  dayId: string;
  relatedIds?: string[];
  aiSummary?: string;
}

export interface NoteTypeConfig {
  id: NoteType;
  name: string;
  icon: string;
  color: string;
  bgColor: string;
}

export const NOTE_TYPES: NoteTypeConfig[] = [
  { id: 'inspiration', name: '灵感', icon: '💡', color: '#F59E0B', bgColor: '#FEF3C7' },
  { id: 'idea', name: '想法', icon: '✨', color: '#8B5CF6', bgColor: '#F3E8FF' },
  { id: 'knowledge', name: '知识', icon: '📚', color: '#3B82F6', bgColor: '#DBEAFE' },
  { id: 'expense', name: '支出', icon: '💸', color: '#EF4444', bgColor: '#FEE2E2' },
  { id: 'income', name: '收入', icon: '💰', color: '#10B981', bgColor: '#D1FAE5' },
  { id: 'diary', name: '日记', icon: '📝', color: '#6B7280', bgColor: '#F3F4F6' },
  { id: 'task', name: '任务', icon: '✅', color: '#10B981', bgColor: '#DCFCE7' },
  { id: 'quote', name: '引用', icon: '💬', color: '#EC4899', bgColor: '#FCE7F3' },
  { id: 'other', name: '其他', icon: '📌', color: '#9CA3AF', bgColor: '#F3F4F6' },
];

export interface NoteStats {
  total: number;
  byType: Record<NoteType, number>;
  byDay: Record<string, number>;
  streak: number;
}

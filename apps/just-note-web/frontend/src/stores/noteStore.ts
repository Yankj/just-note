import { create } from 'zustand';
import type { Note, NoteType, NoteStats } from '@/types';

interface NoteState {
  notes: Note[];
  filteredNotes: Note[];
  filter: {
    type: NoteType | 'all';
    search: string;
    date: string | null;
  };
  stats: NoteStats | null;
  loading: boolean;
  error: string | null;
  
  // Actions
  setNotes: (notes: Note[]) => void;
  addNote: (note: Note) => void;
  updateNote: (id: string, updates: Partial<Note>) => void;
  deleteNote: (id: string) => void;
  setFilter: (filter: Partial<NoteState['filter']>) => void;
  fetchNotes: () => Promise<void>;
  createNote: (data: Omit<Note, 'id' | 'createdAt' | 'updatedAt'>) => Promise<void>;
}

export const useNoteStore = create<NoteState>((set, get) => ({
  notes: [],
  filteredNotes: [],
  filter: {
    type: 'all',
    search: '',
    date: null,
  },
  stats: null,
  loading: false,
  error: null,

  setNotes: (notes) => {
    set({ notes });
    applyFilters(notes, get().filter);
  },

  addNote: (note) => {
    const notes = [note, ...get().notes];
    set({ notes });
    applyFilters(notes, get().filter);
  },

  updateNote: (id, updates) => {
    const notes = get().notes.map(note => 
      note.id === id ? { ...note, ...updates, updatedAt: new Date().toISOString() } : note
    );
    set({ notes });
    applyFilters(notes, get().filter);
  },

  deleteNote: (id) => {
    const notes = get().notes.filter(note => note.id !== id);
    set({ notes });
    applyFilters(notes, get().filter);
  },

  setFilter: (filter) => {
    const newFilter = { ...get().filter, ...filter };
    set({ filter: newFilter });
    applyFilters(get().notes, newFilter);
  },

  fetchNotes: async () => {
    set({ loading: true, error: null });
    try {
      // TODO: Replace with actual API call
      const response = await fetch('/api/notes');
      const notes = await response.json();
      set({ notes, loading: false });
      applyFilters(notes, get().filter);
    } catch (error) {
      set({ error: 'Failed to fetch notes', loading: false });
    }
  },

  createNote: async (data) => {
    set({ loading: true, error: null });
    try {
      // TODO: Replace with actual API call
      const response = await fetch('/api/notes', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });
      const note = await response.json();
      get().addNote(note);
      set({ loading: false });
    } catch (error) {
      set({ error: 'Failed to create note', loading: false });
      throw error;
    }
  },
}));

function applyFilters(notes: Note[], filter: NoteState['filter']) {
  let filtered = [...notes];
  
  if (filter.type !== 'all') {
    filtered = filtered.filter(note => note.type === filter.type);
  }
  
  if (filter.search) {
    const search = filter.search.toLowerCase();
    filtered = filtered.filter(note =>
      note.title.toLowerCase().includes(search) ||
      note.content.toLowerCase().includes(search) ||
      note.tags.some(tag => tag.toLowerCase().includes(search))
    );
  }
  
  if (filter.date) {
    filtered = filtered.filter(note => note.dayId === filter.date);
  }
  
  // Sort by creation date (newest first)
  filtered.sort((a, b) => 
    new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
  );
  
  set({ filteredNotes: filtered });
}

/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#1E40AF',
          light: '#3B82F6',
        },
        accent: '#F97316',
        success: '#10B981',
        warning: '#F59E0B',
        danger: '#EF4444',
        note: {
          inspiration: { bg: '#FEF3C7', icon: '#F59E0B' },
          idea: { bg: '#F3E8FF', icon: '#8B5CF6' },
          knowledge: { bg: '#DBEAFE', icon: '#3B82F6' },
          expense: { bg: '#FEE2E2', icon: '#EF4444' },
          income: { bg: '#D1FAE5', icon: '#10B981' },
          diary: { bg: '#F3F4F6', icon: '#6B7280' },
          task: { bg: '#DCFCE7', icon: '#10B981' },
          quote: { bg: '#FCE7F3', icon: '#EC4899' },
          other: { bg: '#F3F4F6', icon: '#9CA3AF' },
        }
      },
    },
  },
  plugins: [],
}

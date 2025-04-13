import { createTheme, alpha } from '@mui/material/styles';

export const getTheme = (mode) => createTheme({
  palette: {
    mode,
    primary: {
      main: mode === 'dark' ? '#8B5CF6' : '#6D28D9', // Vibrant purple
      light: '#A78BFA',
      dark: '#5B21B6',
    },
    secondary: {
      main: mode === 'dark' ? '#EC4899' : '#DB2777', // Vibrant pink
      light: '#F472B6',
      dark: '#BE185D',
    },
    background: {
      default: mode === 'dark' ? '#0F172A' : '#F8FAFC', // Darker blue-gray / Light gray
      paper: mode === 'dark' ? '#1E293B' : '#FFFFFF',
    },
    accent: {
      blue: mode === 'dark' ? '#38BDF8' : '#0EA5E9',
      green: mode === 'dark' ? '#4ADE80' : '#22C55E',
      yellow: mode === 'dark' ? '#FACC15' : '#EAB308',
      orange: mode === 'dark' ? '#FB923C' : '#F97316',
    },
    grey: {
      50: mode === 'dark' ? '#1E293B' : '#F8FAFC',
      100: mode === 'dark' ? '#334155' : '#F1F5F9',
      200: mode === 'dark' ? '#475569' : '#E2E8F0',
      300: mode === 'dark' ? '#64748B' : '#CBD5E1',
      800: mode === 'dark' ? '#1E293B' : '#1E293B',
      900: mode === 'dark' ? '#0F172A' : '#0F172A',
    },
    text: {
      primary: mode === 'dark' ? '#F3F4F6' : '#111827',
      secondary: mode === 'dark' ? '#D1D5DB' : '#4B5563',
    },
  },
  shape: {
    borderRadius: 12,
  },
  spacing: 8,
  components: {
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 12,
          padding: 8,
          transition: 'all 0.2s ease-in-out',
          backgroundImage: mode === 'dark' 
            ? 'linear-gradient(to bottom right, rgba(30, 41, 59, 0.8), rgba(15, 23, 42, 0.8))'
            : 'linear-gradient(to bottom right, rgba(255, 255, 255, 0.8), rgba(241, 245, 249, 0.8))',
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          borderRadius: 8,
          fontWeight: 600,
          transition: 'all 0.2s ease-in-out',
          '&:hover': {
            transform: 'translateY(-1px)',
          },
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          transition: 'all 0.2s ease-in-out',
        },
      },
    },
  },
}); 
import React, { useState, useEffect } from 'react';
import { 
  AppBar, 
  Toolbar, 
  Typography, 
  IconButton, 
  Avatar, 
  Menu, 
  MenuItem, 
  Box,
  ThemeProvider,
  CssBaseline,
  Tooltip,
  Divider
} from '@mui/material';
import {
  Menu as MenuIcon,
  LightMode as LightIcon,
  DarkMode as DarkIcon,
  Person as PersonIcon,
  Settings as SettingsIcon,
  Logout as LogoutIcon
} from '@mui/icons-material';
import { createTheme } from '@mui/material/styles';
import Sidebar from './components/Sidebar';
import MainWorkspace from './components/MainWorkspace';
import './App.css';
import { alpha } from '@mui/material/styles';

function App() {
  const [anchorEl, setAnchorEl] = useState(null);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [isMobile, setIsMobile] = useState(window.innerWidth < 600);
  const [darkMode, setDarkMode] = useState(true);
  const [selectedTab, setSelectedTab] = useState(0);
  const theme = createTheme({
    palette: {
      mode: darkMode ? 'dark' : 'light',
      primary: {
        main: '#3B82F6',
      },
      background: {
        default: darkMode ? '#0F172A' : '#F8FAFC',
        paper: darkMode ? '#1E293B' : '#FFFFFF',
      },
      text: {
        primary: darkMode ? '#F1F5F9' : '#1E293B',
        secondary: darkMode ? '#94A3B8' : '#64748B',
      },
    },
    shape: {
      borderRadius: 8,
    },
  });

  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth < 600);
      if (window.innerWidth < 600) {
        setSidebarOpen(false);
      }
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const handleProfileClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
    handleClose();
  };

  const handleNewChat = () => {
    setSelectedTab(0);
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ display: 'flex' }}>
        <AppBar 
          position="fixed" 
          elevation={0}
          sx={{ 
            zIndex: theme.zIndex.drawer + 1,
            bgcolor: 'background.paper',
            borderBottom: '1px solid',
            borderColor: 'divider',
          }}
        >
          <Toolbar>
            <IconButton
              color="inherit"
              edge="start"
              onClick={() => setSidebarOpen(!sidebarOpen)}
              sx={{ mr: 2, display: { sm: 'none' } }}
            >
              <MenuIcon />
            </IconButton>

            <Typography 
              variant="h6" 
              noWrap 
              component="div"
              sx={{ 
                color: 'text.primary',
                fontWeight: 500,
                fontSize: '1.2rem'
              }}
            >
              AI Tools
            </Typography>

            <Box sx={{ flexGrow: 1 }} />

            <Tooltip title={darkMode ? "Switch to Light Mode" : "Switch to Dark Mode"}>
              <IconButton 
                onClick={toggleDarkMode}
                sx={{ mr: 1 }}
                color="inherit"
              >
                {darkMode ? <LightIcon /> : <DarkIcon />}
              </IconButton>
            </Tooltip>

            <IconButton
              onClick={handleProfileClick}
              size="small"
              sx={{ ml: 1 }}
            >
              <Avatar sx={{ width: 32, height: 32 }}>U</Avatar>
            </IconButton>

            <Menu
              anchorEl={anchorEl}
              open={Boolean(anchorEl)}
              onClose={handleClose}
              onClick={handleClose}
              PaperProps={{
                elevation: 0,
                sx: {
                  overflow: 'visible',
                  filter: 'drop-shadow(0px 2px 8px rgba(0,0,0,0.15))',
                  mt: 1.5,
                  minWidth: 200,
                  '& .MuiMenuItem-root': {
                    px: 2,
                    py: 1,
                    gap: 1.5,
                  },
                },
              }}
              transformOrigin={{ horizontal: 'right', vertical: 'top' }}
              anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }}
            >
              <MenuItem>
                <PersonIcon fontSize="small" />
                <Box>
                  <Typography variant="body1">John Doe</Typography>
                  <Typography variant="caption" color="text.secondary">
                    Admin
                  </Typography>
                </Box>
              </MenuItem>
              <MenuItem>
                <SettingsIcon fontSize="small" />
                Settings
              </MenuItem>
              <MenuItem>
                <LogoutIcon fontSize="small" />
                Logout
              </MenuItem>
            </Menu>
          </Toolbar>
        </AppBar>

        <Sidebar 
          open={sidebarOpen} 
          onClose={() => setSidebarOpen(false)}
          isMobile={isMobile}
          darkMode={darkMode}
          onNewChat={handleNewChat}
        />
        
        <MainWorkspace selectedTab={selectedTab} setSelectedTab={setSelectedTab} />
      </Box>
    </ThemeProvider>
  );
}

export default App;

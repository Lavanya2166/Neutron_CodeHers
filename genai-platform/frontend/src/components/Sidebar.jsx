import React, { useState } from 'react';
import {
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Button,
  Box,
  IconButton,
  styled,
  useTheme
} from '@mui/material';
import {
  Add as AddIcon,
  Chat as ChatIcon,
  Delete as DeleteIcon
} from '@mui/icons-material';

const drawerWidth = 240;

const StyledDrawer = styled(Drawer)(({ theme }) => ({
  width: drawerWidth,
  flexShrink: 0,
  '& .MuiDrawer-paper': {
    width: drawerWidth,
    boxSizing: 'border-box',
    marginTop: '64px',
    height: 'calc(100vh - 64px)',
    border: 'none',
    backgroundColor: theme.palette.background.paper,
    borderRight: `1px solid ${theme.palette.divider}`,
  },
}));

const Sidebar = ({ open, onClose, isMobile, onNewChat }) => {
  const [chats, setChats] = useState([
    { id: 1, title: "Text Generation Chat", timestamp: "2 mins ago" },
    { id: 2, title: "Image Generation", timestamp: "1 hour ago" },
  ]);

  const addNewChat = () => {
    const newChat = {
      id: Date.now(),
      title: `New Chat ${chats.length + 1}`,
      timestamp: "Just now"
    };
    setChats([newChat, ...chats]);
    if (onNewChat) onNewChat();
  };

  const deleteChat = (chatId) => {
    setChats(chats.filter(chat => chat.id !== chatId));
  };

  return (
    <StyledDrawer
      variant={isMobile ? "temporary" : "permanent"}
      open={open}
      onClose={onClose}
    >
      <Box sx={{ p: 2 }}>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          fullWidth
          onClick={addNewChat}
          sx={{ 
            mb: 2,
            bgcolor: 'primary.main',
            textTransform: 'none',
            fontSize: '0.9rem',
            '&:hover': {
              bgcolor: 'primary.dark',
            }
          }}
        >
          New Chat
        </Button>
      </Box>

      <List sx={{ px: 1 }}>
        {chats.map((chat) => (
          <ListItem 
            key={chat.id}
            sx={{
              borderRadius: 1,
              mb: 0.5,
              '&:hover': {
                bgcolor: 'action.hover',
              }
            }}
          >
            <ListItemIcon sx={{ minWidth: 40 }}>
              <ChatIcon fontSize="small" />
            </ListItemIcon>
            <ListItemText 
              primary={chat.title}
              secondary={chat.timestamp}
              primaryTypographyProps={{ 
                fontSize: '0.85rem',
                fontWeight: 500 
              }}
              secondaryTypographyProps={{ 
                fontSize: '0.75rem' 
              }}
            />
            <IconButton 
              size="small" 
              onClick={() => deleteChat(chat.id)}
              sx={{ opacity: 0.7 }}
            >
              <DeleteIcon fontSize="small" />
            </IconButton>
          </ListItem>
        ))}
      </List>
    </StyledDrawer>
  );
};

export default Sidebar; 
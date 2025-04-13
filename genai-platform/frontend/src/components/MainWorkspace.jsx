import React, { useState } from 'react';
import {
  Box,
  Paper,
  Tabs,
  Tab,
  TextField,
  Button,
  Card,
  CardContent,
  Typography,
  styled,
  Checkbox,
  FormControlLabel,
  Input,
  IconButton,
  MenuItem,
  useTheme
} from '@mui/material';
import {
  Send as SendIcon,
  Image as ImageIcon,
  TextFields as TextIcon,
  Article as BlogIcon,
  Campaign as SocialIcon,
  Subtitles as CaptionsIcon,
  CloudUpload as UploadIcon,
  Download as DownloadIcon
} from '@mui/icons-material';
import { alpha } from '@mui/material/styles';

const WorkspaceContainer = styled(Box)(({ theme }) => ({
  flexGrow: 1,
  padding: theme.spacing(1),
  paddingLeft: 4,
  marginTop: '64px',
  marginLeft: '240px',
  backgroundColor: theme.palette.mode === 'dark' 
    ? alpha(theme.palette.background.default, 0.95)
    : alpha(theme.palette.background.paper, 0.95),
  minHeight: 'calc(100vh - 64px)',
  transition: 'margin-left 0.3s ease',
  overflowX: 'hidden',
  [theme.breakpoints.down('sm')]: {
    marginLeft: 0,
    padding: theme.spacing(0.5),
  },
}));

const VisuallyHiddenInput = styled('input')({
  clip: 'rect(0 0 0 0)',
  clipPath: 'inset(50%)',
  height: 1,
  overflow: 'hidden',
  position: 'absolute',
  bottom: 0,
  left: 0,
  whiteSpace: 'nowrap',
  width: 1,
});

const TabPanel = ({ children, value, index }) => (
  <Box
    role="tabpanel"
    hidden={value !== index}
    sx={{
      flex: 1,
      display: value === index ? 'block' : 'none',
      p: 2,
    }}
  >
    {value === index && children}
  </Box>
);

const DropZone = styled(Box)(({ theme }) => ({
  border: '2px dashed rgba(255, 255, 255, 0.2)',
  borderRadius: theme.spacing(1.5),
  padding: theme.spacing(4),
  minHeight: '200px',
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  justifyContent: 'center',
  backgroundColor: 'rgba(255, 255, 255, 0.02)',
  cursor: 'pointer',
  transition: 'all 0.3s ease',
  '&:hover': {
    borderColor: theme.palette.primary.main,
    backgroundColor: 'rgba(255, 255, 255, 0.05)',
  }
}));

const MainWorkspace = () => {
  const [selectedTab, setSelectedTab] = useState(0);
  const [input, setInput] = useState('');
  const [imageFile, setImageFile] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [includeHashtags, setIncludeHashtags] = useState(false);
  const [generateVariants, setGenerateVariants] = useState(false);
  const [captionDescription, setCaptionDescription] = useState('');
  const theme = useTheme();

  const commonTextFieldStyles = {
    '& .MuiOutlinedInput-root': {
      fontSize: '0.85rem',
    },
    '& .MuiInputLabel-root': {
      fontSize: '0.85rem',
    },
    mb: 1.5
  };

  const commonHeadingStyles = {
    fontSize: '1rem',
    fontWeight: 500,
    color: theme.palette.text.secondary,
    mb: 2
  };

  const handleTabChange = (event, newValue) => {
    setSelectedTab(newValue);
    setImageFile(null);
    setImagePreview(null);
    setInput('');
  };

  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    if (file && file.type.startsWith('image/')) {
      setImageFile(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  return (
    <WorkspaceContainer>
      <Paper 
        elevation={0} 
        sx={{ 
          borderRadius: 1.5,
          overflow: 'hidden',
          border: '1px solid',
          borderColor: 'divider',
          height: 'calc(100vh - 80px)',
          display: 'flex',
          flexDirection: 'column',
          ml: -0.5,
          width: 'calc(100% + 8px)',
        }}
      >
        <Tabs
          value={selectedTab}
          onChange={handleTabChange}
          variant="scrollable"
          scrollButtons="auto"
          sx={{ 
            borderBottom: 1, 
            borderColor: 'divider',
            px: 1,
            pt: 1,
          }}
        >
          <Tab 
            icon={<TextIcon />} 
            iconPosition="start"
            label="Text Generation" 
          />
          <Tab 
            icon={<ImageIcon />} 
            iconPosition="start"
            label="Image Generation" 
          />
          <Tab 
            icon={<CaptionsIcon />} 
            iconPosition="start"
            label="Caption Generator" 
          />
          <Tab 
            icon={<SocialIcon />} 
            iconPosition="start"
            label="Social Content" 
          />
          <Tab 
            icon={<BlogIcon />} 
            iconPosition="start"
            label="Blog Writing" 
          />
        </Tabs>

        <Box sx={{ 
          flexGrow: 1, 
          overflow: 'auto', 
          p: 1,
          pl: 0.5,
        }}>
          {selectedTab === 0 && (
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1.5 }}>
              {/* Input Card */}
              <Card>
                <CardContent sx={{ p: 1.5 }}>
                  <TextField
                    fullWidth
                    multiline
                    rows={3}
                    placeholder="Enter your prompt here..."
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    variant="outlined"
                    sx={commonTextFieldStyles}
                  />
                  <Button
                    variant="contained"
                    fullWidth
                    sx={{
                      mt: 1.5,
                      bgcolor: '#3B82F6',
                      '&:hover': {
                        bgcolor: '#2563EB',
                      },
                      textTransform: 'none',
                      py: 1,
                      fontSize: '0.9rem'
                    }}
                  >
                    Generate Text
                  </Button>
                </CardContent>
              </Card>

              {/* Output Card */}
              <Card>
                <CardContent sx={{ p: 1.5 }}>
                  <Box sx={{ 
                    display: 'flex', 
                    justifyContent: 'space-between', 
                    alignItems: 'center',
                    mb: 1 
                  }}>
                    <Typography variant="h6" sx={{ 
                      fontSize: '0.9rem',
                      fontWeight: 500,
                      color: 'text.secondary'
                    }}>
                      Generated Text
                    </Typography>
                    <IconButton size="small">
                      <DownloadIcon fontSize="small" />
                    </IconButton>
                  </Box>
                  
                  <Box sx={{ 
                    height: '120px',
                    border: '1px solid',
                    borderColor: 'divider',
                    borderRadius: 1,
                    p: 1.5,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    backgroundColor: alpha(theme.palette.background.default, 0.6)
                  }}>
                    <Typography color="text.secondary" sx={{ fontSize: '0.85rem' }}>
                      Generated text will appear here
                    </Typography>
                  </Box>
                </CardContent>
              </Card>
            </Box>
          )}

          {selectedTab === 1 && (
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1.5 }}>
              {/* Upload Section */}
              <Card>
                <CardContent sx={{ p: 1.5 }}>
                  <DropZone
                    component="label"
                    htmlFor="image-upload"
                  >
                    <input
                      type="file"
                      id="image-upload"
                      hidden
                      accept=".jpg,.png,.gif"
                      onChange={(e) => {
                        const file = e.target.files[0];
                        if (file) {
                          setImageFile(file);
                          const reader = new FileReader();
                          reader.onloadend = () => {
                            setImagePreview(reader.result);
                          };
                          reader.readAsDataURL(file);
                        }
                      }}
                    />
                    <UploadIcon sx={{ 
                      fontSize: 40,
                      color: 'text.secondary',
                      mb: 1.5 
                    }} />
                    <Typography variant="h6" sx={{ 
                      color: 'text.primary',
                      mb: 0.5,
                      fontSize: '1rem'
                    }}>
                      Drag & drop images or click to upload
                    </Typography>
                    <Typography variant="body2" sx={{ 
                      color: 'text.secondary',
                      fontSize: '0.85rem'
                    }}>
                      Supported formats: JPG, PNG, GIF
                    </Typography>
                  </DropZone>

                  {imagePreview && (
                    <Box sx={{ mt: 1.5 }}>
                      <img 
                        src={imagePreview} 
                        alt="Preview" 
                        style={{ 
                          maxWidth: '100%',
                          maxHeight: '150px',
                          borderRadius: '8px',
                          objectFit: 'contain'
                        }} 
                      />
                    </Box>
                  )}

                  <Button
                    variant="contained"
                    fullWidth
                    sx={{
                      mt: 1.5,
                      bgcolor: '#3B82F6',
                      '&:hover': {
                        bgcolor: '#2563EB',
                      },
                      textTransform: 'none',
                      py: 1,
                      fontSize: '0.9rem'
                    }}
                  >
                    Process Images
                  </Button>
                </CardContent>
              </Card>

              {/* Generated Images Section */}
              <Card>
                <CardContent sx={{ p: 1.5 }}>
                  <Box sx={{ 
                    display: 'flex', 
                    justifyContent: 'space-between', 
                    alignItems: 'center',
                    mb: 1 
                  }}>
                    <Typography variant="h6" sx={{ 
                      fontSize: '0.9rem',
                      fontWeight: 500,
                      color: 'text.secondary'
                    }}>
                      Generated Images
                    </Typography>
                    <IconButton size="small">
                      <DownloadIcon fontSize="small" />
                    </IconButton>
                  </Box>
                  
                  <Box sx={{ 
                    height: '120px',
                    border: '1px solid',
                    borderColor: 'divider',
                    borderRadius: 1,
                    p: 1.5,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    backgroundColor: alpha(theme.palette.background.default, 0.6)
                  }}>
                    <Typography color="text.secondary" sx={{ fontSize: '0.85rem' }}>
                      Generated images will appear here
                    </Typography>
                  </Box>
                </CardContent>
              </Card>
            </Box>
          )}

          {selectedTab === 2 && (
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1.5 }}>
              {/* Upload Section */}
              <Card>
                <CardContent sx={{ p: 1.5 }}>
                  <DropZone
                    component="label"
                    htmlFor="caption-image-upload"
                  >
                    <input
                      type="file"
                      id="caption-image-upload"
                      hidden
                      accept=".jpg,.png,.gif"
                      onChange={(e) => {
                        const file = e.target.files[0];
                        if (file) {
                          setImageFile(file);
                          const reader = new FileReader();
                          reader.onloadend = () => {
                            setImagePreview(reader.result);
                          };
                          reader.readAsDataURL(file);
                        }
                      }}
                    />
                    <UploadIcon sx={{ 
                      fontSize: 40,
                      color: 'text.secondary',
                      mb: 1.5 
                    }} />
                    <Typography variant="h6" sx={{ 
                      color: 'text.primary',
                      mb: 0.5,
                      fontSize: '1rem'
                    }}>
                      Drag & drop images or click to upload
                    </Typography>
                    <Typography variant="body2" sx={{ 
                      color: 'text.secondary',
                      fontSize: '0.85rem'
                    }}>
                      Supported formats: JPG, PNG, GIF
                    </Typography>
                  </DropZone>

                  {imagePreview && (
                    <Box sx={{ mt: 1.5 }}>
                      <img 
                        src={imagePreview} 
                        alt="Preview" 
                        style={{ 
                          maxWidth: '100%',
                          maxHeight: '150px',
                          borderRadius: '8px',
                          objectFit: 'contain'
                        }} 
                      />
                    </Box>
                  )}

                  <Box sx={{ mt: 1.5 }}>
                    <TextField
                      fullWidth
                      multiline
                      rows={2}
                      placeholder="Enter description for caption..."
                      value={captionDescription}
                      onChange={(e) => setCaptionDescription(e.target.value)}
                      sx={{ 
                        mb: 1.5,
                        '& .MuiOutlinedInput-root': {
                          fontSize: '0.85rem',
                        }
                      }}
                    />
                    
                    <Box sx={{ 
                      display: 'flex', 
                      gap: 2, 
                      mb: 1.5,
                      '& .MuiFormControlLabel-root': {
                        marginRight: 0
                      }
                    }}>
                      <FormControlLabel
                        control={
                          <Checkbox
                            checked={includeHashtags}
                            onChange={(e) => setIncludeHashtags(e.target.checked)}
                            size="small"
                          />
                        }
                        label={
                          <Typography sx={{ fontSize: '0.85rem' }}>
                            Include Hashtags
                          </Typography>
                        }
                      />
                      <FormControlLabel
                        control={
                          <Checkbox
                            checked={generateVariants}
                            onChange={(e) => setGenerateVariants(e.target.checked)}
                            size="small"
                          />
                        }
                        label={
                          <Typography sx={{ fontSize: '0.85rem' }}>
                            Generate Variants
                          </Typography>
                        }
                      />
                    </Box>

                    <Button
                      variant="contained"
                      fullWidth
                      sx={{
                        bgcolor: '#3B82F6',
                        '&:hover': {
                          bgcolor: '#2563EB',
                        },
                        textTransform: 'none',
                        py: 1,
                        fontSize: '0.9rem'
                      }}
                    >
                      Generate Captions
                    </Button>
                  </Box>
                </CardContent>
              </Card>

              {/* Generated Captions Section */}
              <Card>
                <CardContent sx={{ p: 1.5 }}>
                  <Box sx={{ 
                    display: 'flex', 
                    justifyContent: 'space-between', 
                    alignItems: 'center',
                    mb: 1 
                  }}>
                    <Typography variant="h6" sx={{ 
                      fontSize: '0.9rem',
                      fontWeight: 500,
                      color: 'text.secondary'
                    }}>
                      Generated Captions
                    </Typography>
                    <IconButton size="small">
                      <DownloadIcon fontSize="small" />
                    </IconButton>
                  </Box>
                  
                  <Box sx={{ 
                    height: '120px',
                    border: '1px solid',
                    borderColor: 'divider',
                    borderRadius: 1,
                    p: 1.5,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    backgroundColor: alpha(theme.palette.background.default, 0.6)
                  }}>
                    <Typography color="text.secondary" sx={{ fontSize: '0.85rem' }}>
                      Generated captions will appear here
                    </Typography>
                  </Box>
                </CardContent>
              </Card>
            </Box>
          )}

          {selectedTab === 3 && (
            <Card>
              <CardContent sx={{ py: 1.5 }}>
                <Typography variant="h6" gutterBottom>
                  Content Creator Assistant
                </Typography>
                <TextField
                  select
                  fullWidth
                  label="Content Type"
                  defaultValue="script"
                  sx={{ mb: 2 }}
                >
                  <MenuItem value="script">Video Script</MenuItem>
                  <MenuItem value="outline">Content Outline</MenuItem>
                  <MenuItem value="caption">Creator Caption</MenuItem>
                  <MenuItem value="hashtags">Hashtag Research</MenuItem>
                </TextField>
                <TextField
                  fullWidth
                  multiline
                  rows={2}
                  label="Brief Description"
                  placeholder="Describe your content idea or target audience..."
                  sx={{ 
                    mb: 2,
                    '& .MuiOutlinedInput-root': {
                      fontSize: '0.85rem',
                    }
                  }}
                />
                <Button
                  variant="contained"
                  endIcon={<SendIcon />}
                >
                  Generate Content
                </Button>
              </CardContent>
            </Card>
          )}

          {selectedTab === 4 && (
            <Card>
              <CardContent sx={{ py: 1.5 }}>
                <Typography variant="h6" gutterBottom>
                  Blog Writing Assistant
                </Typography>
                <TextField
                  fullWidth
                  label="Blog Title"
                  placeholder="Enter your blog title..."
                  sx={{ 
                    mb: 2,
                    '& .MuiOutlinedInput-root': {
                      fontSize: '0.85rem',
                    }
                  }}
                />
                <TextField
                  fullWidth
                  multiline
                  rows={2}
                  label="Topic Overview"
                  placeholder="Briefly describe what you want to write about..."
                  sx={{ 
                    mb: 2,
                    '& .MuiOutlinedInput-root': {
                      fontSize: '0.85rem',
                    }
                  }}
                />
                <TextField
                  select
                  fullWidth
                  label="Writing Style"
                  defaultValue="informative"
                  sx={{ mb: 2 }}
                >
                  <MenuItem value="informative">Informative</MenuItem>
                  <MenuItem value="conversational">Conversational</MenuItem>
                  <MenuItem value="professional">Professional</MenuItem>
                  <MenuItem value="casual">Casual</MenuItem>
                </TextField>
                <Button
                  variant="contained"
                  endIcon={<SendIcon />}
                >
                  Generate Blog Content
                </Button>
              </CardContent>
            </Card>
          )}
        </Box>
      </Paper>
    </WorkspaceContainer>
  );
};

export default MainWorkspace; 
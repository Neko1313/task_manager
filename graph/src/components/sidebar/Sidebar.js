import React, { useState, useRef } from 'react';
import Drawer from '@mui/material/Drawer';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import Switch from '@mui/material/Switch';
import Button from '@mui/material/Button';
import Brightness4Icon from '@mui/icons-material/Brightness4';
import Brightness7Icon from '@mui/icons-material/Brightness7';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import { useThemeContext } from './ThemeContext';
import { Link } from 'react-router-dom';
import axios from 'axios';


const Sidebar = () => {
  const { darkTheme, toggleTheme } = useThemeContext();
  const [selectedFile, setSelectedFile] = useState(null);
  const fileInputRef = useRef(null);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleFileUpload = async () => {
    if (selectedFile) {
      const formData = new FormData();
      formData.append('file', selectedFile);
  
      try {
        const response = await axios.post(
          'http://localhost:5000/api/working_data/parse_xls',
          formData,
          {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          }
        );
        console.log('Серверный ответ:', response.data);
  
        // Очищаем значение выбранного файла
        fileInputRef.current.value = null;
      } catch (error) {
        console.error('Ошибка при отправке файла:', error);
      }
  
      setSelectedFile(null);
    }
  };
  

  return (
    <Drawer variant="permanent">
      <List>
        <ListItem>
          <Switch
            checked={darkTheme}
            onChange={toggleTheme}
            color="primary"
          />
          {darkTheme ? (
            <Brightness7Icon />
          ) : (
            <Brightness4Icon />
          )}
        </ListItem>
        <ListItem button component={Link} to="/spiders">
          <ListItemText primary="Пауки" />
        </ListItem>
        <ListItem button component={Link} to="/statistics">
          <ListItemText primary="Статистика" />
        </ListItem>
        <ListItem>
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileChange}
            name="file"
            style={{ display: 'none' }}
            accept=".xlsx"
          />
          <Button
            variant="contained"
            color="primary"
            onClick={() => fileInputRef.current.click()}
            startIcon={<CloudUploadIcon />}
          >
            XLS
          </Button>
        </ListItem>
        <ListItem>
          <Button
            variant="contained"
            color="secondary"
            onClick={handleFileUpload}
            disabled={!selectedFile}
          >
            Отправить
          </Button>
        </ListItem>
      </List>
    </Drawer>
  );
};

export default Sidebar;

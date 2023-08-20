import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Container from '@mui/material/Container';
import Sidebar from './components/sidebar/Sidebar';
import SpiderPage from './components/spider/SpiderPage';
import StatsPage from './components/stats/StatsPage';
import { CustomThemeProvider } from './components/sidebar/ThemeContext';

const App = () => {
  return (
    <CustomThemeProvider>
      <Router>
        <Container>
          <Sidebar />
          <Routes>
            <Route path="/spiders" element={<SpiderPage />} />
            <Route path="/statistics" element={<StatsPage />} />
          </Routes>
        </Container>
      </Router>
    </CustomThemeProvider>
  );
};

export default App;

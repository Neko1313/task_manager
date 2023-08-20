import React, { useState } from 'react';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Typography from '@mui/material/Typography';
import Diagram from './Diagram';
import Diagram2 from './Diagram2';

const SpiderPage = () => {
  const [tabValue, setTabValue] = useState(0);

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  return (
    <div>
      <Tabs
        value={tabValue}
        onChange={handleTabChange}
        indicatorColor="primary"
        textColor="primary"
        centered
      >
        <Tab label="Фото" />
        <Tab label="Описание" />
      </Tabs>
      {tabValue === 0 && (
        <Typography>
          <Diagram/>
        </Typography>
      )}
      {tabValue === 1 && (
        <Typography>
          <Diagram2/>
        </Typography>
      )}
    </div>
  );
};

export default SpiderPage;

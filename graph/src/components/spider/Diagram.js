import React, { useState, useEffect, useCallback, useRef } from 'react';
import ReactFlow, {
  Background,
  useNodesState,
  useEdgesState,
  addEdge,
  Controls
} from 'reactflow';

import 'reactflow/dist/style.css';
import './overview.css';
import axios from 'axios';
import Button from '@mui/material/Button';
import ErrorModal from '../Error/ErrorModal';
import { ListItem } from '@mui/material';
import List from '@mui/material/List';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';

const Diagram = () => {
  const [nodePositions, setNodePositions] = useState({});
  const [responseReceived, setResponseReceived] = useState(false);
  const [error, setError] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const fileInputRef = useRef(null);

  const handleFileUpload = async () => {
    if (selectedFile) {
      const formData = new FormData();
      formData.append('file', selectedFile);
  
      try {
        const response = await axios.post(
          'http://127.0.0.1:5000/api/scrapy/scrapy_new_spider/photo',
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

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleError = (errorMessage) => {
    setError(errorMessage);
  };

  const handleCloseError = () => {
    setError(null);
  };
  useEffect(() => {
    axios.get('http://localhost:5000/api/scrapy/configuration_photo')
      .then(response => {
        const data = response.data;
        const newNodes = data.map((name, index) => ({
          id: `${name}`,
          type: 'default',
          data: { label: name },
          position: nodePositions[`${index}`] || { x: index * 250, y: index * 100 + 100 }
        }));

        const newEdges = [];
        for (let i = 0; i < newNodes.length - 1; i++) {
          newEdges.push({ id: `edge_${i}`, source: `${newNodes[i].id}`, target: `${newNodes[i+1].id}`, animated: true });
        }

        setNodes(newNodes);
        setEdges(newEdges);
        setResponseReceived(true);

      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
  }, []);

  const [nodes, setNodes, onNodesChange] = useNodesState();
  const [edges, setEdges, onEdgesChange] = useEdgesState();
  const onConnect = useCallback((params) => setEdges((eds) => addEdge(params, eds)), [setEdges]);
  const new_data = (datas, idsw) => {
    if (datas[datas.length - 1] === idsw.source){
      if (datas.length === 0){
        datas.push(idsw.source)
      }
      datas.push(idsw.target)
      return datas
    }
    else{
      if (datas.length === 0){
        datas.push(idsw.target)
      }
      datas.unshift(idsw.source)
      return datas
    }
  }
  const handlePrintEdges = async () => {
    var datas = []
    edges.map(idsw => (
      datas = new_data(datas, idsw)
    ))
    if (datas.length > 0){
      try {
        const response = await axios.post(
          'http://localhost:5000/api/scrapy/configuration_photo',
          [...new Set(datas)],
          {
            headers: {
              'Content-Type': 'application/json'
            }
          }
        );
        console.log('Серверный ответ:', response.data);
  
      } catch (error) {
        console.error('Ошибка при отправке файла:', error);
      }
      console.log(datas)
    }
    else{
      handleError("Нет не каких связий с пауками, попробуйте еще раз")
    }
    
  };
  return (
    <>
    <div style={{ width: '100%', height: '600px', padding: 'auto' }}>
      {responseReceived && (
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onConnect={onConnect}
          fitView
          attributionPosition="top-right"
        >
          <Controls />
          <Background />
        </ReactFlow>
      )}
    </div>
    <List>
      <ListItem>
        <Button variant="contained" onClick={handlePrintEdges}>Загрузить новую очередь на сервер</Button>
      </ListItem>
      <ListItem>
        <input
        type="file"
        ref={fileInputRef}
        onChange={handleFileChange}
        name="file"
        style={{ display: 'none' }}
        accept=".py"
        />
        <Button
            variant="contained"
            color="primary"
            onClick={() => fileInputRef.current.click()}
            startIcon={<CloudUploadIcon />}
          >
            .PY
        </Button>
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
    {error && <ErrorModal message={error} onClose={handleCloseError} />}
    </>
  );
};

export default Diagram;

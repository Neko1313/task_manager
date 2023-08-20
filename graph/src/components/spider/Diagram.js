import React, { useState, useEffect } from 'react';
import ReactFlow, {
  Background
} from 'reactflow';

import 'reactflow/dist/style.css';
import './overview.css';
import axios from 'axios';

const Diagram = () => {
    useEffect(() => {
        axios.get('http://localhost:5000/api/scrapy/configuration_photo')
          .then(response => {
            const data = response.data;
            const nodes_axios = data.map((name, index) => ({
              id: `${index}`,
              type: 'default',
              data: { label: name },
              position: { x: index * 250, y: index*100+100 }
            }));
    
            const edges_axios = [];
            for (let i = 0; i < nodes_axios.length - 1; i++) {
              edges_axios.push({ id: `edge_${i}`, source: `${i}`, target: `${i + 1}`, animated: true });
            }

            setElements([nodes_axios, edges_axios]);
            
          })
          .catch(error => {
            console.error('Error fetching data:', error);
          });
    }, []);
    
    const [elements, setElements] = useState([]);

    return (
        <div style={{ width: '100%', height: '600px', padding: "auto" }}>
            <ReactFlow
              nodes={elements[0]}
              edges={elements[1]}
              fitView
              attributionPosition="top-right"
            >
              <Background color="#aaa" gap={8} />
            </ReactFlow>
        </div>
        
    );
};
  
export default Diagram;

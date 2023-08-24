import React, { useState } from 'react';
import Slider from 'react-slick';
import axios from 'axios';
import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';
import "./slick-custom.css"
import Datatime from "./Datatime"
import Button from '@mui/material/Button';
import CircularProgress from '@mui/material/CircularProgress';
import JSZip from 'jszip';

function GraphSlider() {
  const [graphData, setGraphData] = useState([]);
  const [selectedDates, setSelectedDates] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchGraphData = () => {
    if (selectedDates && selectedDates.length >= 2 && selectedDates[0] && selectedDates[1]) {
      setLoading(true);

      const startDate = selectedDates[0].toISOString();
      const endDate = selectedDates[1].toISOString();

      axios.get(`http://localhost:5000/api/working_data/get_graph_data?start=${startDate}&end=${endDate}`)
        .then(response => {
          setGraphData(response.data);
        })
        .catch(error => {
          console.error('Error fetching graph data:', error);
        })
        .finally(() => {
          setLoading(false);
        });
    }
  };

  const handleFetchGraphData = () => {
    fetchGraphData();
    setSelectedDates(null); // Очищаем поля даты
  };

  const handleDownloadGraphs = () => {
    if (graphData.length > 0) {
      const zip = new JSZip();

      graphData.forEach((graph, index) => {
        const imageBlob = dataURLtoBlob(`data:image/png;base64,${graph.image_data}`);
        zip.file(`graph_${index}.png`, imageBlob);
      });

      zip.generateAsync({ type: 'blob' })
        .then((content) => {
          const downloadLink = document.createElement('a');
          downloadLink.href = URL.createObjectURL(content);
          downloadLink.download = 'graphs.zip';
          downloadLink.click();
        })
        .catch(error => {
          console.error('Error creating zip archive:', error);
        });
    }
  };

  // Helper function to convert Data URL to Blob
  function dataURLtoBlob(dataURL) {
    const arr = dataURL.split(',');
    const mime = arr[0].match(/:(.*?);/)[1];
    const bstr = atob(arr[1]);
    let n = bstr.length;
    const u8arr = new Uint8Array(n);
    while (n--) {
      u8arr[n] = bstr.charCodeAt(n);
    }
    return new Blob([u8arr], { type: mime });
  }

  const settings = {
    dots: true,
    infinite: true,
    speed: 500,
    slidesToShow: 1,
    slidesToScroll: 1,
    centerMode: true,
    centerPadding: '30px',
  };

  return (
    <div className="graph-slider-container">
      <h1>Графики</h1>
      <Datatime onDateChange={setSelectedDates} />
      <Button variant="contained" onClick={handleFetchGraphData} disabled={!selectedDates || loading}>
        {loading ? <CircularProgress size={24} /> : 'Получить графики'}
      </Button>
      <Button variant="contained" onClick={handleDownloadGraphs} disabled={graphData.length === 0}>
        Скачать графики
      </Button>
      {graphData.length > 0 && (
        <Slider {...settings}>
          {graphData.map(graph => (
            <div key={graph.id} className="graph-slide">
              <div className="date-container">
                <p className="date-text">Дата создания: {graph.access_date}</p>
              </div>
              <img src={`data:image/png;base64,${graph.image_data}`} alt="Graph"/>
            </div>
          ))}
        </Slider>
      )}
    </div>
  );
}

export default GraphSlider;

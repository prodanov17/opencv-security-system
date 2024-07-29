import React, { useState, useEffect } from 'react';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import Log from './log';

function Logs() {
  const [logs, setLogs] = useState([]);
  const [startDate, setStartDate] = useState(new Date());
  const [endDate, setEndDate] = useState(new Date());
  const [error, setError] = useState(null);

  const API_URL = import.meta.env.VITE_API_URL;

  useEffect(() => {
    fetchLogs(startDate, endDate);
  }, [startDate, endDate]);

  const fetchLogs = async (start, end) => {
    try {
      const response = await fetch(`${API_URL}/get-logs?startDate=${formatDate(start)}&endDate=${formatDate(end)}`);
      const data = await response.json();
      if (response.ok) {
        setLogs(data.logs);
        setError(null);
      } else {
        setError(data.error);
      }
    } catch (error) {
      setError('Failed to fetch logs');
    }
  };

  const formatDate = (date) => {
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const year = date.getFullYear().toString().slice(-2);
    return `${day}-${month}-${year}`;
  };

    const captureFrame = (video, canvas) => {
    const context = canvas.getContext('2d');
    video.currentTime = 0;
    video.onloadeddata = () => {
      context.drawImage(video, 0, 0, canvas.width, canvas.height);
      video.pause();
    };
  };

  return (
    <div className="flex flex-col items-center justify-center bg-gray-100 p-4">
      <h1 className="text-2xl font-bold mb-4">Motion Logs</h1>
      <div className="flex mb-4">
        <div className="mr-4">
          <label className="block text-gray-700">Start Date:</label>
          <DatePicker selected={startDate} onChange={(date) => setStartDate(date)} dateFormat="dd-MM-yy" />
        </div>
        <div>
          <label className="block text-gray-700">End Date:</label>
          <DatePicker selected={endDate} onChange={(date) => setEndDate(date)} dateFormat="dd-MM-yy" />
        </div>
      </div>
      {error && <p className="text-red-500 mb-4">{error}</p>}
      <div className="w-full max-w-2xl flex flex-col gap-2">
        {logs.map((log, index) => (
            <Log
              key={index}
              url={log.url}
              date={log.date}
              onClick={() => {}}
            />
        ))}
      </div>
    </div>
  );
}

export default Logs;


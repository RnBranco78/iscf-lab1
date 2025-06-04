'use client'

import { getDatabase, ref, onValue } from "firebase/database";
import { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, Label, AreaChart, Area} from "recharts";
import { initializeApp } from "firebase/app";
import Papa from "papaparse";

const firebaseConfig = {
  apiKey: "AIzaSyDtkV64htawFkwChpKB-2JM9G5AqQzWVNI",
  authDomain: "iscf-ac914.firebaseapp.com",
  databaseURL: "https://iscf-ac914-default-rtdb.europe-west1.firebasedatabase.app",
  projectId: "iscf-ac914",
  storageBucket: "iscf-ac914.firebasestorage.app",
  messagingSenderId: "586621867031",
  appId: "1:586621867031:web:a181f461062cb41c3c3852",
  measurementId: "G-X5CG2V4B7J"
};

initializeApp(firebaseConfig);
const db = getDatabase();

const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    return (
      <div className="bg-white border rounded p-2 shadow">
        <p className="text-black font-semibold">Time: {label}</p>
        {payload.map((entry, index) => (
          <p key={index} className="text-sm" style={{ color: entry.color }}>
            {entry.name}: {entry.value}
          </p>
        ))}
      </div>
    );
  }

  return null;
};

export default function RealtimeGraph() {
  const [data, setData] = useState([]);
  const [updateInterval, setUpdateInterval] = useState(1000);

  useEffect(() => {
    const dataRef = ref(db, "data");
    let latestData = [];
    const unsubscribe = onValue(dataRef, (snapshot) => {
        const values = snapshot.val();
        if (values) {
          latestData = Object.entries(values).map(([key, value]) => ({
            timestamp: value.timestamp || 0,
            x: value.x || 0,
            y: value.y || 0,
            z: value.z || 0,
            temp: value.temp || 0
          }));
          latestData = latestData.slice(-5000);
        }
      });

      const intervalId = setInterval(() => {
        if (latestData.length > 0) {
          setData([...latestData]);
        }
      }, updateInterval)

      return () => {
        clearInterval(intervalId);
        unsubscribe();
      };
    }, [updateInterval]);

    const calculateSummary = () => {
      if (data.length === 0) return null;
  
      const stats = ['x', 'y', 'z', 'temp'].map(key => {
        const values = data.map(item => item[key]);
        const min = Math.min(...values);
        const max = Math.max(...values);
        const avg = values.reduce((sum, val) => sum + val, 0) / values.length;
        return { metric: key, min, max, avg: avg.toFixed(2) };
      });
  
      return stats;
    };

  const handleExport = () => {
    const csv = Papa.unparse(data);
    const blob = new Blob([csv], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "simulation_data.csv";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    const summary = calculateSummary();
    if (summary) {
      const summaryCsv = Papa.unparse(summary);
      const summaryBlob = new Blob([summaryCsv], { type: "text/csv" });
      const summaryUrl = URL.createObjectURL(summaryBlob);
      const summaryA = document.createElement("a");
      summaryA.href = summaryUrl;
      summaryA.download = "summary_data.csv";
      document.body.appendChild(summaryA);
      summaryA.click();
      document.body.removeChild(summaryA);
    }
  };

  useEffect(() => {
    const intervalId = setInterval(() => {
      handleExport();
    }, 600000);
    return () => clearInterval(intervalId);
  }, [data.length]);

  return (
    <div className="p-4">
      <h1 className="text-xl font-bold mb-2">Real-time Accelerometer Data</h1>
      <label className="block mb-2">Update Interval:
        <select
          value={updateInterval}
          onChange={(e) => setUpdateInterval(Number(e.target.value))}
          className="ml-2 p-1 border rounded"
        >
          <option value={1000}>1 second</option>
          <option value={2000}>2 seconds</option>
        </select>
      </label>
      <LineChart width={750} height={250} data={data}>
        <CartesianGrid strokeDasharray="1 1" />
        <XAxis dataKey="timestamp">
          <Label value = "Time" offset={-10} position="insideBottom"/>
        </XAxis>
        <YAxis yAxisId="Coppelia Data for X" width={120}>
          <Label value="Coppelia Data for X" offset={0} angle={-90} position="Left"/>
        </YAxis>
        <Tooltip content={<CustomTooltip />} />
        <Legend />
        <Line yAxisId = "Coppelia Data for X" type="monotone" dataKey="x" stroke="#8884d8" />
      </LineChart>
      <LineChart width={750} height={250} data={data}>
        <CartesianGrid strokeDasharray="1 1" />
        <XAxis dataKey="timestamp">
          <Label value = "Time" offset={-10} position="insideBottom"/>
        </XAxis>
        <YAxis yAxisId="Coppelia Data for Y" width={120}>
          <Label value="Coppelia Data for Y" offset={0} angle={-90} position="Left"/>
        </YAxis>
        <Tooltip content={<CustomTooltip />} />
        <Legend />
        <Line yAxisId = "Coppelia Data for Y" type="monotone" dataKey="y" stroke="#82ca9d" />
      </LineChart>
      <LineChart width={750} height={250} data={data}>
        <CartesianGrid strokeDasharray="1 1" />
        <XAxis dataKey="timestamp">
          <Label value = "Time" offset={-10} position="insideBottom"/>
        </XAxis>
        <YAxis yAxisId="Coppelia Data for Z" width={120}>
          <Label value="Coppelia Data for Z" offset={0} angle={-90} position="Left"/>
        </YAxis>
        <Tooltip content={<CustomTooltip />} />
        <Legend />
        <Line yAxisId = "Coppelia Data for Z" type="monotone" dataKey="z" stroke="#8B4513" />
      </LineChart>
      <LineChart width={750} height={250} data={data}>
        <CartesianGrid strokeDasharray="1 1" />
        <XAxis dataKey="timestamp">
          <Label value = "Time" offset={-10} position="insideBottom"/>
        </XAxis>
        <YAxis yAxisId="Temperature Data" width={100} domain={[300, 'auto']}>
          <Label value="Temperature Data(K)" offset={0} angle={-90} position="Left"/>
        </YAxis>
        <Tooltip content={<CustomTooltip />} />
        <Legend />
        <Line yAxisId = "Temperature Data" type="monotone" dataKey="temp" stroke="#8B4513" />
      </LineChart>
      <button className="mt-4 p-2 bg-blue-500 text-white rounded" onClick={handleExport}>Download Report</button>
    </div>
  );
}
import React, { useEffect, useState } from 'react';
import './App.css';
import LineCharts from './components/LineCharts';
import TemperatureGauge from './components/TemperatureGauge';
import HumidityGauge from './components/HumidityGauge';
import mqtt from 'mqtt';

function App() {
  const [temperatureData, setTemperatureData] = useState([]);
  const [humidityData, setHumidityData] = useState([]);

  useEffect(() => {
    const client = mqtt.connect('ws://192.168.10.175:9001'); // Asegúrate de que tu broker MQTT tiene WebSocket habilitado en ese puerto

    client.on('connect', () => {
      console.log('Conectado al broker MQTT');
      client.subscribe('casa/temperatura'); // Asegúrate de que este es el topic correcto
    });

    client.on('message', (topic, message) => {
      try {
        const newData = JSON.parse(message.toString());

        setTemperatureData((prevData) => [
          ...prevData,
          { timestamp: newData.timestamp, value: newData.temperatura_c},
        ]);

        setHumidityData((prevData) => [
          ...prevData,
          { timestamp: newData.timestamp, value: newData.humedad },
        ]);

        console.log(newData);
      } catch (err) {
        console.error('Error al parsear el mensaje MQTT:', err);
      }
    });

    return () => {
      client.end();
      console.log('Desconectado del broker MQTT');
    };
  }, []);

  return (
    <div className="container">
      <header>
        <h1>Sensor Data Dashboard</h1>
      </header>
      <div className="sensor-data">
        <div className="sensor-data-item">
          <h2>Timestamp</h2>
          <p>{temperatureData.length > 0 && temperatureData[temperatureData.length - 1].timestamp}</p>
        </div>
        <div className="sensor-data-item">
          <h2>Temperatura</h2>
          <p>{temperatureData.length > 0 && temperatureData[temperatureData.length - 1].value} °C</p>
          {temperatureData.length > 0 && typeof temperatureData[temperatureData.length - 1].value === 'number' && (
            <TemperatureGauge value={temperatureData[temperatureData.length - 1].value} />
          )}
        </div>
        <div className="sensor-data-item">
          <h2>Humedad</h2>
          <p>{humidityData.length > 0 && humidityData[humidityData.length - 1].value} %</p>
          {humidityData.length > 0 && typeof humidityData[humidityData.length - 1].value === 'number' && (
            <HumidityGauge value={humidityData[humidityData.length - 1].value} />
          )}
        </div>
      </div>
      <div className="charts">
        <LineCharts data={temperatureData} label="Temperature" />
        <LineCharts data={humidityData} label="Humidity" />
      </div>
    </div>
  );
}

export default App;

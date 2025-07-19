import React, { useEffect, useState } from 'react';
import './App.css';
import LineCharts from './components/LineCharts';
import TemperatureGauge from './components/TemperatureGauge';
import HumidityGauge from './components/HumidityGauge';
import mqtt from 'mqtt';
import ReactMarkdown from 'react-markdown';

function App() {
  const [temperatureData, setTemperatureData] = useState([]);
  const [humidityData, setHumidityData] = useState([]);
  const [adviceMessage, setAdviceMessage] = useState('Esperando recomendación...');
  const [lastUpdate, setLastUpdate] = useState('');

  useEffect(() => {
    const client = mqtt.connect('ws://192.168.10.175:9001');

    client.on('connect', () => {
      console.log('Conectado al broker MQTT');
      client.subscribe('cuartofrio/sensor');
      client.subscribe('cuartofrio/recomendaciones');
    });

    client.on('message', (topic, message) => {
      try {
        if (topic === 'cuartofrio/sensor') {
          const newData = JSON.parse(message.toString());
          const timestamp = new Date().toLocaleTimeString();

          setTemperatureData((prevData) => [
            ...prevData,
            { timestamp, value: newData.temperatura_c },
          ]);

          setHumidityData((prevData) => [
            ...prevData,
            { timestamp, value: newData.humedad },
          ]);

          setLastUpdate(timestamp);
          console.log('Datos de sensor:', newData);
        }

        if (topic === 'cuartofrio/recomendaciones') {
          const advice = message.toString();
          setAdviceMessage(advice);
          console.log('Recomendación recibida:', advice);
        }
      } catch (err) {
        console.error('Error al procesar mensaje MQTT:', err);
      }
    });

    return () => {
      client.end();
      console.log('Desconectado del broker MQTT');
    };
  }, []);

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1>Monitoreo de Cuarto Frío</h1>
        <div className="status-indicator">
          <span className="status-dot"></span>
          <span>Conectado</span>
          <span className="last-update">Última actualización: {lastUpdate}</span>
        </div>
      </header>

      <div className="dashboard-grid">
        {/* Sección de medidores */}
        <div className="gauges-section">
          <div className="gauge-card temperature-card">
            <h2>Temperatura Actual</h2>
            <div className="gauge-value">
              {temperatureData.length > 0 && temperatureData[temperatureData.length - 1].value} °C
            </div>
            {temperatureData.length > 0 && typeof temperatureData[temperatureData.length - 1].value === 'number' && (
              <TemperatureGauge value={temperatureData[temperatureData.length - 1].value} />
            )}
          </div>

          <div className="gauge-card humidity-card">
            <h2>Humedad Actual</h2>
            <div className="gauge-value">
              {humidityData.length > 0 && humidityData[humidityData.length - 1].value} %
            </div>
            {humidityData.length > 0 && typeof humidityData[humidityData.length - 1].value === 'number' && (
              <HumidityGauge value={humidityData[humidityData.length - 1].value} />
            )}
          </div>
        </div>

        {/* Sección de recomendación */}
        <div className="advice-section">
          <div className="advice-card">
            <h2>Recomendación Técnica</h2>
            <div className="advice-content">
              <ReactMarkdown>{adviceMessage}</ReactMarkdown>
            </div>
          </div>
        </div>

        {/* Sección de gráficos */}
        <div className="charts-section">
          <div className="chart-card">
            <h3>Historial de Temperatura (°C)</h3>
            <LineCharts data={temperatureData} label="Temperature" color="#FF6B6B" />
          </div>
          <div className="chart-card">
            <h3>Historial de Humedad (%)</h3>
            <LineCharts data={humidityData} label="Humidity" color="#4D96FF" />
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
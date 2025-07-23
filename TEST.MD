# 🧊 IoT Cold Room Monitoring System con IA y Contenedores

> Sistema inteligente de monitoreo ambiental para cámaras frigoríficas usando arquitectura MAPE-K, sensores IoT, modelo LLM local y despliegue Docker.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)  
[![Node-RED](https://img.shields.io/badge/Node--RED-Enabled-red)](https://nodered.org/)  
[![MQTT](https://img.shields.io/badge/MQTT-Broker-orange)](https://mqtt.org/)  
[![MongoDB](https://img.shields.io/badge/Database-MongoDB-green)](https://www.mongodb.com/)  
[![LLM](https://img.shields.io/badge/LLM-Local%20AI-informational)](https://huggingface.co/)  
[![Docker](https://img.shields.io/badge/Containerized-Docker-blue)](https://www.docker.com/)  
[![React](https://img.shields.io/badge/Frontend-React-61DAFB?logo=react&logoColor=white)](https://reactjs.org/)  
[![LangChain](https://img.shields.io/badge/Framework-🦜🔗LangChain-blueviolet)](https://www.langchain.com/)

---

## 📑 Tabla de Contenidos

- [🔥 Descripción General](#-descripción-general)  
- [⚙️ Componentes Principales](#️-componentes-principales)  
- [🧠 Arquitectura MAPE-K](#-arquitectura-mape-k)  
- [🔍 Características Técnicas](#-características-técnicas)  
- [💻 Tecnologías Usadas](#-tecnologías-usadas)  
- [📦 Contenedores Activos](#-contenedores-activos)  
- [🚀 Flujo de Datos](#-flujo-de-datos)  
- [🤖 Uso del Modelo LLM](#-uso-del-modelo-llm)  
- [📸 Vistas del Proyecto](#-vistas-del-proyecto)  
- [🚧 Ejecución del Proyecto](#-ejecución-del-proyecto)  
- [📊 Simulación en Node-RED](#-simulación-en-node-red)  
- [🛠️ Configuración de Mosquitto](#️-configuración-de-mosquitto)  
- [🧰 Referencias](#-referencias)  
- [✅ TODO y NICE TO DO](#-todo-y-nice-to-do)  
- [🛡 Seguridad](#-seguridad)

---

## 🔥 Descripción General

> ⚠️ **Nota**: Este proyecto **no utiliza Docker Compose**. Todos los contenedores se gestionan manualmente usando comandos `docker build`, `docker run`, `docker stop`, etc.

Sistema distribuido en **7 contenedores colaborativos** que permiten:

- Capturar datos ambientales (temperatura/humedad)  
- Detectar condiciones críticas en tiempo real  
- Generar recomendaciones usando un modelo de lenguaje local (LLM)  
- Visualizar datos e historial vía dashboard  
- Notificar al usuario vía Telegram  

---

## ⚙️ Componentes Principales

| Componente          | Descripción                                                         |
|---------------------|---------------------------------------------------------------------|
| **Node-RED**        | Simulador y orquestador de sensores MQTT                           |
| **Mosquitto Broker**| Comunicación MQTT entre sensores y procesadores                    |
| **MongoDB + Compass** | Almacenamiento de datos históricos                                |
| **Dashboard React** | Visualización en tiempo real                                       |
| **Contenedor LLM**  | Modelo de lenguaje que genera recomendaciones técnicas            |
| **Bot Telegram**    | Notificaciones en caso de valores fuera de rango                   |
| **Runner Python**   | Ejecuta las acciones definidas por el modelo de IA                 |

---

## 🧠 Arquitectura MAPE-K

> Aplicación del ciclo MAPE-K (Monitor, Analyze, Plan, Execute – Knowledge) para gestionar ambientes críticos.

![Arquitectura](https://github.com/user-attachments/assets/3ee01b48-c806-493b-ab15-6cc4c0a5dcb0)

---

## 🔍 Características Técnicas

- 📡 **Monitoreo en tiempo real** vía MQTT  
- 🧠 **IA local** con modelo LLM  
- 📊 **Dashboard interactivo**  
- 🔔 **Alertas** por Telegram  
- 🐳 **Despliegue Docker** (manual)  
- 📁 **Persistencia NoSQL** con MongoDB  

---

## 💻 Tecnologías Usadas

- **Lenguajes**: Python 3.8+, JavaScript  
- **Frontend**: React + WebSockets  
- **Base de Datos**: MongoDB + Mongo Express  
- **Contenedores**: Docker  
- **IA Local**: `ai/smollm2` (vía plugin de modelos)  
- **Broker MQTT**: Eclipse Mosquitto  
- **Orquestación**: Node-RED  

---

## 📦 Contenedores Activos

- `mosquitto`  
- `nodered`  
- `mongodb`  
- `mongo-express`  
- `frontend-dashboard`  
- `llm-runner`  
- `planner.py`  

---

## 🚀 Flujo de Datos

1. Sensor simulado emite datos vía MQTT  
2. Node-RED recibe y guarda en MongoDB  
3. Se analizan los datos  
4. Si hay alerta:  
   - Notificación Telegram  
   - Recomendación por LLM  
5. Visualización en dashboard  

---

## 🤖 Uso del Modelo LLM

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:12434/engines/v1",
    api_key="local-key"
)

response = client.completions.create(
    model="ai/smollm2:360M-Q4_K_M",
    prompt="¿Qué hacer si la temperatura es 2°C bajo lo esperado?",
    max_tokens=100,
)

print(response.choices[0].text)
```

---

## 📸 Vistas del Proyecto

### Dashboard  
![Dashboard 1](https://github.com/user-attachments/assets/a38aa4a7-8ebf-463f-8015-c9bfb29769db)  
![Dashboard 2](https://github.com/user-attachments/assets/609aa1cc-0dd8-41d8-86f8-df881c86df30)  

### Telegram Alerts  
![Bot Telegram](https://github.com/user-attachments/assets/5eaa731a-da88-4b74-8cb2-a7fa2f3536e3)  

### Activación de Alerta  
<img width="656" height="945" alt="Recomendación de seguridad" src="https://github.com/user-attachments/assets/6acac98e-9750-4756-86c4-c15d226acd64" />

---

## 🚧 Ejecución del Proyecto

### Cliente React
```bash
cd client
npm install
npm start
```

### Servicio MAPE-K (`planeador.py`)

Instalar dependencias:
```bash
pip install -r requirements.txt
```

Ejecutar en primer plano (modo prueba):
```bash
python planeador.py --interval 10 --log-file my_service.log
```

Ejecutar como daemon:
```bash
python planeador.py --interval 10 --log-file my_service.log --daemon
```

Detener daemon:
```bash
kill $(cat /tmp/analyzer_service.pid)
```

---

## 📊 Simulación en Node-RED

Función para generar datos simulados:

```javascript
// Temperatura: 0°C a 8°C
var randomTemperatureC = parseFloat((Math.random() * (8 - 0) + 0).toFixed(2));
// Humedad: 30% a 60%
var randomHumidity = parseFloat((Math.random() * (60 - 30) + 30).toFixed(2));
// Fecha/hora actual simulada
var now = new Date();

msg.payload = {
  sensor: "Sensor_A1",
  temperatura_c: randomTemperatureC,
  humedad: randomHumidity,
  fecha_hora: now.toLocaleString()
};
return msg;
```

Visual de flujo:  
<img width="1018" height="453" alt="image" src="https://github.com/user-attachments/assets/7bd9634a-6161-4439-bf12-9caa231c3525" />

---

## 🛠️ Configuración de Mosquitto

```bash
docker run -d --name mosquitto-container -p 1883:1883 -p 9001:9001 eclipse-mosquitto
docker exec -it mosquitto-container /bin/sh
apk update && apk add nano
nano mosquitto/config/mosquitto.conf
```

Configura el archivo:
```
allow_anonymous true
listener 1883 0.0.0.0
protocol mqtt
listener 9001
protocol websockets
```

Reinicia:
```bash
docker restart mosquitto-container
```

---

## 🧰 Referencias

- [MongoDB + Mongo Express Docker](https://github.com/cataniamatt/mongodb-docker)  
- [IoT Monitoring Dashboard](https://github.com/jamalabdi2/IoT-Temperature-And-Humidity-Monitoring-System)  
- [Integración Docker + LLM](https://jggomezt.medium.com/building-local-ai-applications-integrating-docker-model-runner-genkit-and-langchain-d0dfb4a4dfa7)  

---

## ✅ TODO y NICE TO DO

- [ ] Automatizar con Docker Compose  
- [ ] Comentarios PEP8 en código Python  
- [ ] Autenticación en dashboard  
- [ ] Umbrales editables  
- [ ] Actuadores GPIO  
- [ ] Lanzador de servicios  
- [ ] Reemplazar `npm start` por versión producción  

---

## 🛡 Seguridad

> **Importante**: ocultar datos sensibles como tokens de Telegram del repositorio público.

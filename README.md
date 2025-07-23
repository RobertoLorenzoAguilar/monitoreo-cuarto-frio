
# 🧊 IoT Cold Room Monitoring System con IA y Contenedores

> Sistema inteligente de monitoreo ambiental para cámaras frigoríficas usando arquitectura MAPE-K, sensores IoT, modelo LLM local y despliegue Docker.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Node-RED](https://img.shields.io/badge/Node--RED-Enabled-red)](https://nodered.org/)
[![MQTT](https://img.shields.io/badge/MQTT-Broker-orange)](https://mqtt.org/)
[![MongoDB](https://img.shields.io/badge/Database-MongoDB-green)](https://www.mongodb.com/)
[![LLM](https://img.shields.io/badge/LLM-Local%20AI-informational)](https://huggingface.co/)
[![Docker](https://img.shields.io/badge/Containerized-Docker-blue)](https://www.docker.com/)

---

## 🔥 Descripción General

> ⚠️ **Nota**: Este proyecto **no utiliza Docker Compose**. Todos los contenedores se gestionan manualmente usando comandos `docker build`, `docker run`, `docker stop`, etc.


Este sistema distribuye la carga de monitoreo y toma de decisiones en **7 contenedores colaborativos**, los cuales permiten:

- Capturar datos ambientales (temperatura/humedad)
- Detectar condiciones críticas en tiempo real
- Generar recomendaciones usando un modelo de lenguaje local (LLM)
- Visualizar la información y el histórico vía dashboard
- Notificar al usuario vía Telegram

---

## ⚙️ Componentes Principales

| Componente         | Descripción                                                                 |
|--------------------|-----------------------------------------------------------------------------|
| **Node-RED**        | Simulador y orquestador de sensores MQTT                                   |
| **Mosquitto Broker**| Comunicación MQTT entre sensores y procesadores                            |
| **MongoDB + Compass** | Almacenamiento de datos históricos                                       |
| **Dashboard React** | Visualización en tiempo real                                                |
| **Contenedor LLM**  | Modelo de lenguaje que genera recomendaciones técnicas                     |
| **Bot Telegram**    | Notificaciones en caso de valores fuera de rango                           |
| **Runner Python**   | Ejecuta las acciones definidas por el modelo de IA                         |

---

## 🧠 Arquitectura MAPE-K

> Aplicación del ciclo MAPE-K (Monitor, Analyze, Plan, Execute – Knowledge) para gestionar ambientes críticos.

![Arquitectura](https://github.com/user-attachments/assets/3ee01b48-c806-493b-ab15-6cc4c0a5dcb0)

---

## 🔍 Características Técnicas

- 📡 **Monitoreo en tiempo real** vía MQTT
- 🧠 **IA integrada** localmente vía modelo LLM
- 📊 **Dashboard interactivo** con histórico
- 🔔 **Alertas** mediante Telegram solo cuando es necesario
- 🧰 **Despliegue completo** vía Docker Compose
- 📁 **Persistencia NoSQL** con MongoDB

---

## 💻 Tecnologías Usadas

- **Lenguajes**: Python 3.8+, JavaScript
- **Frontend**: React + WebSockets
- **Base de Datos**: MongoDB + Mongo Express
- **Contenedores**: Docker, Docker Compose
- **IA Local**: `ai/smollm2` vía plugin de modelos
- **Broker MQTT**: Eclipse Mosquitto
- **Orquestación**: Node-RED

---

## 📦 Contenedores en Ejecución

- `mosquitto`: Broker MQTT
- `nodered`: Simulación y procesamiento de flujos
- `mongodb`: Base de datos
- `mongo-express`: Visualizador de base de datos
- `frontend-dashboard`: Visualización React
- `llm-runner`: Modelo LLM
- `planner.py`: Daemon de acciones y notificaciones

---

## 🚀 Ejemplo de Flujo de Datos

1. Sensor simulado emite temperatura vía MQTT
2. Node-RED recibe y guarda en MongoDB
3. El sistema analiza los valores
4. Si hay alerta:
   - Envía notificación vía Telegram
   - Genera recomendación vía LLM
5. Se visualiza todo en el dashboard

---

## 🤖 Ejemplo de Uso del Modelo LLM

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

### Dashboard en Tiempo Real

![Dashboard 1](https://github.com/user-attachments/assets/a38aa4a7-8ebf-463f-8015-c9bfb29769db)
![Dashboard 2](https://github.com/user-attachments/assets/609aa1cc-0dd8-41d8-86f8-df881c86df30)

### Alertas Telegram

![Bot Telegram](https://github.com/user-attachments/assets/5eaa731a-da88-4b74-8cb2-a7fa2f3536e3)

---

## 📋 TODO

- [ ] Automatizar despliegue con `docker-compose up`
- [ ] Comentar todo el código fuente segú pep8 de python
- [ ] Añadir interfaz para configurar umbrales de alerta
- [ ] Agregar un actuador físico (ej. luz/señal) vía GPIO
- [ ] Añadir autenticación a la interfaz visual un "LOGIN"


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

## 📋 Por Documentar 
<img width="656" height="1086" alt="image" src="https://github.com/user-attachments/assets/0f086b81-5093-47ed-857e-08b1883d41fd" />

## Otros 🏗️

> Se activa una alerta cuando los parámetros **no** están dentro de los rangos definidos como seguros.

<img width="656" height="945" alt="Recomendación de seguridad" src="https://github.com/user-attachments/assets/6acac98e-9750-4756-86c4-c15d226acd64" />

---

## 🏗️ Arquitectura General

> Diagrama de distribución y comunicación entre contenedores y servicios.

<img width="1055" height="720" alt="Arquitectura" src="https://github.com/user-attachments/assets/3ee01b48-c806-493b-ab15-6cc4c0a5dcb0" />

---

## 🚧 NICE TO DO

- [ ] Comentar adecuadamente el código fuente.
- [ ] Ejecutar cliente en modo producción (`npm start`) en lugar de `dev`.
- [ ] Crear un lanzador de servicios.
- [ ] Integrar sistema de alertas vía Telegram.
- [ ] Activar un actuador físico (foco o semáforo) si hay valores fuera de rango.

---

## 🐳 Mosquitto en Docker

1. **Crear contenedor Mosquitto**:

```bash
docker run -d --name mosquitto-container -p 1883:1883 -p 9001:9001 eclipse-mosquitto
```

2. **Acceder al contenedor**:

```bash
docker exec -it mosquitto-container /bin/sh
```

3. **Instalar herramientas para edición**:

```bash
apk update && apk add nano
```

4. **Editar configuración**:

```bash
nano mosquitto/config/mosquitto.conf
```

Descomenta y configura lo siguiente:

```
allow_anonymous true

listener 1883 0.0.0.0
protocol mqtt

listener 9001
protocol websockets
```

5. **Reiniciar contenedor**:

```bash
docker restart mosquitto-container
```

6. **Prueba de suscripción/publicación MQTT**:

```bash
mosquitto_sub -h 192.168.16.76 -t "prueba/robert"
mosquitto_pub -h localhost -p 1883 -t "prueba/robert" -m "¡Hola MQTT desde Docker!"
```

---

## 🧰 Node-RED

1. **Ejecutar Node-RED en contenedor**:

```bash
docker run -d -p 1880:1880 --name mynodered nodered/node-red
```

2. **Gestionar flujos** desde el navegador:
```
http://localhost:1880/
```

---

## 🧱 MongoDB + Mongo Express

Repositorio sugerido: [cataniamatt/mongodb-docker](https://github.com/cataniamatt/mongodb-docker)

Autenticación sugerida para MongoDB Compass:
- **Usuario:** admin
- **Contraseña:** pass

<img width="623" height="321" alt="MongoDB Compass" src="https://github.com/user-attachments/assets/1920c777-8930-4557-aaa2-a8ec98d6d479" />

---

## 🌐 Comunicación WebSocket

Configurar WebSocket para una comunicación eficiente con el dashboard de visualización en tiempo real.

---

## 🤖 LLMs Locales con Docker "es necesario tener corriendo el servicio de docker“

Guía útil: [Medium - Integrando Genkit y LangChain](https://jggomezt.medium.com/building-local-ai-applications-integrating-docker-model-runner-genkit-and-langchain-d0dfb4a4dfa7)

### Instalación del plugin de modelos:

```bash
sudo apt-get update
sudo apt-get install docker-model-plugin
```

### Probar instalación:

```bash
docker model version
docker model run ai/smollm2
```

Modelo en DockerHub: [ai/smollm2](https://hub.docker.com/r/ai/smollm2)

### Ejemplo de uso:

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:12434/engines/v1",
    api_key="local-key"
)

response = client.completions.create(
    model="ai/smollm2:360M-Q4_K_M",
    prompt="¿Recomendación climatica?",
    max_tokens=100,
)

print(response.choices[0].text)
```

---

## 📊 Herramientas de Monitoreo

- `htop` para supervisar consumo del modelo.
- Evaluar coherencia de las respuestas.
- Listar modelos disponibles:

```bash
docker model list
```

<img width="1611" height="996" alt="Modelos listados" src="https://github.com/user-attachments/assets/fb8d5a8c-6e6a-45af-844b-07ee64ee251e" />

---


## Cuarto Frio Bot Alertas
<img width="983" height="948" alt="image" src="https://github.com/user-attachments/assets/5eaa731a-da88-4b74-8cb2-a7fa2f3536e3" />



## Habilitar Grupos para el chatbot
<img width="720" height="700" alt="image" src="https://github.com/user-attachments/assets/99763de9-b7b6-4a5b-b5f2-c675eaa0be74" />

## Referencias

- **MongoDB + Mongo Express**  
  [https://github.com/cataniamatt/mongodb-docker](https://github.com/cataniamatt/mongodb-docker)

- **Cliente React para monitoreo IoT**  
  [https://github.com/jamalabdi2/IoT-Temperature-And-Humidity-Monitoring-System](https://github.com/jamalabdi2/IoT-Temperature-And-Humidity-Monitoring-System)

- **Ejecución de modelos de IA de forma local (Docker + Genkit + LangChain)**  
  [https://jggomezt.medium.com/building-local-ai-applications-integrating-docker-model-runner-genkit-and-langchain-d0dfb4a4dfa7](https://jggomezt.medium.com/building-local-ai-applications-integrating-docker-model-runner-genkit-and-langchain-d0dfb4a4dfa7)

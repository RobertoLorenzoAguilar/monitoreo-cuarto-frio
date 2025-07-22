Tablero Visualización en tiempo real sensor humedad/temperatura
# IoT Cold Room Monitoring System 🌡️💧

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![IoT](https://img.shields.io/badge/IoT-Enabled-green)](https://en.wikipedia.org/wiki/Internet_of_things)
[![Real-time](https://img.shields.io/badge/Real--time-WebSockets-orange)](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API)

Sistema de monitoreo para cámaras frigoríficas que integra IoT, análisis  y recomendaciones técnicas mediante IA.

## Características Principales 🚀

- **Monitoreo en Tiempo Real** de temperatura y humedad mediante sensores IoT
- **Dashboard** con visualización de datos históricos y actuales
- **Sistema de Alertas** que solo notifica cuando los parámetros salen de rangos seguros
- **Recomendaciones Técnicas Automatizadas** generadas por un modelo LLM local
- **Arquitectura MAPE-K** (Monitor, Analyze, Plan, Execute - Knowledge) para gestión
- **Comunicación Bidireccional** mediante WebSockets para actualizaciones instantáneas
- **Base de Datos No Relacional** para almacenamiento eficiente de series temporales

## Tecnologías Clave 🔧

- **Backend**: Python 3.8+
- **Frontend**: react
- **Base de Datos**: MongoDB
- **IoT**: Protocolos MQTT/HTTP para comunicación con sensores
- **IA**: Modelo LLM en contenedor Docker para generación de recomendaciones
- **Infraestructura**: Contenedores Docker para despliegue escalable

## Arquitectura del Sistema 🏗️


# Sistema de Monitoreo Inteligente con Contenedores

Este repositorio documenta el despliegue de un sistema distribuido para monitoreo inteligente de condiciones ambientales, integración con actuadores físicos, visualización en tiempo real y procesamiento con LLMs de forma local.

---

## 🧠 Recomendaciones de Seguridad

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

## 🤖 LLMs Locales con Docker

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


Cuarto Frio Bot Alertas
<img width="983" height="948" alt="image" src="https://github.com/user-attachments/assets/5eaa731a-da88-4b74-8cb2-a7fa2f3536e3" />


Habilitar Grupos para el chatbot
<img width="720" height="700" alt="image" src="https://github.com/user-attachments/assets/99763de9-b7b6-4a5b-b5f2-c675eaa0be74" />

Visualización alertas 
<img width="1206" height="935" alt="image" src="https://github.com/user-attachments/assets/2518ca48-8544-4a9b-b2c4-b028eb4ef75c" />


## 📸 Vistas del Proyecto

Dashboard:

<img width="1489" height="870" alt="Dashboard 1" src="https://github.com/user-attachments/assets/a38aa4a7-8ebf-463f-8015-c9bfb29769db" />
<img width="1416" height="846" alt="Dashboard 2" src="https://github.com/user-attachments/assets/609aa1cc-0dd8-41d8-86f8-df881c86df30" />


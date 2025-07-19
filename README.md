Tablero Visualización en tiempo real sensor humedad/temperatura
<img width="1489" height="870" alt="image" src="https://github.com/user-attachments/assets/a38aa4a7-8ebf-463f-8015-c9bfb29769db" />

<img width="1416" height="846" alt="image" src="https://github.com/user-attachments/assets/609aa1cc-0dd8-41d8-86f8-df881c86df30" />


TODO:

** agregar comentario codigo **
** agregar client en vez de dev a produccion npm start  **
** agregar lanzador de servicio **



Se genera un contenedor a partir d ela imagen eclipse-mosquitto
docker run -d --name mosquitto-container 1883:1883 -p 9001:9001 eclipse-mosquitto


se accede al contenedor para configurar el servicio 

docker exec -it mosquitto_agosto /bin/sh

para instalar en el contenedor nano y poder editar la configuración del servidor de mosquitto
apk update
apk add nano

se edita el siguiente archivo
nano mosquitto/config/mosquitto.conf

se ubican en el archivo las siguientes líneas

se descomentan y setean los siguientes paramentros
allow_anonymous true
listener 1883 0.0.0.0

una vez hecho esto se sale del contenedor

y reinicia

docker restart mosquitto-container


se instala la librería de donde se encuentra para probar de mqtt cliente

mosquitto_sub -h 192.168.16.76 -t “prueba/robert”

mosquitto_pub -h localhost -p 1883 -t "prueba/robert" -m "¡Hola MQTT desde Docker!"

y se denerian ver en los nodos subscritos 


<img width="442" height="106" alt="image" src="https://github.com/user-attachments/assets/cea14113-751f-4c07-bdb5-0d921c2f6d6b" />



Se procede a prototipar con node-red

Con el siguiente comando se   instala y corre node-red 
docker run -d -p 1880:1880 --name mynodered nodered/node-red 


desde la url en el explorador puedee entra para gesstionar cualquier tipo de trabejo


CREAR CONTENEDOR PARA MONGO Y GESTIONARLO CON MONGOEXPRESS

https://github.com/cataniamatt/mongodb-docker




mongodbcompass 

admin
pass

mongodb autentification

<img width="1412" height="862" alt="image" src="https://github.com/user-attachments/assets/739147f9-134d-43bb-8fcf-7dfffc9dc0f3" />


<img width="623" height="321" alt="image" src="https://github.com/user-attachments/assets/1920c777-8930-4557-aaa2-a8ec98d6d479" />

configurar web socket para establecer un canal de comunicacion mas eficiente con el dashboard de visualización


LLMS info




https://jggomezt.medium.com/building-local-ai-applications-integrating-docker-model-runner-genkit-and-langchain-d0dfb4a4dfa7


install docker model run

https://docs.docker.com/ai/model-runner/


sudo apt-get update
sudo apt-get install docker-model-plugin


test instalacion


docker model version
docker model run ai/smollm2


https://hub.docker.com/r/ai/smollm2


ejemplo

from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:12434/engines/v1",  # o según tu endpoint
    api_key="local-key"  # cualquier texto, si el servidor local no requiere cl$
)

response = client.completions.create(
   # model="ai/gemma3:latest",
    model="ai/smollm2:360M-Q4_K_M",
    prompt="¿Cómo preparo los chilaquiles?",
    max_tokens=100,
)

print(response.choices[0].text)



<img width="442" height="649" alt="image" src="https://github.com/user-attachments/assets/2f5addef-0507-4b0b-9712-a24956b6867c" />


Instalación Herramientas para gestion de modelos dockernizados:

<img width="539" height="488" alt="image" src="https://github.com/user-attachments/assets/02a3af61-747d-4f5d-b394-4f59fec1d0e8" />

Análisis modelos de LLM 
Herramientas:
HTOP
Coherencia en respuestas

docker model list

como puede apreciarse tenemos instalados dos modelos diferentes.

<img width="1611" height="996" alt="image" src="https://github.com/user-attachments/assets/fb8d5a8c-6e6a-45af-844b-07ee64ee251e" />

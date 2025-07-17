
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
<img width="442" height="528" alt="image" src="https://github.com/user-attachments/assets/44e9d496-de62-4af2-9507-d4156c96b79e" />



Instalación Herramientas para gestion de modelos dockernizados:

<img width="539" height="488" alt="image" src="https://github.com/user-attachments/assets/02a3af61-747d-4f5d-b394-4f59fec1d0e8" />

Análisis modelos de LLM 
Herramientas:
HTOP
Coherencia en respuestas

docker model list

como puede apreciarse tenemos instalados dos modelos diferentes.

<img width="1611" height="996" alt="image" src="https://github.com/user-attachments/assets/fb8d5a8c-6e6a-45af-844b-07ee64ee251e" />

"""
MQTTMonitor: Servicio de monitoreo MQTT y almacenamiento en MongoDB

Este script define una clase `MQTTMonitor` que se suscribe a un topic MQTT, recibe datos
de sensores (temperatura y humedad), los guarda en una base de datos MongoDB y los deja
disponibles para ser consultados por otros módulos (por ejemplo, un analizador de alertas).

Requiere:
- Broker MQTT accesible
- Servidor MongoDB con autenticación
- Mensajes JSON con campos 'humedad' y 'temperatura_c'

Ejemplo de mensaje esperado:
{
    "temperatura_c": 22.5,
    "humedad": 55.0
}

Ejemplo de uso:
    monitor = MQTTMonitor()
    humedad, temperatura = monitor.get_data()
"""

import time
import json
import random
from datetime import datetime
import paho.mqtt.client as mqtt
from pymongo import MongoClient


class MQTTMonitor:
    """
    Clase que gestiona la suscripción a un broker MQTT y el almacenamiento en MongoDB.

    Métodos:
        get_data() -> tuple:
            Retorna la última lectura de humedad y temperatura si hay nuevos datos.

        close() -> None:
            Cierra las conexiones activas a MQTT y MongoDB.
    """

    def __init__(self, broker='192.168.10.175', port=1883, topic='cuartofrio/sensor'):
        """
        Inicializa el monitor MQTT y establece conexión con MongoDB.

        Parámetros:
            broker (str): Dirección IP del broker MQTT.
            port (int): Puerto de conexión al broker MQTT.
            topic (str): Topic al que suscribirse para recibir datos.

        Retorna:
            None
        """
        self.broker = broker
        self.port = port
        self.topic = topic

        # MongoDB autenticación y conexión
        mongo_user = "admin"
        mongo_pwd = "Grupac123*"
        mongo_host = "192.168.10.175"
        mongo_port = 27017
        mongo_db = "almacen_db"
        mongo_collection = "sensor_mqtt"

        mongo_uri = f"mongodb://{mongo_user}:{mongo_pwd}@{mongo_host}:{mongo_port}/"
        self.mongo_client = MongoClient(mongo_uri)
        self.db = self.mongo_client[mongo_db]
        self.collection = self.db[mongo_collection]

        # Configuración MQTT
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.broker, self.port, 60)
        self.client.loop_start()

        # Variables internas
        self.last_humedad = None
        self.last_temperatura_c = None
        self.new_data = False

    def on_connect(self, client, userdata, flags, rc):
        """
        Callback al establecer conexión con el broker.

        Suscribe al topic si la conexión es exitosa.

        Parámetros:
            client, userdata, flags, rc: parámetros de conexión MQTT

        Retorna:
            None
        """
        if rc == 0:
            print(f" Conectado al broker MQTT {self.broker}:{self.port}")
            self.client.subscribe(self.topic)
            print(f" Suscrito al topic: {self.topic}")
        else:
            print(f" Error de conexión MQTT: {rc}")

    def on_message(self, client, userdata, msg):
        """
        Callback que procesa los mensajes recibidos del topic MQTT.

        Extrae temperatura y humedad del mensaje JSON, inserta en MongoDB
        y actualiza los últimos valores.

        Parámetros:
            client, userdata, msg: parámetros del mensaje MQTT

        Retorna:
            None
        """
        try:
            line = msg.payload.decode('utf-8').strip()
            print(f" Datos recibidos: {line}")
            payload = json.loads(line)

            if 'humedad' in payload and 'temperatura_c' in payload:
                now = datetime.now()

                document = {
                    "sensor": "Sensor_A1",
                    "fecha": now.strftime("%d/%m/%Y"),
                    "hora": now.strftime("%H:%M:%S"),
                    "temperatura_c": float(payload['temperatura_c']),
                    "temperatura_f": round(float(payload['temperatura_c']) * 9 / 5 + 32, 2),
                    "humedad": float(payload['humedad']),
                    "rssi": random.randint(-70, -40),
                    "fecha_hora": now.isoformat(),
                    "ip": "192.168.1.133",
                    "ssid": "Robert-Wifi",
                    "mac": "48:E7:29:A6:0B:D4",
                    "firmware": "1.0.10",
                    "interval": 5000,
                    "name": "NCD-0BD4",
                    "timestamp": now.isoformat()
                }

                result = self.collection.insert_one(document)
                print(f" Insertado en MongoDB con _id: {result.inserted_id}")

                self.last_temperatura_c = float(payload['temperatura_c'])
                self.last_humedad = float(payload['humedad'])
                self.new_data = True
            else:
                print("  Error: faltan claves 'humedad' o 'temperatura_c'")
        except Exception as e:
            print(f" Error al procesar el mensaje: {e}")

    def get_data(self):
        """
        Retorna los últimos valores de humedad y temperatura si hay nuevos datos.

        Retorna:
            tuple (float | None, float | None): humedad, temperatura_c
        """
        if self.new_data:
            self.new_data = False
            return self.last_humedad, self.last_temperatura_c
        return None, None

    def close(self):
        """
        Cierra la conexión con el broker MQTT y con la base de datos MongoDB.

        Retorna:
            None
        """
        self.client.loop_stop()
        self.client.disconnect()
        self.mongo_client.close()
        print(" Conexión MQTT y MongoDB cerradas.")


# ------------------ MAIN ------------------
if __name__ == "__main__":
    monitor = MQTTMonitor()

    try:
        print(" Escuchando mensajes MQTT...")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n Deteniendo...")
        monitor.close()

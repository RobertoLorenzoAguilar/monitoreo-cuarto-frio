import time
import json
import paho.mqtt.client as mqtt

class MQTTMonitor:
    def __init__(self, broker='192.168.10.175', port=1883, topic='casa/temperatura'):
        self.broker = broker
        self.port = port
        self.topic = topic
        self.last_humedad = None
        self.last_temperatura_c = None
        self.new_data = False

        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.broker, self.port, 60)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print(f"Conectado al broker MQTT {self.broker}:{self.port}")
            self.client.subscribe(self.topic)
            print(f"Suscrito al topic: {self.topic}")
        else:
            print(f"Error de conexión MQTT: {rc}")

    def on_message(self, client, userdata, msg):
        try:
            line = msg.payload.decode('utf-8').strip()
            print(f"Datos recibidos: {line}")  # similar a monitor_arduino.py
            payload = json.loads(line)
            if 'humedad' in payload and 'temperatura_c' in payload:
                self.last_humedad = str(payload['humedad'])
                self.last_temperatura_c = str(payload['temperatura_c'])
                self.new_data = True
            else:
                print(f"Error: faltan claves 'humedad' o 'temperatura_c'")
        except Exception as e:
            print(f"Error al procesar el mensaje: {e}")

    def get_data(self):
        if self.new_data:
            self.new_data = False  # Reset bandera
            return self.last_humedad, self.last_temperatura_c
        return None, None

    def close(self):
        self.client.loop_stop()
        self.client.disconnect()

# Monitoreo continuo (similar estructura al de Arduino)
if __name__ == "__main__":
    monitor = MQTTMonitor()

    try:
        while True:
            humedad, temperatura_c = monitor.get_data()
            if humedad and temperatura_c:
                print(f"Lectura en tiempo real: Humedad = {humedad}%, Temperatura = {temperatura_c}°C")
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nCerrando conexión MQTT...")
        monitor.close()


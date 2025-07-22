from openai import OpenAI
import paho.mqtt.client as mqtt
import re
from datetime import datetime
import requests

# === Configuración MQTT ===
MQTT_BROKER = "192.168.10.175"
MQTT_PORT = 1883
MQTT_TOPIC = "cuartofrio/recomendaciones"

# === Configuración Telegram ===

help = 'Automatiza la asignación de requisiciones basadas en usuarios y empresas asignadas'

TOKEN = '6517578549:AAGV8R5CpgvtltIwaQTlG6V0kPN9dZSfxa8'
URL = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
PJ = 'TCA'
HOUR = datetime.now().strftime('%d-%m-%Y %H:%M:%S ')



# Crear cliente MQTT
mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)

# === Cliente del modelo local ===
client = OpenAI(
    base_url="http://localhost:12434/engines/v1",
    api_key="local-key"
)

# === Función para obtener la respuesta completa del modelo ===
def get_chat_completion(user_prompt):
    try:
        response = client.chat.completions.create(
            model="ai/llama3.2:3B-Q4_0",
            messages=[{"role": "user", "content": user_prompt}],
            max_tokens=1500,
            stream=False  # Asegurarse de obtener el texto completo
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error al generar recomendación: {e}")
        return ""

# === Función principal para procesar alertas y publicar MQTT ===
def execute_action(alert_messages, correcto):
    if (correcto ==False):
        print(f"Mensajes recibidos: {alert_messages}")

        humedad, temperatura = valor_parametro(alert_messages[0])

        user_prompt = f"""
        Eres un experto en bioseguridad y conservación de vacunas veterinarias. Estás monitoreando un cuarto frío con sensores de temperatura y humedad.

        Se recibieron las siguientes alertas:
        {chr(10).join(alert_messages)}

        Valores actuales:
        - Temperatura: {temperatura} °C
        - Humedad: {humedad} %

        Evalúa la situación y proporciona recomendaciones técnicas para corregir cualquier problema detectado.
        """

        advice = get_chat_completion(user_prompt)

        if advice:
            print(f"\n Recomendación generada:\n{advice}\n")
            mqtt_client.publish(MQTT_TOPIC, advice)
            print(f"Recomendación publicada en MQTT: {MQTT_TOPIC}")
        else:
            print("No se pudo generar una recomendación. No se publicará nada.")

        for alert in alert_messages:
            envio_mensaje_grupo_telegram(alert)
            # if "Temperatura fuera de rango" in alert:
            #     print("Ejecutando acción para controlar la temperatura...")
            #     envio_mensaje_grupo_telegram(alert)
            #     print("Ejecutando acción genérica...")
            # elif "Humedad fuera de rango" in alert:
            #     print("Ejecutando acción para ajustar la humedad...")
            # else:
            #     pass
    else:
        print("Sin recomendaciones hasta el momento...")
        mqtt_client.publish(MQTT_TOPIC, "Sin recomendaciones hasta el momento...")
        

# === Extraer humedad y temperatura de la alerta ===
def valor_parametro(mensaje):
    coincidencia = re.search(r'humedad:\(([^)]+)\).*temperatura:\s*\(([^)]+)\)', mensaje)
    if coincidencia:
        return float(coincidencia.group(1)), float(coincidencia.group(2))
    else:
        print(" No se encontraron valores de humedad/temperatura.")
        return None, None
    
def envio_mensaje_grupo_telegram(message):
    # curl -X POST "https://api.telegram.org/bot7566541429:AAECRitrvyX35x53dLsUV3-etEqVPAHnTB8/sendMessage" -d "chat_id=-4813338698&text=Mensaje a Telegra Canal"

    # Replace with your bot token and chat ID
    bot_token = '7566541429:AAECRitrvyX35x53dLsUV3-etEqVPAHnTB8'
    chat_id = '-4813338698'  # For channels, use the chat ID with a leading negative sign   

    # Send the message
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print("Message sent successfully!")
    else:
        print("Failed to send message:", response.json())
        

# === Ejemplo de ejecución directa ===
if __name__ == "__main__":
    alertas = [
        "Alerta de humedad fuera de rango humedad:(67.5) temperatura: (9.1) - Nivel crítico",
        "Alerta de temperatura fuera de rango humedad:(67.5) temperatura: (9.1) - Nivel crítico"
    ]
    execute_action(alertas)

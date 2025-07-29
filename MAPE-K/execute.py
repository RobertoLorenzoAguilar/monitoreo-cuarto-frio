"""
Executor: Procesador de alertas, generación de recomendaciones técnicas
y envío de mensajes vía MQTT y Telegram.

Este módulo:
- Recibe alertas de sensores (temperatura/humedad).
- Extrae los valores actuales de las alertas.
- Genera recomendaciones técnicas usando un modelo LLM local.
- Publica las recomendaciones por MQTT.
- Envía las alertas por Telegram a un canal.

Requisitos:
- Servidor LLM local compatible con OpenAI API (como llama.cpp o Ollama)
- Broker MQTT y canal de Telegram configurados

Ejemplo de uso:
    if __name__ == "__main__":
        alertas = [
            "Alerta de humedad fuera de rango humedad:(67.5) temperatura: (9.1) - Nivel crítico"
        ]
        execute_action(alertas)
"""

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
# Token y chat_id deben mantenerse confidenciales
TOKEN = '£££££££££££££££££££££££££££££££££££££££££££'
URL = f'https://api.telegram.org/bot{TOKEN}/sendMessage'

# === Cliente MQTT ===
mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)

# === Cliente del modelo local (llama.cpp, Ollama, etc.) ===
client = OpenAI(
    base_url="http://localhost:12434/engines/v1",
    api_key="local-key"  # Dummy key para motores locales
)

def get_chat_completion(user_prompt: str) -> str:
    """
    Solicita una respuesta al modelo LLM local.

    Args:
        user_prompt (str): Instrucción completa enviada al modelo.

    Returns:
        str: Respuesta generada por el modelo o cadena vacía si hay error.
    """
    try:
        response = client.chat.completions.create(
            model="ai/llama3.2:3B-Q4_0",
            messages=[{"role": "user", "content": user_prompt}],
            max_tokens=1500,
            stream=False
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error al generar recomendación: {e}")
        return ""

def execute_action(alert_messages: list[str], correcto: bool = False):
    """
    Procesa las alertas y genera recomendaciones técnicas si corresponde.

    Args:
        alert_messages (list[str]): Lista de mensajes de alerta recibidos.
        correcto (bool): Indica si todo está en orden. Si es True, no se genera recomendación.

    Returns:
        None
    """
    if not correcto:
        print(f"Mensajes recibidos: {alert_messages}")

        # Extrae valores desde el primer mensaje
        humedad, temperatura = valor_parametro(alert_messages[0])

        # Prepara el prompt para el modelo
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
    else:
        print("Sin recomendaciones hasta el momento...")
        mqtt_client.publish(MQTT_TOPIC, "Sin recomendaciones hasta el momento...")

def valor_parametro(mensaje: str) -> tuple[float | None, float | None]:
    """
    Extrae valores numéricos de humedad y temperatura de un mensaje de alerta.

    Args:
        mensaje (str): Cadena con el formato: '...humedad:(xx.x) temperatura:(yy.y)...'

    Returns:
        tuple: (humedad, temperatura) como floats o (None, None) si no se encuentran.
    """
    coincidencia = re.search(r'humedad:\(([^)]+)\).*temperatura:\s*\(([^)]+)\)', mensaje)
    if coincidencia:
        return float(coincidencia.group(1)), float(coincidencia.group(2))
    else:
        print(" No se encontraron valores de humedad/temperatura.")
        return None, None

def envio_mensaje_grupo_telegram(message: str):
    """
    Envía un mensaje a un grupo o canal de Telegram usando un bot.

    Args:
        message (str): Texto del mensaje a enviar.

    Returns:
        None
    """ 
    bot_token = '£££££££££££££££££££££££££££££££££££££££££££'  # poner el tokem del bot propio
    chat_id = '-£££££££££££££££'  # Canal o grupo de destino
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    payload = {
        'chat_id': chat_id,
        'text': message
    }

    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print("Mensaje enviado a Telegram correctamente.")
    else:
        print("Error al enviar mensaje a Telegram:", response.json())

# === Ejemplo de ejecución directa ===
if __name__ == "__main__":
    alertas = [
        "Alerta de humedad fuera de rango humedad:(67.5) temperatura: (9.1) - Nivel crítico",
        "Alerta de temperatura fuera de rango humedad:(67.5) temperatura: (9.1) - Nivel crítico"
    ]
    execute_action(alertas)

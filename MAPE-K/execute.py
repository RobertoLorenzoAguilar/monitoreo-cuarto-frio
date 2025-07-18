from openai import OpenAI
import paho.mqtt.client as mqtt
import re

# === Configuración MQTT ===
MQTT_BROKER = "192.168.10.175"         # Cambiar si tu broker está en otro host
MQTT_PORT = 1883                  # O 9001 si usas WebSocket
MQTT_TOPIC = "cuartofrio/recomendaciones"

# Crear cliente MQTT y conectar
mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)

# === Cliente del modelo local ===
client = OpenAI(
    base_url="http://localhost:12434/engines/v1",
    api_key="local-key"
)

# === Función para obtener la respuesta del modelo local ===
def get_chat_completion(user_prompt):
    response = client.chat.completions.create(
        model="ai/llama3.2:3B-Q4_0",
        messages=[{"role": "user", "content": user_prompt}],
        max_tokens=150,
    )
    return response.choices[0].message.content.strip()

# === Función principal para procesar alertas y publicar ===
def execute_action(alert_messages):
    print(f"Mensajes recibidos: {alert_messages}")

    # Usar la primera alerta para extraer valores
    humedad, temperatura = valor_parametro(alert_messages[0])

    # Consolidar el mensaje para el modelo
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
    print(f"Respuesta del modelo local:\n{advice}")

    # Publicar el consejo por MQTT
    mqtt_client.publish(MQTT_TOPIC, advice)
    print(f"Consejo publicado a MQTT topic '{MQTT_TOPIC}'")

    # Acciones automáticas según tipo de alerta
    for alert in alert_messages:
        if "Temperatura fuera de rango" in alert:
            print("Ejecutando acción para controlar la temperatura...")
        elif "Humedad fuera de rango" in alert:
            print("Ejecutando acción para ajustar la humedad...")
        else:
            print("Ejecutando acción genérica...")

# === Función para extraer humedad y temperatura de la alerta ===
def valor_parametro(mensaje):
    coincidencia = re.search(r'humedad:\(([^)]+)\).*temperatura:\s*\(([^)]+)\)', mensaje)
    if coincidencia:
        valor_humedad = float(coincidencia.group(1))
        valor_temperatura = float(coincidencia.group(2))
        return valor_humedad, valor_temperatura
    else:
        print("No se encontraron los valores.")
        return None, None

# === Ejemplo de uso ===
if __name__ == "__main__":
    alertas = [
        "Alerta de humedad fuera de rango humedad:(67.5) temperatura: (9.1) - Nivel crítico",
        "Alerta de temperatura fuera de rango humedad:(67.5) temperatura: (9.1) - Nivel crítico"
    ]
    execute_action(alertas)

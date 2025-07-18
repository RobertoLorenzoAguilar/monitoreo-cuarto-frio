from openai import OpenAI
import paho.mqtt.client as mqtt
import re

# === Configuración MQTT ===
MQTT_BROKER = "192.168.10.175"
MQTT_PORT = 1883
MQTT_TOPIC = "cuartofrio/recomendaciones"

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
def execute_action(alert_messages):
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
        print(f"\n✅ Recomendación generada:\n{advice}\n")
        mqtt_client.publish(MQTT_TOPIC, advice)
        print(f"📡 Recomendación publicada en MQTT: {MQTT_TOPIC}")
    else:
        print("⚠️ No se pudo generar una recomendación. No se publicará nada.")

    for alert in alert_messages:
        if "Temperatura fuera de rango" in alert:
            print("⚙️ Ejecutando acción para controlar la temperatura...")
        elif "Humedad fuera de rango" in alert:
            print("⚙️ Ejecutando acción para ajustar la humedad...")
        else:
            print("⚙️ Ejecutando acción genérica...")

# === Extraer humedad y temperatura de la alerta ===
def valor_parametro(mensaje):
    coincidencia = re.search(r'humedad:\(([^)]+)\).*temperatura:\s*\(([^)]+)\)', mensaje)
    if coincidencia:
        return float(coincidencia.group(1)), float(coincidencia.group(2))
    else:
        print("❌ No se encontraron valores de humedad/temperatura.")
        return None, None

# === Ejemplo de ejecución directa ===
if __name__ == "__main__":
    alertas = [
        "Alerta de humedad fuera de rango humedad:(67.5) temperatura: (9.1) - Nivel crítico",
        "Alerta de temperatura fuera de rango humedad:(67.5) temperatura: (9.1) - Nivel crítico"
    ]
    execute_action(alertas)

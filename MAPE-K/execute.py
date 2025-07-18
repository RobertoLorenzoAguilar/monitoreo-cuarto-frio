from openai import OpenAI

# Crear cliente para modelo local en localhost
client = OpenAI(
    base_url="http://localhost:12434/engines/v1",  # Asegúrate que el endpoint es correcto
    api_key="local-key"
)

# Función para obtener la respuesta del modelo local
def get_chat_completion(user_prompt):
    response = client.chat.completions.create(
        model="ai/llama3.2:3B-Q4_0",  # O el nombre exacto que muestra en localhost:12434/v1/models
        messages=[{"role": "user", "content": user_prompt}],
        max_tokens=150,
    )
    return response.choices[0].message.content.strip()

# Función para ejecutar acción basada en alerta
def execute_action(alert_message):
    print(f"Mensaje recibido: {alert_message}")

    user_prompt = f"""
    Eres un experto en bioseguridad y conservación de vacunas veterinarias. Estás monitoreando un cuarto frío con sensores de temperatura y humedad.

    Alerta recibida: {alert_message}

    Evalúa la situación y proporciona recomendaciones técnicas para corregir cualquier problema detectado.
    """
    advice = get_chat_completion(user_prompt)

    print(f"Respuesta del modelo local: {advice}")

    # Acciones automáticas según tipo de alerta
    if "Temperatura fuera de rango" in alert_message:
        print("Ejecutando acción para controlar la temperatura...")
    elif "Humedad fuera de rango" in alert_message:
        print("Ejecutando acción para ajustar la humedad...")
    else:
        print("Ejecutando acción genérica...")

    # Simulación de alerta
    sensor_data = {
        "temperatura": 9.2,
        "humedad": 65
    }

    alerta = f"Temperatura: {sensor_data['temperatura']} °C, Humedad: {sensor_data['humedad']} %"
    execute_action(alerta)




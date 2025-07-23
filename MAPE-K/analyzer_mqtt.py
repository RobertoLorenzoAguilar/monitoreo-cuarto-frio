"""
Analizador de condiciones ambientales (temperatura y humedad) con reglas externas.

Este script define una clase `Analyzer` que evalúa datos obtenidos por MQTT en tiempo real
y genera alertas si los valores de temperatura o humedad se encuentran fuera de los rangos definidos.

Uso de ejemplo:

1. Crear un archivo de reglas llamado `k.txt` con el siguiente formato por línea:
    humedad,30,60,Alta humedad
    temperatura,15,25,Frío o Calor extremo

2. Ejecutar el script directamente:
    python analyzer_mqtt.py

Esto iniciará un análisis continuo cada 5 segundos.

El script depende de un monitor MQTT (`monitor_mqtt.MQTTMonitor`) que debe implementar el método `get_data()`
y retornar una tupla `(humedad: float, temperatura: float)`.
"""

import time
from monitor_mqtt import MQTTMonitor


class Analyzer:
    class Rule:
        """
        Clase interna que representa una regla de validación de un parámetro ambiental.

        Atributos:
            feature (str): Nombre del parámetro (por ejemplo: 'humedad' o 'temperatura').
            lower (float): Límite inferior permitido.
            upper (float): Límite superior permitido.
            alarm (str): Mensaje de alarma asociado.

        Métodos:
            is_triggered(value: float) -> bool:
                Retorna True si el valor está fuera del rango permitido.
        """
        def __init__(self, feature: str, lower: float, upper: float, alarm: str):
            self.feature = feature.lower()
            self.lower = lower
            self.upper = upper
            self.alarm = alarm

        def is_triggered(self, value: float) -> bool:
            """
            Evalúa si el valor está fuera del rango definido.

            Parámetros:
                value (float): Valor actual del parámetro.

            Retorna:
                bool: True si se dispara la alerta (fuera de rango), False en caso contrario.
            """
            return not (self.lower <= value <= self.upper)

    def __init__(self, rules_file: str = "k.txt"):
        """
        Inicializa el analizador cargando reglas desde un archivo.

        Parámetros:
            rules_file (str): Ruta del archivo de reglas. Por defecto es 'k.txt'.

        Retorna:
            None
        """
        self.rules_file = rules_file
        self.rules = self._load_rules()
        self.monitor = MQTTMonitor()

    def _load_rules(self) -> list:
        """
        Carga y parsea las reglas desde el archivo especificado.

        Formato esperado de cada línea:
            parametro,min,max,mensaje

        Retorna:
            list[Rule]: Lista de objetos Rule válidos.
        """
        rules = []
        with open(self.rules_file, 'r') as file:
            for line in file:
                line = line.strip().strip('[]')
                elements = line.split(',')
                if len(elements) == 4:
                    feature = elements[0].strip().lower()
                    lower = float(elements[1].strip())
                    upper = float(elements[2].strip())
                    alarm = elements[3].strip()
                    rules.append(Analyzer.Rule(feature, lower, upper, alarm))
        return rules

    def analyze(self) -> list:
        """
        Ejecuta el análisis de las condiciones ambientales actuales.

        Recupera datos desde MQTT, los compara con las reglas cargadas
        y genera una lista de alertas si hay parámetros fuera de rango.

        Retorna:
            list[str]: Lista de mensajes de alerta. Vacía si no hay alertas.
        """
        humedad, temperature = self.monitor.get_data()

        if humedad is None or temperature is None:
            return []

        alerts = []
        for rule in self.rules:
            if rule.feature == "humedad":
                if rule.is_triggered(humedad):
                    alerts.append(
                        f"Alerta de {rule.feature} fuera de rango humedad:({humedad}) temperatura: ({temperature}) - {rule.alarm}"
                    )
            if rule.feature == "temperatura":
                if rule.is_triggered(temperature):
                    alerts.append(
                        f"Alerta de {rule.feature} fuera de rango humedad:({humedad}) temperatura: ({temperature}) - {rule.alarm}"
                    )
        return alerts


# ---------------- MAIN ------------------
if __name__ == "__main__":
    analyzer = Analyzer("k.txt")

    print("Iniciando análisis continuo de condiciones...\nPresiona Ctrl+C para detener.\n")
    try:
        while True:
            alerts = analyzer.analyze()
            for alert in alerts:
                print(alert)
            time.sleep(5)  # Espera 5 segundos antes del siguiente análisis
    except KeyboardInterrupt:
        print("\nAnálisis detenido por el usuario.")

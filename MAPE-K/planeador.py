# planner.py
from analyzer_mqtt import Analyzer
import execute
import time


def plan_actions():
    analyzer = Analyzer()

    while True:
        # Analiza las alertas
        alerts = analyzer.analyze()

        if alerts:
            print(f"Alertas activadas: {alerts}")
            for alert in alerts:
                # Esperar antes de realizar la siguiente consulta a la API
                # time.sleep(10)  # Espera 10 segundos antes de la siguiente pregunta
                execute.execute_action(alert)  # Pasa la alerta al ejecutor
                # Salimos del bucle si una alerta activa una acción
                return
        else:
            print(" Todo en orden, sin alertas.")
            execute.execute_action("Todo bien")  # Si no hay alertas, todo está bien

        # Esperar un poco antes de volver a analizar
        time.sleep(5)  # Puedes ajustar este valor dependiendo de la frecuencia de monitoreo


if __name__ == "__main__":
    plan_actions()

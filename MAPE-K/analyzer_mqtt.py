import time
from monitor_mqtt import MQTTMonitor


class Analyzer:
    class Rule:
        def __init__(self, feature: str, lower: float, upper: float, alarm: str):
            self.feature = feature.lower()
            self.lower = lower
            self.upper = upper
            self.alarm = alarm

        def is_triggered(self, value: float) -> bool:
            return not (self.lower <= value <= self.upper)

    def __init__(self, rules_file: str = "k.txt"):
        self.rules_file = rules_file
        self.rules = self._load_rules()
        self.monitor = MQTTMonitor()

    def _load_rules(self):
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

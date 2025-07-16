from monitor_mqtt import MQTTMonitor

class Analyzer:
    class Rule:
        def __init__(self, feature: str, lower: float, upper: float, alarm: str):
            self.feature = feature.lower()  # Asegúrate de que la característica esté en minúsculas
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
                line = line.strip().strip('[]')  # Remove brackets and extra whitespace
                elements = line.split(',')
                if len(elements) == 4:
                    feature = elements[0].strip().lower()  # Usamos minúsculas
                    lower = float(elements[1].strip())
                    upper = float(elements[2].strip())
                    alarm = elements[3].strip()
                    rules.append(Analyzer.Rule(feature, lower, upper, alarm))
        return rules

    def analyze(self) -> list:
        humedad, temperature = self.monitor.get_data()  # Obtener los datos de humedad y temperatura_c
        if not humedad or not temperature:
            return []

        # Eliminar el sufijo '%' de la humedad y convertir a float
        if '%' in humedad:
            humedad = humedad.replace('%', '').strip()

        # Eliminar el sufijo 'C' de la temperatura_c y convertir a float
        if 'C' in temperature:
            temperature = temperature.replace('C', '').strip()

        alerts = []
        # Verificar si la humedad está fuera de rango
        for rule in self.rules:
            if rule.feature == "humedad":  # Comparación en minúsculas
                if rule.is_triggered(float(humedad)):
                    alerts.append(f"Alerta Humedad en Vacunas veterinarias sensor en hielera DH11: {rule.feature} fuera de rango ({humedad}) - {rule.alarm}")
            elif rule.feature == "temperatura_c":  # Comparación en minúsculas
                if rule.is_triggered(float(temperature)):
                    alerts.append(f"Alerta Humedad en Vacunas veterinarias sensor en temperatura_cuarto DH11: {rule.feature} fuera de rango ({temperature}) - {rule.alarm}")

        return alerts

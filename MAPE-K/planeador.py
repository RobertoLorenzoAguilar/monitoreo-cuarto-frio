#Cómo Usar el Servicio
#Ejecutar en primer plano (para pruebas):
#python script.py --interval 10 --log-file my_service.log
#Esto ejecuta el servicio con un intervalo de 10 segundos y guarda logs en my_service.log.
#Ejecutar como daemon (en segundo plano):
#python script.py --interval 10 --log-file my_service.log --daemon
#El servicio se ejecuta en segundo plano. Los logs se guardan en my_service.log.
#El archivo PID se crea en /tmp/analyzer_service.pid.
#Detener el servicio:
#Encuentra el PID del proceso en /tmp/analyzer_service.pid y mátalo:
#kill $(cat /tmp/analyzer_service.pid)

import argparse
import daemon
import daemon.pidfile
import logging
import os
import time
import sys
from analyzer_mqtt import Analyzer
import execute
import lockfile


# Configuración del logger
def setup_logging(log_file):
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )


def plan_actions(interval, log_file):
    setup_logging(log_file)
    logging.info("Servicio iniciado")

    analyzer = Analyzer()

    while True:
        try:
            # Analiza las alertas
            alerts = analyzer.analyze()

            if alerts:
                logging.info(f"Alertas activadas: {alerts}")
                execute.execute_action(alerts, False)
            else:
                logging.info("Todo en orden, sin alertas.")
                execute.execute_action(alerts, True)

            time.sleep(interval)
        except Exception as e:
            logging.error(f"Error en el servicio: {e}")
            time.sleep(interval)  # Continúa incluso si hay errores


def run_service(args):
    if args.daemon:
        # Configuración para ejecutar como daemon
        pid_file = "/tmp/analyzer_service.pid"
        context = daemon.DaemonContext(
            working_directory=os.getcwd(),
            umask=0o002,
            pidfile=lockfile.FileLock(pid_file),
            stdout=open(args.log_file, 'a'),
            stderr=open(args.log_file, 'a')
        )

        with context:
            logging.info("Iniciando servicio en modo daemon")
            plan_actions(args.interval, args.log_file)
    else:
        # Ejecutar en primer plano
        plan_actions(args.interval, args.log_file)


def main():
    parser = argparse.ArgumentParser(description="Servicio de análisis de alertas MQTT")
    parser.add_argument(
        '--interval',
        type=int,
        default=5,
        help='Intervalo de monitoreo en segundos (default: 5)'
    )
    parser.add_argument(
        '--log-file',
        type=str,
        default='analyzer_service.log',
        help='Archivo donde se guardarán los logs (default: analyzer_service.log)'
    )
    parser.add_argument(
        '--daemon',
        action='store_true',
        help='Ejecutar el servicio en segundo plano como daemon'
    )

    args = parser.parse_args()
    run_service(args)


if __name__ == "__main__":
    main()
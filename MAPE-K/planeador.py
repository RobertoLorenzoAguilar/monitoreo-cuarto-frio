"""
Servicio de análisis de alertas MQTT

Este script permite ejecutar un servicio que analiza mensajes MQTT periódicamente
y ejecuta acciones si detecta alertas. Puede ejecutarse en primer plano (para pruebas)
o en segundo plano como un daemon.

Modo de uso:

- Ejecutar en primer plano:
    python planeador.py --interval 10 --log-file my_service.log

  Ejecuta el servicio con un intervalo de 10 segundos. Los logs se escriben en `my_service.log`.

- Ejecutar como daemon (segundo plano):
    python planeador.py --interval 10 --log-file my_service.log --daemon

  Ejecuta el servicio en segundo plano. El archivo de logs se mantiene actualizado
  y se genera un archivo PID en `/tmp/analyzer_service.pid`.

- Detener el servicio:
    kill $(cat /tmp/analyzer_service.pid)
"""

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


def setup_logging(log_file):
    """
    Configura el sistema de logging para registrar eventos del servicio.

    Parámetros:
        log_file (str): Ruta al archivo donde se almacenarán los logs.

    Retorna:
        None
    """
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )


def plan_actions(interval, log_file):
    """
    Ejecuta el ciclo principal del servicio: analiza alertas y ejecuta acciones.

    Parámetros:
        interval (int): Intervalo de tiempo en segundos entre cada análisis.
        log_file (str): Ruta al archivo de logs.

    Retorna:
        None

    Ejemplo:
        plan_actions(10, 'my_service.log')
    """
    setup_logging(log_file)
    logging.info("Servicio iniciado")

    analyzer = Analyzer()

    while True:
        try:
            # Analiza las alertas a través del analizador MQTT
            alerts = analyzer.analyze()

            if alerts:
                logging.info(f"Alertas activadas: {alerts}")
                execute.execute_action(alerts, False)
            else:
                logging.info("Todo en orden, sin alertas.")
                execute.execute_action(alerts, True)

            time.sleep(interval)

        except Exception as e:
            # Si ocurre un error, se registra pero no detiene el servicio
            logging.error(f"Error en el servicio: {e}")
            time.sleep(interval)


def run_service(args):
    """
    Ejecuta el servicio de acuerdo con los argumentos proporcionados.

    Parámetros:
        args (argparse.Namespace): Argumentos parseados desde la línea de comandos.

    Retorna:
        None
    """
    if args.daemon:
        # Ejecutar el servicio en segundo plano (modo daemon)
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
        # Ejecutar el servicio en primer plano (modo desarrollo/prueba)
        plan_actions(args.interval, args.log_file)


def main():
    """
    Punto de entrada principal del script.

    Procesa los argumentos de línea de comandos y lanza el servicio.

    Retorna:
        None
    """
    parser = argparse.ArgumentParser(description="Servicio de análisis de alertas MQTT")

    parser.add_argument(
        '--interval',
        type=int,
        default=5,
        help='Intervalo de monitoreo en segundos (por defecto: 5)'
    )

    parser.add_argument(
        '--log-file',
        type=str,
        default='analyzer_service.log',
        help='Archivo donde se guardarán los logs (por defecto: analyzer_service.log)'
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

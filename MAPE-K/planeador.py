import argparse
import os
import sys
import time
from analyzer_mqtt import Analyzer
import execute

PID_FILE = "/tmp/planner_service.pid"

def plan_actions():
    analyzer = Analyzer()

    while True:
        try:
            alerts = analyzer.analyze()
            if alerts:
                print(f"Alertas activadas: {alerts}")
                execute.execute_action(alerts, False)
            else:
                execute.execute_action(alerts, True)
            time.sleep(5)  # Adjustable monitoring frequency
        except KeyboardInterrupt:
            print("Stopping planner service...")
            sys.exit(0)

def start_service():
    if os.path.exists(PID_FILE):
        with open(PID_FILE, 'r') as f:
            pid = f.read().strip()
        print(f"Service already running with PID {pid}")
        sys.exit(1)

    print("Starting planner service in background...")
    # Fork the process to run in the background
    if os.fork() > 0:
        sys.exit(0)  # Exit parent process

    # Detach from terminal
    os.setsid()
    if os.fork() > 0:
        sys.exit(0)  # Exit second parent process

    # Redirect stdout and stderr to log files
    with open('planner_service.log', 'a') as log, open('planner_service_err.log', 'a') as err_log:
        os.dup2(log.fileno(), sys.stdout.fileno())
        os.dup2(err_log.fileno(), sys.stderr.fileno())

    # Write PID to file
    with open(PID_FILE, 'w') as f:
        f.write(str(os.getpid()))

    plan_actions()

def stop_service():
    if not os.path.exists(PID_FILE):
        print("Service is not running.")
        sys.exit(1)

    with open(PID_FILE, 'r') as f:
        pid = f.read().strip()

    try:
        os.kill(int(pid), 15)  # Send SIGTERM
        os.remove(PID_FILE)
        print(f"Service with PID {pid} stopped.")
    except ProcessLookupError:
        print("Service PID not found. Cleaning up.")
        os.remove(PID_FILE)
    except Exception as e:
        print(f"Error stopping service: {e}")
        sys.exit(1)

def status_service():
    if os.path.exists(PID_FILE):
        with open(PID_FILE, 'r') as f:
            pid = f.read().strip()
        print(f"Service is running with PID {pid}")
    else:
        print("Service is not running.")

def main():
    parser = argparse.ArgumentParser(description="Planner Service CLI")
    parser.add_argument('command', choices=['start', 'stop', 'status'],
                        help="Command to execute: start, stop, or status")
    args = parser.parse_args()

    if args.command == 'start':
        start_service()
    elif args.command == 'stop':
        stop_service()
    elif args.command == 'status':
        status_service()

if __name__ == "__main__":
    main()
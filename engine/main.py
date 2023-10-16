import os
import psutil
import socket
import time
import csv
from tabulate import tabulate

def resolve_domain(ip):
    try:
        domain = socket.gethostbyaddr(ip)
        return domain[0]
    except socket.herror:
        return "N/A"

def scan_and_save_connections(interval=1):
    active_connections = set()  # Usamos un conjunto para evitar duplicados
    log_file = 'data/connections.csv'

    while True:
        external_connections = []

        for conn in psutil.net_connections(kind='inet'):
            if conn.raddr and conn.raddr.ip != '127.0.0.1':
                remote_ip = conn.raddr.ip

                if remote_ip not in active_connections:
                    active_connections.add(remote_ip)

                    pid = conn.pid or "N/A"
                    if pid != "N/A":
                        pid = int(pid)
                    remote_port = conn.raddr.port

                    # Comprobar si el PID es un entero
                    if isinstance(pid, int):
                        process_name = psutil.Process(pid).name()
                    else:
                        process_name = "N/A"

                    domain = resolve_domain(remote_ip)
                    connection_info = [remote_ip, domain, remote_port, process_name]
                    external_connections.append(connection_info)

        if external_connections:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(tabulate(external_connections, headers=['IP', 'Nombre de dominio', 'Puerto', 'Proceso'], tablefmt='grid'))

            # Guardar las conexiones activas en el archivo CSV de registro
            with open(log_file, mode='a', newline='') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerows(external_connections)

        time.sleep(interval)

if __name__ == '__main__':
    scan_and_save_connections()
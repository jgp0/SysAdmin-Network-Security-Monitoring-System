import psutil
import csv
import time

# Función para obtener el tráfico de red para cada proceso
def obtener_trafico_de_red():
    conexiones = psutil.net_connections(kind='inet')
    trafico_por_proceso = {}

    for conexion in conexiones:
        pid = conexion.pid
        if pid is not None:
            proceso = psutil.Process(pid)
            nombre_proceso = proceso.name()
            if nombre_proceso in trafico_por_proceso:
                trafico = trafico_por_proceso[nombre_proceso]
            else:
                trafico = {'Enviado (bytes)': 0, 'Recibido (bytes)': 0}

            trafico['Enviado (bytes)'] += conexion.sent
            trafico['Recibido (bytes)'] += conexion.recv
            trafico_por_proceso[nombre_proceso] = trafico

    return trafico_por_proceso

# Función para guardar los datos en un archivo CSV
def guardar_en_csv(trafico_por_proceso, ruta_csv):
    with open(ruta_csv, mode='w', newline='') as archivo_csv:
        campos = ['Proceso', 'Enviado (bytes)', 'Recibido (bytes)']
        escritor_csv = csv.DictWriter(archivo_csv, fieldnames=campos)
        escritor_csv.writeheader()

        for proceso, trafico in trafico_por_proceso.items():
            escritor_csv.writerow({
                'Proceso': proceso,
                'Enviado (bytes)': trafico['Enviado (bytes)'],
                'Recibido (bytes)': trafico['Recibido (bytes)']
            })

if __name__ == "__main__":
    ruta_csv = 'trafico_de_red.csv'

    try:
        while True:
            trafico_por_proceso = obtener_trafico_de_red()
            guardar_en_csv(trafico_por_proceso, ruta_csv)
            print("Datos guardados en", ruta_csv)
            time.sleep(5)  # Intervalo de tiempo entre mediciones (5 segundos)
    except KeyboardInterrupt:
        print("Monitoreo de red finalizado.")
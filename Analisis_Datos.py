import numpy as np
import pandas as pd
import glob
import matplotlib.pyplot as plt
directory_path = 'Datos/'

# Listado de los archivos .txt en el directorio
file_paths = glob.glob(directory_path + '*.txt')

# Constantes para el calculo
Target = (192.1, -49.7)
L = 230.7472

# Configurar el plot
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))
fig.suptitle('Comparacion de Velocidad en Y vs Tiempo y Distancia vs Tiempo para varias alturas')


for file_path in file_paths:

    # Leer datos de el archivo
    data = pd.read_csv(file_path, header=None, usecols=[0, 2, 3], names=['time', 'y', 'z'])

    # Calcular velocidad
    data["delta_y"] = data["y"].diff()
    data["delta_t"] = data["time"].diff()
    data["Vy"] = data["delta_y"] / data["delta_t"]



    # Calcular punto de impacto
    t = np.sqrt(2 * (data['z'][1]- Target[1] - L) / (9.81 * 1000))
    data["Impacto"] = data["Vy"] * t + data["y"]

    # Preparar el nombre del archivo para exportar
    file_name = file_path.split('/')[-1].replace('.txt', '')

    # Plot Velocidad en Y vs Tiempo
    ax1.plot(data['time'], data['Vy'], label=f'{file_name} Vy(t)')
    ax1.set_xlabel('Tiempo (s)')
    ax1.set_ylabel('Velocidad (mm/s)')
    ax1.legend(loc='best')
    ax1.grid(True)

    # Plot Y vs Tiempo
    ax2.plot(data['time'], data['y'], label=f'{file_name} Y(t)')
    ax2.set_xlabel('Tienpo (s)')
    ax2.set_ylabel('Y (mm)')
    ax2.legend(loc='best')
    ax2.grid(True)

    #Exportar cada dataframe a un archivo con su respectiva altura
    output_csv = f'{file_name}.csv'
    data.to_csv(output_csv, index=False)

    print(f'Datos procesados y guardados como {output_csv}')

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()
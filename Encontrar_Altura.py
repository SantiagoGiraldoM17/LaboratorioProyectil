import pandas as pd
import numpy as np

# Constants
Target = (192.1, -49.7) #Coordenadas (y,z) del objetivo
g = 9.81 * 1000  # Gravedad en mm/s^2
L = 230.7472 #

# Cargar datos
file_path = 'Datos/horLine_z_0380__y-900_y900_t_xyz.txt' 
data = pd.read_csv(file_path, header=None, usecols=[0, 2], names=['time', 'y'])

# Calculos de Velocidad
data["delta_y"] = data["y"].diff()
data["delta_t"] = data["time"].diff()
data["Vy"] = data["delta_y"] / data["delta_t"]

def check_d_within_range(z, target, tolerance):
    """Calcular el impacto para una altura(z) dada y revisar si algun valor en el rango [29:33] concuerda con el deseado dentro de una tolerancia"""
    t = np.sqrt(2 * (z - Target[1] - L) / g)  # Calcular el tiempo de caida del objeto dado una altura
    data["Impacto"] = data["Vy"] * t + data["y"]  # Calcular las coordenadas de impacto para todos los instantes de tiempo
    # Revisar si algun valor dentro del rango [29:34] coincide con el deseado
    impact_range = data["Impacto"].iloc[29:34]
    valid_indices = impact_range[abs(impact_range - target) <= tolerance].index
    if not valid_indices.empty:
        return True, valid_indices[0] 
    return False, None

# Parametros para el calculo
desired_impact = Target[0]
min_z = 380
max_z = 1180
tolerance = 0.02

for z in np.arange(min_z, max_z + 1, 0.1):  # Increment z by 0.1 in each iteration
    result, index = check_d_within_range(z, desired_impact, tolerance)
    if result:
        print(f"Se encontro z: {z} donde el impacto es: {data["Impacto"].iloc[index]}, soltandolo a {data['time'].iloc[index]}s")
        break
else:
    print("No se encontro valores de z en el rango que cumplan la condicion")


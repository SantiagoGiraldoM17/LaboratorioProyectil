import pandas as pd
import numpy as np

#Leer uno de los archivos de texto para datos de tiempo y coordenada 'y'
file_path = 'Datos/horLine_z_0380__y-900_y900_t_xyz.txt'
data = pd.read_csv(file_path, header=None, usecols=[0, 2], names=['time', 'y'])

#Establecer constantes
Target = (192.1, -49.7) #Coordenadas (y,z) del objetivo
Height = 755.9 #Altura (z) a la que se va a realizar el experimento (Hallada en "Encontrar_Altura.py")
g = 9.81 * 1000 # Gravedad en mm/s^2
L = 230.7472 #Longitud de la pinza

data["delta_y"] = data["y"].diff()
data["delta_t"] = data["time"].diff()
data["Vy"] = data["delta_y"] / data["delta_t"]

t = np.sqrt(2 * (Height - Target[1] - L) / g) # Tiempo que se demora en caer el proyectil al objetivo (Calculo de Caida Libre)
data["Impacto"] = data["Vy"] * t + data["y"] # Posibles impactos (Coordenada y) del proyectil

data.to_csv("output.csv", index=False) #Se guardan los datos a un .csv

print(f'El punto de Impacto es: {data["Impacto"].iloc[33]}, soltandolo en {data["time"].iloc[33]}s')
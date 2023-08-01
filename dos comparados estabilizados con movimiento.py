import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib import animation
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import copy

def vecindario(b):
    # Función vecindario sin cambios
    filas, columnas = b.shape
    vecindario = np.zeros_like(b)

    for i in range(filas):
        for j in range(columnas):
            vecindario[i, j] = np.sum(b[max(0, i-1):min(filas, i+2), max(0, j-1):min(columnas, j+2)]) - b[i, j]

    return vecindario

def paso(b):
    # Función paso corregida para calcular el siguiente estado del tablero
    vecinos = vecindario(b)
    nueva_generacion = np.zeros_like(b)

    for i in range(b.shape[0]):
        for j in range(b.shape[1]):
            if b[i, j] == 1:
                if vecinos[i, j] < 2 or vecinos[i, j] > 3:
                    nueva_generacion[i, j] = 0
                else:
                    nueva_generacion[i, j] = 1
            else:
                if vecinos[i, j] == 3:
                    nueva_generacion[i, j] = 1

    return nueva_generacion

# Parámetros del problema para el tablero rojo
GENERACIONES = 10001
N_ROJO = 100
M_ROJO = 100

# Construimos el tablero rojo con una configuración inicial que asemeje a los hemisferios cerebrales
tablero_rojo = np.zeros((N_ROJO, M_ROJO), dtype=int)
tablero_rojo[40:60, 40:60] = 1
tablero_rojo[40:45, 50:55] = 0
tablero_rojo[55:50, 45:50] = 0

# Parámetros del problema para el tablero amarillo
N_AMARILLO = 100
M_AMARILLO = 100

# Construimos otro tablero con una configuración inicial que asemeje a los hemisferios cerebrales (amarillo)
tablero_amarillo = np.zeros((N_AMARILLO, M_AMARILLO), dtype=int)
tablero_amarillo[10:40, 20:40] = 1
tablero_amarillo[10:25, 30:35] = 0
tablero_amarillo[15:40, 25:30] = 0

# Creamos las figuras
fig = plt.figure(figsize=(12, 6))

ax_rojo = fig.add_subplot(121)
ax_rojo.axis('off')
b_rojo = tablero_rojo
imagen_rojo = ax_rojo.imshow(b_rojo, interpolation="none", cmap=cm.Reds)

ax_amarillo = fig.add_subplot(122)
ax_amarillo.axis('off')
b_amarillo = tablero_amarillo
imagen_amarillo = ax_amarillo.imshow(b_amarillo, interpolation="none", cmap=cm.YlOrBr)

def animate(i):
    global b_rojo, b_amarillo
    b_rojo = paso(copy.deepcopy(b_rojo))
    b_amarillo = paso(copy.deepcopy(b_amarillo))
    imagen_rojo.set_data(b_rojo)
    imagen_amarillo.set_data(b_amarillo)
    return [imagen_rojo, imagen_amarillo]

# Función para actualizar la animación en el formulario
def update_animation():
    global anim
    anim = animation.FuncAnimation(fig, animate, frames=GENERACIONES, blit=True, interval=200)
    canvas.draw()

# Crear la ventana del formulario
root = tk.Tk()
root.title("Juego de la Vida")

# Agregar el lienzo para mostrar las animaciones
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Agregar un botón para iniciar las animaciones
start_button = tk.Button(root, text="Iniciar Animaciones", command=update_animation)
start_button.pack()

# Mostrar la ventana del formulario
root.mainloop()

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib import animation
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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

# Parámetros del problema
GENERACIONES = 500
N = 100
M = 100

# Construimos el tablero con una configuración inicial aleatoria
tablero = np.random.randint(2, size=(N, M))

# Creamos la figura
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111)
ax.axis('off')
b = tablero
imagen = ax.imshow(b, interpolation="none", cmap=cm.gray_r)

def animate(i):
    global b
    b = paso(b)
    imagen.set_data(b)
    return [imagen]

# Función para actualizar la animación en el formulario
def update_animation():
    global anim
    anim = animation.FuncAnimation(fig, animate, frames=GENERACIONES, blit=True)
    canvas.draw()

# Crear la ventana del formulario
root = tk.Tk()
root.title("Juego de la Vida")

# Agregar el lienzo para mostrar la animación
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Agregar un botón para iniciar la animación
start_button = tk.Button(root, text="Iniciar Animación", command=update_animation)
start_button.pack()

# Mostrar la ventana del formulario
root.mainloop()
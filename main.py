import tkinter as tk
from tkinter import ttk
from visualizador import VisualizadorProcesos

'''
ENLACE GIT



copy.py es un ejemplo extraido de CHAT GPT, usarlo como referencia,
mas evitar copiar o pedir a chat que haga las cosas, esta resultando 
problematicor

Se DEBE tener los ficheros en la misma carpeta:
    cpu.py
    main.py
    proceso.py
    visualizador.py

Logica y jerarquia es:
    Objeto visualizador     (si bien guardamos en arr, TK lo guarda en un arbol)
        Objeto cpu          (Implementar planificacion comandada)
            Objeto proceso  (Unidad basica, evitar tocar mucho)

Revisar trheding (Muchos objetos creados xd, mea culpa)
Revisar lamda (Al ser dinamicos se presento problemas al graficar la logica)
Resivar polimorfismo (crear y matar objeto proceso es difernte a copiar de psutil)
Revisar Psutil (   !!!!UNNIX!!!!   )
Fue desarrollado en Python3, linux mint 22, kernel unix 6.8.0-49-generic

V.0.2
    Funciona :D
    Importa procesos
    divide y asigna 4 CPU (sin ningun algoritmo x ahora)
    X defecto deve ejecutar FCFS
    SJF funciona
    RR no funciona
    Errores visuales al maximizar pantalla
    visualizador.py es muy extenso
    la interfaz se ve simple y es torpe de manejar
'''


if __name__ == "__main__":
    root = tk.Tk()
    app = VisualizadorProcesos(root)
    root.mainloop()

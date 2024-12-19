import tkinter as tk
from tkinter import ttk
from visualizador import VisualizadorProcesos

'''
ENLACE GIT

https://github.com/ChalozMe/Process_viewer
'''


if __name__ == "__main__":
    root = tk.Tk()
    app = VisualizadorProcesos(root)
    root.mainloop()

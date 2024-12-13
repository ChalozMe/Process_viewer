


import tkinter as tk
from tkinter import ttk
import threading
import time
import random


class Proceso:
    def __init__(self, pid, nombre, cpu_time, arrival_time, remaining_time):
        self.pid = pid
        self.nombre = nombre
        self.cpu_time = cpu_time
        self.arrival_time = arrival_time
        self.remaining_time = remaining_time

    def __repr__(self):
        return (f"Proceso(PID={self.pid}, Nombre={self.nombre}, "
                f"CPU Time={self.cpu_time}, Arrival Time={self.arrival_time}, "
                f"Remaining Time={self.remaining_time})")


class VisualizadorProcesos:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualizador de Procesos")
        self.root.geometry("800x400")

        # Lista de procesos simulados
        self.procesos = [
            Proceso(pid=i, nombre=f"P{i}", cpu_time=random.randint(1, 10),
                    arrival_time=time.time(), remaining_time=random.randint(1, 10))
            for i in range(1, 6)
        ]

        # Tabla para mostrar procesos
        self.tree = ttk.Treeview(root, columns=("PID", "Nombre", "CPU Time", "Arrival Time", "Remaining Time"),
                                 show="headings")
        self.tree.heading("PID", text="PID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("CPU Time", text="CPU Time")
        self.tree.heading("Arrival Time", text="Arrival Time")
        self.tree.heading("Remaining Time", text="Remaining Time")
        self.tree.pack(fill=tk.BOTH, expand=True)

        for proceso in self.procesos:
            self.tree.insert("", "end", values=(proceso.pid, proceso.nombre,
                                                f"{proceso.cpu_time:.2f}", proceso.arrival_time,
                                                f"{proceso.remaining_time:.2f}"))

        # Botón para abrir simulador
        btn_simular = tk.Button(root, text="Simular FCFS", command=self.abrir_simulador)
        btn_simular.pack(pady=10)

    def abrir_simulador(self):
        """
        Abre una nueva ventana para mostrar la simulación del algoritmo FCFS.
        """
        ventana_simulacion = tk.Toplevel(self.root)
        ventana_simulacion.title("Simulación FCFS")
        ventana_simulacion.geometry("800x300")

        # Canvas para mostrar la simulación
        canvas = tk.Canvas(ventana_simulacion, bg="white")
        canvas.pack(fill=tk.BOTH, expand=True)

        # Etiquetas y línea de tiempo
        canvas.create_text(50, 50, text="Línea de tiempo", font=("Arial", 12), anchor="w")
        canvas.create_line(50, 100, 750, 100, width=2)  # Línea de tiempo

        # Simular FCFS en un hilo aparte
        thread = threading.Thread(target=self.simular_fcfs, args=(canvas,))
        thread.start()

    def simular_fcfs(self, canvas):
        """
        Simula el algoritmo FCFS asignando procesos a una CPU y visualizando su progreso.
        """
        x_start = 50  # Posición inicial de la barra
        y_bar = 150   # Posición vertical de la barra
        escala = 10   # Escala para reducir la longitud de las barras
        cola = self.procesos[:]
        tiempo_actual = 0

        for proceso in cola:
            # Dibujar barra para el proceso
            barra = canvas.create_rectangle(x_start, y_bar, x_start + proceso.cpu_time * escala, y_bar + 20, fill="blue")
            indicador = canvas.create_text(x_start + (proceso.cpu_time * escala) // 2, y_bar + 10, 
                                            text=proceso.nombre, font=("Arial", 10), fill="white")

            # Dibujar indicador en la línea de tiempo
            canvas.create_text(x_start, 90, text=str(tiempo_actual), font=("Arial", 10))
            tiempo_actual += proceso.cpu_time

            # Actualizar interfaz y esperar
            for _ in range(proceso.cpu_time):
                canvas.update()
                time.sleep(0.05)

            # Avanzar la posición inicial de la siguiente barra
            x_start += proceso.cpu_time * escala

        # Completar la línea de tiempo
        canvas.create_text(x_start, 90, text=str(tiempo_actual), font=("Arial", 10))
        canvas.create_text(400, 250, text="Simulación completada", font=("Arial", 14), fill="green")


if __name__ == "__main__":
    root = tk.Tk()
    app = VisualizadorProcesos(root)
    root.mainloop()

import tkinter as tk
from tkinter import ttk, messagebox
import psutil
import threading
import time
from random import uniform

from proceso import Proceso
from cpu import CPU


class VisualizadorProcesos:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualizador de Procesos")
        self.root.geometry("800x600")

        # Lista de procesos y 4 CPUs estáticas
        self.procesos = []
        self.cpus = [CPU(id=i + 1) for i in range(4)]  # Crear 4 CPUs

        # Árbol de procesos (visualizador)
        self.tree = ttk.Treeview(root, columns=("PID", "Nombre", "CPU Time", "Arrival Time", "Remaining Time"),
                                 show="headings")
        self.tree.heading("PID", text="PID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("CPU Time", text="CPU Time")
        self.tree.heading("Arrival Time", text="Arrival Time")
        self.tree.heading("Remaining Time", text="Remaining Time")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Botones
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        btn_agregar = tk.Button(btn_frame, text="Agregar Proceso", command=self.agregar_proceso)
        btn_agregar.grid(row=0, column=0, padx=10)

        btn_importar = tk.Button(btn_frame, text="Importar Procesos del Sistema", command=self.importar_procesos)
        btn_importar.grid(row=0, column=1, padx=10)

        btn_eliminar = tk.Button(btn_frame, text="Eliminar Proceso", command=self.eliminar_proceso)
        btn_eliminar.grid(row=0, column=2, padx=10)

        btn_asignar = tk.Button(btn_frame, text="Asignar a CPUs", command=self.asignar_procesos_a_cpus)
        btn_asignar.grid(row=0, column=3, padx=10)

        btn_configurar = tk.Button(btn_frame, text="Configurar CPUs", command=self.configurar_cpus)
        btn_configurar.grid(row=0, column=4, padx=10)

        btn_simular = tk.Button(btn_frame, text="Simular Planificación", command=self.abrir_simulador)
        btn_simular.grid(row=0, column=5, padx=10)

    def agregar_proceso(self):
        ventana_agregar = tk.Toplevel(self.root)
        ventana_agregar.title("Agregar Proceso")
        ventana_agregar.geometry("400x300")

        tk.Label(ventana_agregar, text="PID:").pack(pady=5)
        entry_pid = tk.Entry(ventana_agregar)
        entry_pid.pack(pady=5)

        tk.Label(ventana_agregar, text="Nombre:").pack(pady=5)
        entry_nombre = tk.Entry(ventana_agregar)
        entry_nombre.pack(pady=5)

        tk.Label(ventana_agregar, text="CPU Time:").pack(pady=5)
        entry_cpu_time = tk.Entry(ventana_agregar)
        entry_cpu_time.pack(pady=5)

        def guardar_proceso():
            try:
                pid = int(entry_pid.get())
                nombre = entry_nombre.get()
                cpu_time = float(entry_cpu_time.get())
                arrival_time = time.time()
                remaining_time = cpu_time
                nuevo_proceso = Proceso(pid, nombre, cpu_time, arrival_time, remaining_time)
                self.procesos.append(nuevo_proceso)
                self.actualizar_tabla()
                ventana_agregar.destroy()
            except ValueError:
                messagebox.showerror("Error", "Datos inválidos. Por favor, revise los campos.")

        tk.Button(ventana_agregar, text="Guardar", command=guardar_proceso).pack(pady=10)

    def importar_procesos(self):
        for p in psutil.process_iter(['pid', 'name', 'cpu_times']):
            try:
                pid = p.info['pid']
                nombre = p.info['name']
                cpu_time = sum(p.info['cpu_times']) if p.info['cpu_times'] else uniform(0.5, 2.0)
                arrival_time = 0
                remaining_time = cpu_time
                nuevo_proceso = Proceso(pid, nombre, cpu_time, arrival_time, remaining_time)
                self.procesos.append(nuevo_proceso)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

        self.actualizar_tabla()

    def eliminar_proceso(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Debe seleccionar un proceso para eliminar.")
            return

        pid_seleccionado = int(self.tree.item(seleccion, 'values')[0])
        self.procesos = [p for p in self.procesos if p.pid != pid_seleccionado]
        self.actualizar_tabla()

    def asignar_procesos_a_cpus(self):
        for i, proceso in enumerate(self.procesos):
            cpu = self.cpus[i % len(self.cpus)]  # Asignación circular
            cpu.asignar_proceso(proceso)
        messagebox.showinfo("Asignación", "Procesos asignados a las CPUs.")

    def configurar_cpus(self):
        ventana_config = tk.Toplevel(self.root)
        ventana_config.title("Configurar CPUs")
        ventana_config.geometry("400x300")

        for cpu in self.cpus:
            frame_cpu = tk.Frame(ventana_config)
            frame_cpu.pack(pady=10, fill=tk.X)

            tk.Label(frame_cpu, text=f"CPU {cpu.id}").grid(row=0, column=0, padx=5)

            def set_sjf(cpu_obj=cpu):
                cpu_obj.algorithm = "SJF"
                cpu_obj.quantum = None
                messagebox.showinfo("Configuración", f"CPU {cpu_obj.id} configurada con SJF.")

            def set_rr(cpu_obj=cpu):
                def set_quantum():
                    quantum_window = tk.Toplevel(self.root)
                    quantum_window.title("Configurar Quantum")
                    tk.Label(quantum_window, text="Quantum:").pack(pady=5)
                    quantum_entry = tk.Entry(quantum_window)
                    quantum_entry.pack(pady=5)

                    def save_quantum():
                        try:
                            quantum = float(quantum_entry.get())
                            cpu_obj.algorithm = "Round Robin"
                            cpu_obj.quantum = quantum
                            messagebox.showinfo("Configuración", f"CPU {cpu_obj.id} configurada con Round Robin y quantum {quantum}.")
                            quantum_window.destroy()
                        except ValueError:
                            messagebox.showerror("Error", "Quantum debe ser un número válido.")

                    tk.Button(quantum_window, text="Guardar", command=save_quantum).pack(pady=10)

                set_quantum()

            tk.Button(frame_cpu, text="SJF", command=set_sjf).grid(row=0, column=1, padx=5)
            tk.Button(frame_cpu, text="Round Robin", command=set_rr).grid(row=0, column=2, padx=5)

    def actualizar_tabla(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for proceso in self.procesos:
            self.tree.insert("", "end", values=(proceso.pid, proceso.nombre,
                                                  f"{proceso.cpu_time:.2f}", proceso.arrival_time,
                                                  f"{proceso.remaining_time:.2f}"))

    def abrir_simulador(self):
        if not any(cpu.procesos for cpu in self.cpus):
            messagebox.showwarning("Advertencia", "No hay procesos asignados a las CPUs para simular.")
            return

        ventana_simulacion = tk.Toplevel(self.root)
        ventana_simulacion.title("Simulación de Planificación")
        ventana_simulacion.geometry("800x400")

        canvas = tk.Canvas(ventana_simulacion, bg="white")
        canvas.pack(fill=tk.BOTH, expand=True)

        # Simular la ejecución en un hilo separado
        thread = threading.Thread(target=self.simular_planificacion, args=(canvas,))
        thread.start()

    def simular_planificacion(self, canvas):
        
        x_start = 50
        y_base = 100
        escala = 5  # Escala para bloquecito
        
        canvas.delete("all")

        for cpu in self.cpus:
            y_position = y_base + (cpu.id - 1) * 60  # cada CPU
            canvas.create_text(50, y_position - 20, text=f"CPU {cpu.id}", font=("Arial", 12), anchor="w")

            tiempo_actual = 0  # Tiempo relativo para cada CPU
            procesos_ordenados = []

            if cpu.algorithm == "SJF":
                procesos_ordenados = sorted(cpu.procesos, key=lambda p: p.cpu_time)
            elif cpu.algorithm == "Round Robin":
                quantum = cpu.quantum or 1  # DEJAR EL 1 X DEFAUT, SINO NO CORRE
                procesos_ordenados = self.round_robin_simulation(cpu.procesos, quantum)

            for proceso in procesos_ordenados: #Draw
                barra = canvas.create_rectangle(
                    x_start + tiempo_actual * escala, y_position,
                    x_start + (tiempo_actual + proceso.cpu_time) * escala,
                    y_position + 20, fill="purple"
                )
                # Dibujar el identificador del proceso
                canvas.create_text(
                    x_start + (tiempo_actual + proceso.cpu_time / 2) * escala,
                    y_position + 10, text=f"P{proceso.pid}", font=("Arial", 10), fill="white"
                )
                # Dibujar indicador del tiempo actual
                canvas.create_text(
                    x_start + tiempo_actual * escala, y_position + 30,
                    text=str(int(tiempo_actual)), font=("Arial", 8)
                )
                # TIEMPO
                tiempo_actual += proceso.cpu_time

            # colocar en la linea de tiempo el segundo en el que comienza el proceso
            canvas.create_text(
                x_start + tiempo_actual * escala, y_position + 30,
                text=str(int(tiempo_actual)), font=("Arial", 8)
            )

        # Test "print"
        canvas.create_text(
            400, y_base + len(self.cpus) * 60 + 20,
            text="Simulación completa :D", font=("Arial", 14), fill="magenta"
        )


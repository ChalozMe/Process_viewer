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
        self.root.geometry("1200x800")

        self.root.configure(bg="lightblue")
        
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
        btn_frame = tk.Frame(root, bg="cyan")
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
        if not self.procesos:
            messagebox.showwarning("Advertencia", "No hay procesos para asignar.")
            return

        for cpu in self.cpus:
            cpu.limpiar_procesos()  # Limpiar cualquier asignación previa.

        for i, proceso in enumerate(self.procesos):
            cpu = self.cpus[i % len(self.cpus)]  # Asignación circular
            cpu.asignar_proceso(proceso)

        messagebox.showinfo("Asignación", "Procesos asignados a las CPUs.")

    def configurar_cpus(self):
        ventana_config = tk.Toplevel(self.root)
        ventana_config.title("Configurar CPUs")
        ventana_config.geometry("500x300")

        # Crear widgets para cada CPU
        for cpu in self.cpus:
            frame_cpu = tk.Frame(ventana_config)
            frame_cpu.pack(pady=5, fill=tk.X)

            tk.Label(frame_cpu, text=f"CPU {cpu.id}").grid(row=0, column=0, padx=5)

            tk.Label(frame_cpu, text="Algoritmo:").grid(row=0, column=1, padx=5)
            
            # Reemplazar combobox por botones para simplicidad
            btn_fcfs = tk.Button(frame_cpu, text="FCFS", 
                                command=lambda cpu_obj=cpu: self.configurar_algoritmo(cpu_obj, "FCFS", None))
            btn_fcfs.grid(row=0, column=4, padx=5)

            btn_sjf = tk.Button(frame_cpu, text="SJF", 
                                command=lambda cpu_obj=cpu: self.configurar_algoritmo(cpu_obj, "SJF", None))
            btn_sjf.grid(row=0, column=2, padx=5)

            btn_rr = tk.Button(frame_cpu, text="Round Robin", 
                            command=lambda cpu_obj=cpu: self.abrir_config_rr(cpu_obj))
            btn_rr.grid(row=0, column=3, padx=5)

        
        tk.Button(ventana_config, text="Cerrar", command=ventana_config.destroy).pack(pady=10)

    def configurar_algoritmo(self, cpu, algoritmo, quantum):
        cpu.algorithm = algoritmo
        cpu.quantum = quantum
        cpu.ejecutar_algoritmo()
        messagebox.showinfo("Configuración", f"CPU {cpu.id} configurada con {algoritmo}.")

    def abrir_config_rr(self, cpu):
        ventana_rr = tk.Toplevel(self.root)
        ventana_rr.title(f"Configurar Quantum - CPU {cpu.id}")
        ventana_rr.geometry("300x150")

        tk.Label(ventana_rr, text=f"Configurar Quantum para CPU {cpu.id}:").pack(pady=10)
        entry_quantum = tk.Entry(ventana_rr)
        entry_quantum.pack(pady=5)

        def guardar_rr():
            try:
                quantum = float(entry_quantum.get())
                self.configurar_algoritmo(cpu, "Round Robin", quantum)
                ventana_rr.destroy()
            except ValueError:
                messagebox.showerror("Error", "El quantum debe ser un número válido.")

        tk.Button(ventana_rr, text="Guardar", command=guardar_rr).pack(pady=10)

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
        ventana_simulacion.geometry("1200x800")

        canvas = tk.Canvas(ventana_simulacion, bg="lightblue")
        canvas.pack(fill=tk.BOTH, expand=True)

        # Simular la ejecución en un hilo separado
        thread = threading.Thread(target=self.simular_planificacion, args=(canvas,))
        thread.start()

    def simular_planificacion(self, canvas):
        size_add = 1
        x_start = 50
        y_base = 100
        escala = 2  # Escala

        for cpu in self.cpus:
            procesos = cpu.get_cola_procesos() 

            # Dibujar una línea base para cada CPU
            canvas.create_text(x_start, y_base + 50, text=f"CPU {cpu.id}", anchor="w", fill="black")
            canvas.create_line(x_start, y_base + 10, x_start + 700, y_base + 10, fill="gray")

            x_pos = x_start + 1
            for proceso in procesos:
                rect_width = proceso.cpu_time * escala
                if(rect_width < 1):
                    canvas.create_rectangle(x_pos, y_base, x_pos + rect_width + size_add, y_base + 20, fill="yellow", outline="black")
                    canvas.create_text(x_pos + (rect_width+size_add) / 2, y_base + 10, text=f"P{proceso.pid}", anchor="center", fill="black")
                else:
                    canvas.create_rectangle(x_pos, y_base, x_pos + rect_width + size_add, y_base + 20, fill="blue", outline="black")
                    canvas.create_text(x_pos + (rect_width+size_add) / 2, y_base + 10, text=f"P{proceso.pid}", anchor="center", fill="white")
                x_pos += rect_width + size_add + 5

            y_base += 100

import time

from proceso import Proceso

class CPU:
    def __init__(self, id):
        self.id = id
        self.procesos = []  # Cola de procesos asignados
        self.algorithm = "SJF"  # Algoritmo por defecto
        self.quantum = None  # Quantum solo aplicable a Round Robin

    def limpiar_procesos(self):
        self.procesos = []

    def asignar_proceso(self, proceso):
        self.procesos.append(proceso)

    def ejecutar_algoritmo(self):
        """Ordena los procesos según el algoritmo configurado."""
        if self.algorithm == "SJF":
            # Shortest Job First
            self.procesos.sort(key=lambda p: p.cpu_time)
        elif self.algorithm == "Round Robin" and self.quantum is not None:
            # Round Robin
            self.procesos = self.round_robin_simulation(self.procesos, self.quantum)

    def round_robin_simulation(self, procesos, quantum):
        """
        Implementa el algoritmo Round Robin. Divide los procesos en porciones
        según el quantum especificado.
        """
        cola = procesos[:]  # Crear una copia de los procesos
        resultado = []
        tiempo_restante = {p.pid: p.cpu_time for p in procesos}

        while cola:
            proceso = cola.pop(0)
            if tiempo_restante[proceso.pid] > quantum:
                # Agregar un segmento del proceso
                nuevo_segmento = Proceso(
                    proceso.pid, proceso.nombre, quantum,
                    proceso.arrival_time, tiempo_restante[proceso.pid] - quantum
                )
                resultado.append(nuevo_segmento)
                tiempo_restante[proceso.pid] -= quantum
                cola.append(proceso)  # Reinsertar el proceso al final de la cola
            else:
                # Agregar el proceso restante
                resultado.append(proceso)
        return resultado

    def obtener_cola_procesos(self):
        return [f"PID: {p.pid}, Nombre: {p.nombre}, CPU Time: {p.cpu_time}" for p in self.procesos]

    def get_cola_procesos(self):
        return self.procesos

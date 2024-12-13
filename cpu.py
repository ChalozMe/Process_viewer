import time

class CPU:
    def __init__(self, id, algoritmo="SJF", quantum=1):

        self.id = id
        self.procesos = [] 
        self.algoritmo = algoritmo
        self.quantum = quantum

    def asignar_proceso(self, proceso):

        self.procesos.append(proceso)#Anhadir a la cola

    def planificar(self):
        if self.algoritmo == "SJF":
            self.procesos.sort(key=lambda p: p.cpu_time)  # Ordenar por tiempo de CPU
            self.ejecutar_procesos()
        elif self.algoritmo == "RR":
            self.ejecutar_round_robin()

    def ejecutar_procesos(self):
        while self.procesos:
            proceso = self.procesos.pop(0)
            print(f"CPU {self.id}: Procesando {proceso.nombre} (Tiempo: {proceso.cpu_time}s)")
            time.sleep(proceso.cpu_time)  # Simulación del tiempo de ejecución

    #Probar en consola
    def ejecutar_round_robin(self):
        while self.procesos:
            proceso = self.procesos.pop(0)
            if proceso.remaining_time > self.quantum:
                print(f"CPU {self.id}: Procesando {proceso.nombre} por {self.quantum}s")
                time.sleep(self.quantum) 
                proceso.remaining_time -= self.quantum
                self.procesos.append(proceso) 
            else:
                print(f"CPU {self.id}: Finalizando {proceso.nombre} (Tiempo restante: {proceso.remaining_time}s)")
                time.sleep(proceso.remaining_time)

    def __repr__(self):
        return f"CPU {self.id} (Algoritmo: {self.algoritmo}, Quantum: {self.quantum})"

import psutil
import time
import random

class Proceso:
    def __init__(self, pid, nombre, cpu_time, arrival_time, remaining_time):
        self.pid = pid
        self.nombre = nombre
        self.cpu_time = cpu_time
        self.arrival_time = arrival_time
        self.remaining_time = remaining_time

    @classmethod
    def from_psutil(cls, psutil_process):
        pid = psutil_process.pid
        nombre = psutil_process.name()

        cpu_times = psutil_process.cpu_times()
        cpu_time = round(cpu_times.user + cpu_times.system, 5)
        
        if cpu_time == 0:
            cpu_time = round(random.uniform(0.5, 2), 5)

        arrival_time = 0
        remaining_time = cpu_time
        return cls(pid, nombre, cpu_time, arrival_time, remaining_time)

    def __repr__(self):
        return (f"Proceso(PID={self.pid}, Nombre={self.nombre}, "
                f"CPU Time={self.cpu_time}, Arrival Time={self.arrival_time}, "
                f"Remaining Time={self.remaining_time})")

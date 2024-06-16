"""
Parcial IV. TDA. Listas Enlazadas, Pilas y Colas

Elaborado por:

- Cristian Guevara. C.I: 31.567.525
- Rodrigo Torres. C.I: 31.014.592
"""

#1.- Módulo de Gestión de Proyectos
"""
El programa deberá gestionar(crear, modificar, consultar, eliminar, y listar) los
proyectos con todos sus datos como su id, su nombre, descripción, fecha de inicio,
fecha de vencimiento, estado actual, empresa, gerente, equipo. Los usuarios podrán
agregar nuevos proyectos. Para realizar las operaciones de modificar, consultar
listar y eliminar se deberá buscar proyectos por nombre o por otros criterios.
Los proyectos deberán ser seleccionados a traves de un menú de opciones
para poder gestionar sus respectivas tareas
"""

import json
from datetime import datetime

class Proyecto:
    def __init__(self, ide, nombre, descripcion, fecha_inicio, fecha_vencimiento, estado_act, empresa, gerente, equipo):
        self.ide = ide
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha_inicio = fecha_inicio
        self.fecha_vencimiento = fecha_vencimiento
        self.estado_act = estado_act
        self.empresa = empresa
        self.gerente = gerente
        self.equipo = equipo
        
    def agregar_tarea(self, tarea):
        self.tareas.append(tarea)
        
    def contar_tareas_asignadas_a_miembro(self, miembro):
        return sum(1 for tarea in self.tareas if miembro in tarea.empresa_cliente)
    
    def obtener_tareas_pendientes(self):
        return [tarea for tarea in self.tareas if tarea.estado_t == 'pendiente']
    
    def duracion_restante(self):
        return (self.fecha_vencimiento - datetime.now()).days

class Tarea:
    def __init__(self, id_t, nombre_t, empresa_cliente, descripcion_t, fecha_inicio_t, fecha_vencimiento_t, estado_t, porcentaje):
        self.id_t = id_t
        self.nombre_t = nombre_t
        self.empresa_cliente = empresa_cliente
        self.descripcion_t = descripcion_t
        self.fecha_inicio_t = fecha_inicio_t
        self.fecha_vencimiento_t = fecha_vencimiento_t
        self.estado_t = estado_t
        self.porcentaje = porcentaje
        self.subtareas = []

    def agregar_subtarea(self, subtarea):
        self.subtareas.append(subtarea)

class Subtarea:
    def __init__(self, id_s, nombre_s, descripcion_s, estado_s):
        self.id_s = id_s
        self.nombre_s = nombre_s
        self.descripcion_s = descripcion_s
        self.estado_s = estado_s
        


#2.- Módulo de Gestión de Tareas y Prioridades
"""
Cada proyecto deberá contener una lista de tareas(id, nombre, empresa
cliente,descripción, fecha de inicio, fecha de vencimiento, estado actual,
porcentaje) y cada tarea una lista de sub tareas.
Los usuarios pueden agregar nuevas tareas al final de la lista de tareas de un
proyecto o insertar tareas en posiciones específicas. Las operaciones disponibles
incluyen eliminar tareas de la lista, buscar tareas por nombre u otros criterios, y
actualizar la información de las tareas existentes.

Se deberá utilizar una pila para almacenar las tareas prioritarias de cada
proyecto. Las tareas se insertan en la pila de acuerdo con su prioridad, de modo que
la tarea más prioritaria esté en la cima de la pila. Los usuarios pueden agregar
nuevas tareas prioritarias, eliminar tareas prioritarias de la cima de la pila y consultar
la tarea más prioritaria sin eliminarla y mostrar el tiempo total de las tareas
prioritarias.

Se deberá utilizar una cola para almacenar las tareas que están próximas a
su fecha de vencimiento. Las tareas se agregan a la cola a medida que se acerca su
fecha de vencimiento, de modo que la tarea más próxima a vencer esté al frente de
la cola. Los usuarios pueden agregar nuevas tareas a la cola, eliminar tareas de la
parte delantera de la cola cuando se completen antes de la fecha de vencimiento y
consultar la tarea que está próxima a vencer sin eliminarla y mostrar el tiempo total
de las tareas próximas a vencer.
"""


#3.- Módulo de Reportes



#4.- Módulo de importación y exportación de datos


class Carga:
    def __init__(self, nombre_archivo):
        self.nombre_archivo = nombre_archivo

    def cargar_datos_desde_json(self):
        proyectos = []
        with open(self.nombre_archivo, "r") as archivo:
            datos = json.load(archivo)
            for proyecto_data in datos["proyectos"]:
                proyecto = Proyecto(
                    proyecto_data["id"],
                    proyecto_data["nombre"],
                    proyecto_data["descripcion"],
                    datetime.strptime(proyecto_data["fecha_inicio"], "%Y-%m-%d"),
                    datetime.strptime(proyecto_data["fecha_vencimiento"], "%Y-%m-%d"),
                    proyecto_data["estado"],
                    proyecto_data["empresa"],
                    proyecto_data["gerente"],
                    proyecto_data["equipo"]
                )
                for tarea_data in proyecto_data["tareas"]:
                    tarea = Tarea(
                        tarea_data["id"],
                        tarea_data["nombre"],
                        tarea_data["empresa_cliente"],
                        tarea_data["descripcion"],
                        datetime.strptime(tarea_data["fecha_inicio"], "%Y-%m-%d"),
                        datetime.strptime(tarea_data["fecha_vencimiento"], "%Y-%m-%d"),
                        tarea_data["estado"],
                        tarea_data["porcentaje"]
                    )
                    for subtarea_data in tarea_data.get("subtareas", []):
                        subtarea = Subtarea(
                            subtarea_data["id"],
                            subtarea_data["nombre"],
                            subtarea_data["descripcion"],
                            subtarea_data["estado"]
                        )
                        tarea.agregar_subtarea(subtarea)
                    proyecto.agregar_tarea(tarea)
                proyectos.append(proyecto)
        return proyectos
    
    
# Cargar datos desde un archivo JSON
prueba = Carga("datos_prueba2.json")
proyectos = prueba.cargar_datos_desde_json()

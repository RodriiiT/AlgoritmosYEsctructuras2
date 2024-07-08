"""
Parcial V. Estructura de Árboles

Elaborado por:

- Cristian Guevara. C.I: 31.567.525
- Rodrigo Torres. C.I: 31.014.592
"""
import json
from datetime import datetime


#1.- Modulo de Gestión de Empreseas--------------------------------------------------------------------------------------------------------------------------------------------
import csv

class Empresa:
    def __init__(self, id, nombre, direccion, telefono):
        self.id = id
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono

    def __str__(self):
        return f"ID: {self.id}, Nombre: {self.nombre}, Dirección: {self.direccion}, Teléfono: {self.telefono}"

class GestionEmpresas:
    def __init__(self, archivo_csv):
        self.archivo_csv = archivo_csv
        self.empresas = self.cargar_empresas()

    def cargar_empresas(self):
        empresas = []
        try:
            with open(self.archivo_csv, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    empresa = Empresa(row['id'], row['nombre'], row['direccion'], row['telefono'])
                    empresas.append(empresa)
        except FileNotFoundError:
            pass
        return empresas

    def guardar_empresas(self):
        with open(self.archivo_csv, 'w', newline='') as csvfile:
            fieldnames = ['id', 'nombre', 'direccion', 'telefono']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for empresa in self.empresas:
                writer.writerow({'id': empresa.id, 'nombre': empresa.nombre, 'direccion': empresa.direccion, 'telefono': empresa.telefono})

    def crear_empresa(self, id, nombre, direccion, telefono):
        nueva_empresa = Empresa(id, nombre, direccion, telefono)
        self.empresas.append(nueva_empresa)
        self.guardar_empresas()

    def listar_empresas(self):
        for empresa in self.empresas:
            print(empresa)

    def buscar_empresa(self, id):
        for empresa in self.empresas:
            if empresa.id == id:
                return empresa
        return None

    def modificar_empresa(self, id, nombre=None, direccion=None, telefono=None):
        empresa = self.buscar_empresa(id)
        if empresa:
            if nombre:
                empresa.nombre = nombre
            if direccion:
                empresa.direccion = direccion
            if telefono:
                empresa.telefono = telefono
            self.guardar_empresas()
            return True
        return False

    def eliminar_empresa(self, id):
        empresa = self.buscar_empresa(id)
        if empresa:
            self.empresas.remove(empresa)
            self.guardar_empresas()
            return True
        return False

# Ejemplo de uso
gestion_empresas = GestionEmpresas('empresas.csv')
gestion_empresas.crear_empresa('1', 'Empresa A', 'Direccion A', '123456789')
gestion_empresas.crear_empresa('2', 'Empresa B', 'Direccion B', '987654321')
gestion_empresas.listar_empresas()


#2.- Modulo de Gestión de Proyectos------------------------------------------------------------------------------------------------------------------------------------------------
class Proyecto:
    def __init__(self, id, nombre, gerente, fecha_inicio, fecha_vencimiento, estado):
        self.id = id
        self.nombre = nombre
        self.gerente = gerente
        self.fecha_inicio = fecha_inicio
        self.fecha_vencimiento = fecha_vencimiento
        self.estado = estado

    def __str__(self):
        return f"ID: {self.id}, Nombre: {self.nombre}, Gerente: {self.gerente}, Fecha de Inicio: {self.fecha_inicio}, Fecha de Vencimiento: {self.fecha_vencimiento}, Estado: {self.estado}"

class NodoAVL:
    def __init__(self, proyecto):
        self.proyecto = proyecto
        self.altura = 1
        self.izquierda = None
        self.derecha = None

class ArbolAVL:
    def __init__(self):
        self.raiz = None

    def obtener_altura(self, nodo):
        if not nodo:
            return 0
        return nodo.altura

    def balancear(self, nodo):
        if not nodo:
            return 0
        return self.obtener_altura(nodo.izquierda) - self.obtener_altura(nodo.derecha)

    def rotar_derecha(self, y):
        x = y.izquierda
        T2 = x.derecha

        x.derecha = y
        y.izquierda = T2

        y.altura = max(self.obtener_altura(y.izquierda), self.obtener_altura(y.derecha)) + 1
        x.altura = max(self.obtener_altura(x.izquierda), self.obtener_altura(x.derecha)) + 1

        return x

    def rotar_izquierda(self, x):
        y = x.derecha
        T2 = y.izquierda

        y.izquierda = x
        x.derecha = T2

        x.altura = max(self.obtener_altura(x.izquierda), self.obtener_altura(x.derecha)) + 1
        y.altura = max(self.obtener_altura(y.izquierda), self.obtener_altura(y.derecha)) + 1

        return y

    def insertar(self, nodo, proyecto):
        if not nodo:
            return NodoAVL(proyecto)

        if proyecto.fecha_vencimiento < nodo.proyecto.fecha_vencimiento:
            nodo.izquierda = self.insertar(nodo.izquierda, proyecto)
        else:
            nodo.derecha = self.insertar(nodo.derecha, proyecto)

        nodo.altura = max(self.obtener_altura(nodo.izquierda), self.obtener_altura(nodo.derecha)) + 1

        balance = self.balancear(nodo)

        if balance > 1 and proyecto.fecha_vencimiento < nodo.izquierda.proyecto.fecha_vencimiento:
            return self.rotar_derecha(nodo)

        if balance < -1 and proyecto.fecha_vencimiento > nodo.derecha.proyecto.fecha_vencimiento:
            return self.rotar_izquierda(nodo)

        if balance > 1 and proyecto.fecha_vencimiento > nodo.izquierda.proyecto.fecha_vencimiento:
            nodo.izquierda = self.rotar_izquierda(nodo.izquierda)
            return self.rotar_derecha(nodo)

        if balance < -1 and proyecto.fecha_vencimiento < nodo.derecha.proyecto.fecha_vencimiento:
            nodo.derecha = self.rotar_derecha(nodo.derecha)
            return self.rotar_izquierda(nodo)

        return nodo

    def preorden(self, nodo):
        if not nodo:
            return
        print(nodo.proyecto)
        self.preorden(nodo.izquierda)
        self.preorden(nodo.derecha)

class GestionProyectos:
    def __init__(self):
        self.arbol_avl = ArbolAVL()

    def crear_proyecto(self, id, nombre, gerente, fecha_inicio, fecha_vencimiento, estado):
        nuevo_proyecto = Proyecto(id, nombre, gerente, fecha_inicio, fecha_vencimiento, estado)
        self.arbol_avl.raiz = self.arbol_avl.insertar(self.arbol_avl.raiz, nuevo_proyecto)

    def listar_proyectos(self):
        self.arbol_avl.preorden(self.arbol_avl.raiz)

# Ejemplo de uso
gestion_proyectos = GestionProyectos()
gestion_proyectos.crear_proyecto('1', 'Proyecto A', 'Gerente 1', '2023-01-01', '2023-12-31', 'En progreso')
gestion_proyectos.crear_proyecto('2', 'Proyecto B', 'Gerente 2', '2023-02-01', '2023-11-30', 'En progreso')
gestion_proyectos.listar_proyectos()

#3.- Modulo de Gestión de Tareas y Prioridades--------------------------------------------------------------------------------------------------------------------------------------
class Tarea:
    def __init__(self, id, nombre, descripcion, prioridad):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.prioridad = prioridad
        self.subtareas = []

    def agregar_subtarea(self, tarea):
        self.subtareas.append(tarea)

    def __str__(self):
        return f"ID: {self.id}, Nombre: {self.nombre}, Descripción: {self.descripcion}, Prioridad: {self.prioridad}"

class GestionTareas:
    def __init__(self):
        self.tareas = []

    def crear_tarea(self, id, nombre, descripcion, prioridad):
        nueva_tarea = Tarea(id, nombre, descripcion, prioridad)
        self.tareas.append(nueva_tarea)
        return nueva_tarea

    def listar_tareas(self):
        for tarea in self.tareas:
            print(tarea)
            self.listar_subtareas(tarea, nivel=1)

    def listar_subtareas(self, tarea, nivel):
        for subtarea in tarea.subtareas:
            print("  " * nivel + str(subtarea))
            self.listar_subtareas(subtarea, nivel + 1)

# Ejemplo de uso
gestion_tareas = GestionTareas()
tarea_principal = gestion_tareas.crear_tarea('1', 'Tarea Principal', 'Descripción de la tarea principal', 'Alta')
subtarea1 = Tarea('1.1', 'Subtarea 1', 'Descripción de la subtarea 1', 'Media')
subtarea2 = Tarea('1.2', 'Subtarea 2', 'Descripción de la subtarea 2', 'Baja')
tarea_principal.agregar_subtarea(subtarea1)
tarea_principal.agregar_subtarea(subtarea2)
gestion_tareas.listar_tareas()

#4.- Modulo de Gestión de Sprint----------------------------------------------------------------------------------------------------------------------------------------------------
class Sprint:
    def __init__(self, id, objetivo, fecha_inicio, fecha_vencimiento):
        self.id = id
        self.objetivo = objetivo
        self.fecha_inicio = fecha_inicio
        self.fecha_vencimiento = fecha_vencimiento
        self.tareas = []

    def agregar_tarea(self, tarea):
        self.tareas.append(tarea)

    def __str__(self):
        return f"ID: {self.id}, Objetivo: {self.objetivo}, Fecha de Inicio: {self.fecha_inicio}, Fecha de Vencimiento: {self.fecha_vencimiento}"

class GestionSprints:
    def __init__(self):
        self.arbol_avl = ArbolAVL()

    def crear_sprint(self, id, objetivo, fecha_inicio, fecha_vencimiento):
        nuevo_sprint = Sprint(id, objetivo, fecha_inicio, fecha_vencimiento)
        self.arbol_avl.raiz = self.arbol_avl.insertar(self.arbol_avl.raiz, nuevo_sprint)

    def listar_sprints(self):
        self.arbol_avl.preorden(self.arbol_avl.raiz)

# Ejemplo de uso
gestion_sprints = GestionSprints()
gestion_sprints.crear_sprint('1', 'Objetivo A', '2023-01-01', '2023-01-15')
gestion_sprints.crear_sprint('2', 'Objetivo B', '2023-02-01', '2023-02-15')
gestion_sprints.listar_sprints()

#5.- Modulo de Reportes-------------------------------------------------------------------------------------------------------------------------------------------------------------
class GestionReportes:
    def __init__(self, gestion_proyectos, gestion_tareas, gestion_sprints):
        self.gestion_proyectos = gestion_proyectos
        self.gestion_tareas = gestion_tareas
        self.gestion_sprints = gestion_sprints

    def tareas_criticas(self):
        # Aquí implementarás la lógica para identificar y mostrar tareas críticas.
        pass

    def listar_tareas_empleado(self, empleado):
        # Aquí implementarás la lógica para listar todas las tareas asignadas a un empleado específico.
        pass

    def exportar_tareas_completadas(self, horas):
        # Aquí implementarás la lógica para exportar a un archivo CSV las tareas completadas cuya duración sea igual o inferior a un valor en horas especificado.
        pass

# Ejemplo de uso
gestion_reportes = GestionReportes(gestion_proyectos, gestion_tareas, gestion_sprints)
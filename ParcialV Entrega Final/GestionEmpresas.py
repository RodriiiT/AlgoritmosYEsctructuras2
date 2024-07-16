"""
Parcial V. Estructura de Árboles

Elaborado por:

- Cristian Guevara. C.I: 31.567.525
- Rodrigo Torres. C.I: 31.014.592
- Regina Escalona. C.I: 30.681671
"""
import csv
import re
import json
from datetime import datetime, date
from collections import defaultdict


class Proyecto:
    def __init__(self, id, nombre, descripcion, fecha_inicio, fecha_vencimiento, estado_actual, empresa, gerente, equipo):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha_inicio = fecha_inicio
        self.fecha_vencimiento = fecha_vencimiento
        self.estado_actual = estado_actual
        self.empresa = empresa
        self.gerente = gerente
        self.equipo = equipo
        self.tareas = ArbolNArio()
        self.sprints = ArbolAVLSprints()

    def __str__(self):
        return f"ID: {self.id}, Nombre: {self.nombre}, Estado: {self.estado_actual}"


    def tiempo_restante(self):
        return (self.fecha_vencimiento - date.today()).days

    def __lt__(self, other):
        return self.tiempo_restante() > other.tiempo_restante()

    def __eq__(self, other):
        return self.tiempo_restante() == other.tiempo_restante()

class Empresa:
    def __init__(self, id, nombre, descripcion, fecha_creacion, direccion, telefono, correo, gerente, equipo_contacto):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha_creacion = fecha_creacion
        self.direccion = direccion
        self.telefono = telefono
        self.correo = correo
        self.gerente = gerente
        self.equipo_contacto = equipo_contacto
        self.proyectos = ArbolAVL()

    def __str__(self):
        return f"ID: {self.id}, Nombre: {self.nombre}, Gerente: {self.gerente}"

    def agregar_proyecto(self, proyecto):
        self.proyectos.append(proyecto)

    def listar_proyectos(self):
        for proyecto in self.proyectos:
            print(proyecto)

    def buscar_proyecto(self, id_proyecto):
        for proyecto in self.proyectos:
            if proyecto.id == id_proyecto:
                return proyecto
        return None

class NodoEmpresa:
    def __init__(self, empresa):
        self.empresa = empresa
        self.siguiente = None

class ListaEnlazadaEmpresas:
    def __init__(self):
        self.cabeza = None

    def agregar_empresa(self, empresa):
        nuevo_nodo = NodoEmpresa(empresa)
        if not self.cabeza:
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo

    def listar_empresas(self):
        actual = self.cabeza
        while actual:
            print(actual.empresa)
            actual = actual.siguiente

    def buscar_empresa(self, id):
        actual = self.cabeza
        while actual:
            if actual.empresa.id == id:
                return actual.empresa
            actual = actual.siguiente
        return None

    def modificar_empresa(self, id, nuevos_datos):
        empresa = self.buscar_empresa(id)
        if empresa:
            for key, value in nuevos_datos.items():
                setattr(empresa, key, value)
            return True
        return False

    def eliminar_empresa(self, id):
        if not self.cabeza:
            return False
        if self.cabeza.empresa.id == id:
            self.cabeza = self.cabeza.siguiente
            return True
        actual = self.cabeza
        while actual.siguiente:
            if actual.siguiente.empresa.id == id:
                actual.siguiente = actual.siguiente.siguiente
                return True
            actual = actual.siguiente
        return False
    
    def obtener_todas_empresas(self):
        empresas = []
        actual = self.cabeza
        while actual:
            empresas.append(actual.empresa)
            actual = actual.siguiente
        return empresas

#-------------------------------------------------------Clases para el 2do módulo----------------------------------------------------------------------------------------------------
class NodoAVL:
    def __init__(self, proyecto):
        self.proyecto = proyecto
        self.izquierda = None
        self.derecha = None
        self.altura = 1

class ArbolAVL:
    def __init__(self):
        self.raiz = None

    def altura(self, nodo):
        if not nodo:
            return 0
        return nodo.altura

    def balance(self, nodo):
        if not nodo:
            return 0
        return self.altura(nodo.izquierda) - self.altura(nodo.derecha)

    def rotacion_derecha(self, y):
        x = y.izquierda
        T2 = x.derecha

        x.derecha = y
        y.izquierda = T2

        y.altura = 1 + max(self.altura(y.izquierda), self.altura(y.derecha))
        x.altura = 1 + max(self.altura(x.izquierda), self.altura(x.derecha))

        return x

    def rotacion_izquierda(self, x):
        y = x.derecha
        T2 = y.izquierda

        y.izquierda = x
        x.derecha = T2

        x.altura = 1 + max(self.altura(x.izquierda), self.altura(x.derecha))
        y.altura = 1 + max(self.altura(y.izquierda), self.altura(y.derecha))

        return y

    def insertar(self, raiz, proyecto):
        if not raiz:
            return NodoAVL(proyecto)
        
        if proyecto < raiz.proyecto:
            raiz.izquierda = self.insertar(raiz.izquierda, proyecto)
        else:
            raiz.derecha = self.insertar(raiz.derecha, proyecto)

        raiz.altura = 1 + max(self.altura(raiz.izquierda), self.altura(raiz.derecha))

        balance = self.balance(raiz)

        if balance > 1 and proyecto < raiz.izquierda.proyecto:
            return self.rotacion_derecha(raiz)

        if balance < -1 and proyecto > raiz.derecha.proyecto:
            return self.rotacion_izquierda(raiz)

        if balance > 1 and proyecto > raiz.izquierda.proyecto:
            raiz.izquierda = self.rotacion_izquierda(raiz.izquierda)
            return self.rotacion_derecha(raiz)

        if balance < -1 and proyecto < raiz.derecha.proyecto:
            raiz.derecha = self.rotacion_derecha(raiz.derecha)
            return self.rotacion_izquierda(raiz)

        return raiz

    def insertar_proyecto(self, proyecto):
        self.raiz = self.insertar(self.raiz, proyecto)

    def buscar(self, raiz, criterio, valor):
        if not raiz:
            return None
        
        proyecto_valor = getattr(raiz.proyecto, criterio)
        if proyecto_valor == valor:
            return raiz.proyecto
        elif valor < proyecto_valor:
            return self.buscar(raiz.izquierda, criterio, valor)
        else:
            return self.buscar(raiz.derecha, criterio, valor)

    def buscar_proyecto(self, criterio, valor):
        return self.buscar(self.raiz, criterio, valor)

    def eliminar(self, raiz, proyecto):
        if not raiz:
            return raiz

        if proyecto < raiz.proyecto:
            raiz.izquierda = self.eliminar(raiz.izquierda, proyecto)
        elif proyecto > raiz.proyecto:
            raiz.derecha = self.eliminar(raiz.derecha, proyecto)
        else:
            if not raiz.izquierda:
                return raiz.derecha
            elif not raiz.derecha:
                return raiz.izquierda

            temp = self.nodo_valor_minimo(raiz.derecha)
            raiz.proyecto = temp.proyecto
            raiz.derecha = self.eliminar(raiz.derecha, temp.proyecto)

        if not raiz:
            return raiz

        raiz.altura = 1 + max(self.altura(raiz.izquierda), self.altura(raiz.derecha))

        balance = self.balance(raiz)

        if balance > 1 and self.balance(raiz.izquierda) >= 0:
            return self.rotacion_derecha(raiz)

        if balance > 1 and self.balance(raiz.izquierda) < 0:
            raiz.izquierda = self.rotacion_izquierda(raiz.izquierda)
            return self.rotacion_derecha(raiz)

        if balance < -1 and self.balance(raiz.derecha) <= 0:
            return self.rotacion_izquierda(raiz)

        if balance < -1 and self.balance(raiz.derecha) > 0:
            raiz.derecha = self.rotacion_derecha(raiz.derecha)
            return self.rotacion_izquierda(raiz)

        return raiz

    def eliminar_proyecto(self, proyecto):
        self.raiz = self.eliminar(self.raiz, proyecto)

    def nodo_valor_minimo(self, nodo):
        actual = nodo
        while actual.izquierda:
            actual = actual.izquierda
        return actual

    def inorden(self, raiz):
        if raiz:
            self.inorden(raiz.izquierda)
            print(raiz.proyecto)
            self.inorden(raiz.derecha)

    def listar_proyectos(self):
        self.inorden(self.raiz)
        
    def obtener_todos_proyectos(self):
        proyectos = []
        def inorden(nodo):
            if nodo:
                inorden(nodo.izquierda)
                proyectos.append(nodo.proyecto)
                inorden(nodo.derecha)
        inorden(self.raiz)
        return proyectos
#-------------------------------------------------------Clases para el 3er módulo---------------------------------------------------------------------------------------------------        
class Tarea:
    def __init__(self, id, nombre, descripcion, fecha_inicio, fecha_vencimiento, estado_actual, duracion, empleado_cedula):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha_inicio = fecha_inicio
        self.fecha_vencimiento = fecha_vencimiento
        self.estado_actual = estado_actual
        self.duracion = duracion
        self.empleado_cedula = empleado_cedula
        self.subtareas = []  # Inicializamos la lista de subtareas

    def __str__(self):
        return f"Tarea: {self.nombre}, Estado: {self.estado_actual}, Duración: {self.duracion} horas"

class ArbolNArio:
    def __init__(self):
        self.raiz = None

    def agregar_tarea(self, tarea, tarea_padre=None):
        if not self.raiz:
            self.raiz = tarea
        elif not tarea_padre:
            self.raiz.subtareas.append(tarea)
        else:
            self._agregar_subtarea(self.raiz, tarea, tarea_padre)

    def _agregar_subtarea(self, nodo_actual, nueva_tarea, tarea_padre):
        if nodo_actual.id == tarea_padre.id:
            nodo_actual.subtareas.append(nueva_tarea)
        else:
            for subtarea in nodo_actual.subtareas:
                self._agregar_subtarea(subtarea, nueva_tarea, tarea_padre)

    def consultar_tarea(self, id_tarea):
        return self._buscar_tarea(self.raiz, id_tarea)

    def _buscar_tarea(self, nodo, id_tarea):
        if nodo.id == id_tarea:
            return nodo
        for subtarea in nodo.subtareas:
            resultado = self._buscar_tarea(subtarea, id_tarea)
            if resultado:
                return resultado
        return None

    def modificar_tarea(self, id_tarea, nuevos_datos):
        tarea = self.consultar_tarea(id_tarea)
        if tarea:
            for key, value in nuevos_datos.items():
                setattr(tarea, key, value)
            return True
        return False

    def eliminar_tarea(self, id_tarea):
        if self.raiz.id == id_tarea:
            self.raiz = None
            return True
        return self._eliminar_subtarea(self.raiz, id_tarea)

    def _eliminar_subtarea(self, nodo, id_tarea):
        for i, subtarea in enumerate(nodo.subtareas):
            if subtarea.id == id_tarea:
                del nodo.subtareas[i]
                return True
            if self._eliminar_subtarea(subtarea, id_tarea):
                return True
        return False

    def listar_tareas(self, nivel=None):
        self._listar_tareas_recursivo(self.raiz, 0, nivel)

    def _listar_tareas_recursivo(self, nodo, nivel_actual, nivel_objetivo=None):
        if nivel_objetivo is None or nivel_actual == nivel_objetivo:
            print("  " * nivel_actual + str(nodo))
        if nivel_objetivo is None or nivel_actual < nivel_objetivo:
            for subtarea in nodo.subtareas:
                self._listar_tareas_recursivo(subtarea, nivel_actual + 1, nivel_objetivo)

    def mostrar_subtareas(self, id_tarea):
        tarea = self.consultar_tarea(id_tarea)
        if tarea:
            self._mostrar_subtareas_recursivo(tarea, 0)
        else:
            print(f"No se encontró la tarea con ID {id_tarea}")

    def _mostrar_subtareas_recursivo(self, tarea, nivel):
        print("  " * nivel + str(tarea))
        for subtarea in tarea.subtareas:
            self._mostrar_subtareas_recursivo(subtarea, nivel + 1)

    def consultar_tarea(self, id_tarea):
        def buscar(nodo):
            if nodo.tarea.id == id_tarea:
                return nodo.tarea
            for hijo in nodo.hijos:
                resultado = buscar(hijo)
                if resultado:
                    return resultado
            return None

        return buscar(self.raiz) if self.raiz else None
#-------------------------------------------------------Clases para el 4to módulo---------------------------------------------------------------------------------------------------      
class Sprint:
    def __init__(self, id, nombre, fecha_inicio, fecha_fin, estado, objetivos, equipo):
        self.id = id
        self.nombre = nombre
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.estado = estado
        self.objetivos = objetivos
        self.equipo = equipo
        self.tareas = ListaEnlazadaTareas()

    def __str__(self):
        return f"Sprint ID: {self.id}, Nombre: {self.nombre}, Estado: {self.estado}"

    def tiempo_restante(self):
        return (self.fecha_fin - date.today()).days

    def __lt__(self, other):
        return self.tiempo_restante() < other.tiempo_restante()

    def __eq__(self, other):
        return self.tiempo_restante() == other.tiempo_restante()

class NodoAVLSprint:
    def __init__(self, sprint):
        self.sprint = sprint
        self.izquierda = None
        self.derecha = None
        self.altura = 1

class ArbolAVLSprints:
    def __init__(self):
        self.raiz = None

    def altura(self, nodo):
        if not nodo:
            return 0
        return nodo.altura

    def balance(self, nodo):
        if not nodo:
            return 0
        return self.altura(nodo.izquierda) - self.altura(nodo.derecha)

    def rotacion_derecha(self, y):
        x = y.izquierda
        T2 = x.derecha

        x.derecha = y
        y.izquierda = T2

        y.altura = 1 + max(self.altura(y.izquierda), self.altura(y.derecha))
        x.altura = 1 + max(self.altura(x.izquierda), self.altura(x.derecha))

        return x

    def rotacion_izquierda(self, x):
        y = x.derecha
        T2 = y.izquierda

        y.izquierda = x
        x.derecha = T2

        x.altura = 1 + max(self.altura(x.izquierda), self.altura(x.derecha))
        y.altura = 1 + max(self.altura(y.izquierda), self.altura(y.derecha))

        return y

    def insertar(self, raiz, sprint):
        if not raiz:
            return NodoAVLSprint(sprint)
        
        if sprint < raiz.sprint:
            raiz.izquierda = self.insertar(raiz.izquierda, sprint)
        else:
            raiz.derecha = self.insertar(raiz.derecha, sprint)

        raiz.altura = 1 + max(self.altura(raiz.izquierda), self.altura(raiz.derecha))

        balance = self.balance(raiz)

        if balance > 1 and sprint < raiz.izquierda.sprint:
            return self.rotacion_derecha(raiz)

        if balance < -1 and sprint > raiz.derecha.sprint:
            return self.rotacion_izquierda(raiz)

        if balance > 1 and sprint > raiz.izquierda.sprint:
            raiz.izquierda = self.rotacion_izquierda(raiz.izquierda)
            return self.rotacion_derecha(raiz)

        if balance < -1 and sprint < raiz.derecha.sprint:
            raiz.derecha = self.rotacion_derecha(raiz.derecha)
            return self.rotacion_izquierda(raiz)

        return raiz

    def insertar_sprint(self, sprint):
        self.raiz = self.insertar(self.raiz, sprint)

    def buscar(self, raiz, id_sprint):
        if not raiz or raiz.sprint.id == id_sprint:
            return raiz
        if id_sprint < raiz.sprint.id:
            return self.buscar(raiz.izquierda, id_sprint)
        return self.buscar(raiz.derecha, id_sprint)

    def buscar_sprint(self, id_sprint):
        return self.buscar(self.raiz, id_sprint)

    def inorden(self, raiz):
        if raiz:
            self.inorden(raiz.izquierda)
            print(raiz.sprint)
            self.inorden(raiz.derecha)

    def listar_sprints(self):
        self.inorden(self.raiz)

class NodoTarea:
    def __init__(self, tarea):
        self.tarea = tarea
        self.siguiente = None

class ListaEnlazadaTareas:
    def __init__(self):
        self.cabeza = None

    def agregar_tarea(self, tarea):
        nuevo_nodo = NodoTarea(tarea)
        if not self.cabeza:
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo

    def listar_tareas(self):
        actual = self.cabeza
        while actual:
            print(actual.tarea)
            actual = actual.siguiente

#-----------------------------------------------------------Menú y validaciones-------------------------------------------------------------------------------------------------------

#Validaciones
def validar_fecha(fecha_str):
    try:
        return datetime.strptime(fecha_str, "%Y-%m-%d").date()
    except ValueError:
        return None

def validar_porcentaje(porcentaje_str):
    try:
        porcentaje = int(porcentaje_str)
        return 0 <= porcentaje <= 100
    except ValueError:
        return False

def validar_correo(correo):
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(patron, correo) is not None

def validar_telefono(telefono):
    patron = r'^\+?1?\d{9,15}$'
    return re.match(patron, telefono) is not None

def input_validado(prompt, validacion, mensaje_error):
    while True:
        valor = input(prompt)
        if validacion(valor):
            return valor
        print(mensaje_error)

#Leer archivo csv
def cargar_empresas_desde_csv(archivo):
    empresas = ListaEnlazadaEmpresas()
    with open(archivo, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            empresa = Empresa(
                row['id'],
                row['nombre'],
                row['descripcion'],
                datetime.strptime(row['fecha_creacion'], "%Y-%m-%d"),
                row['direccion'],
                row['telefono'],
                row['correo'],
                row['gerente'],
                row['equipo_contacto']
            )
            
            if 'proyectos' in row and row['proyectos']:
                try:
                    proyectos = json.loads(row['proyectos'])
                    for p in proyectos:
                        proyecto = Proyecto(
                            p['id'],
                            p['nombre'],
                            p['descripcion'],
                            datetime.strptime(p['fecha_inicio'], "%Y-%m-%d"),
                            datetime.strptime(p['fecha_vencimiento'], "%Y-%m-%d"),
                            p['estado_actual'],
                            empresa.nombre,
                            p['gerente'],
                            p['equipo']
                        )
                        empresa.proyectos.insertar_proyecto(proyecto)
                except json.JSONDecodeError:
                    print(f"Error al decodificar proyectos para la empresa {empresa.nombre}. Continuando sin proyectos.")
            
            empresas.agregar_empresa(empresa)
    return empresas

def guardar_empresas_en_csv(empresas, archivo):
    with open(archivo, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'nombre', 'descripcion', 'fecha_creacion', 'direccion', 'telefono', 'correo', 'gerente', 'equipo_contacto', 'proyectos'])
        actual = empresas.cabeza
        while actual:
            e = actual.empresa
            proyectos_json = json.dumps([{
                'id': p.id,
                'nombre': p.nombre,
                'descripcion': p.descripcion,
                'fecha_inicio': p.fecha_inicio.strftime("%Y-%m-%d"),
                'fecha_vencimiento': p.fecha_vencimiento.strftime("%Y-%m-%d"),
                'estado_actual': p.estado_actual,
                'gerente': p.gerente,
                'equipo': p.equipo
            } for p in obtener_proyectos_inorden(e.proyectos.raiz)]) if e.proyectos.raiz else ''
            
            writer.writerow([e.id, e.nombre, e.descripcion, e.fecha_creacion.strftime("%Y-%m-%d"), 
                             e.direccion, e.telefono, e.correo, e.gerente, e.equipo_contacto, proyectos_json])
            actual = actual.siguiente

def obtener_proyectos_inorden(nodo):
    if not nodo:
        return []
    return (obtener_proyectos_inorden(nodo.izquierda) + 
            [nodo.proyecto] + 
            obtener_proyectos_inorden(nodo.derecha))

#Métodos entradas para el primer módulo
def crear_empresa(empresas):
    print("Creando nueva empresa:")
    id = input_validado("ID: ", lambda x: x.isalnum(), "El ID debe ser alfanumérico.")
    nombre = input_validado("Nombre: ", lambda x: len(x) > 0, "El nombre no puede estar vacío.")
    descripcion = input("Descripción: ")
    fecha_creacion = input_validado("Fecha de creación (YYYY-MM-DD): ", 
                                    lambda x: validar_fecha(x) is not None, 
                                    "Formato de fecha inválido. Use YYYY-MM-DD.")
    direccion = input("Dirección: ")
    telefono = input_validado("Teléfono: ", validar_telefono, "Formato de teléfono inválido.")
    correo = input_validado("Correo: ", validar_correo, "Formato de correo electrónico inválido.")
    gerente = input("Gerente: ")
    equipo_contacto = input("Equipo de contacto: ")

    nueva_empresa = Empresa(id, nombre, descripcion, validar_fecha(fecha_creacion), 
                            direccion, telefono, correo, gerente, equipo_contacto)
    empresas.agregar_empresa(nueva_empresa)
    print("Empresa creada con éxito.")

def consultar_empresa(empresas):
    id = input("Ingrese el ID de la empresa a consultar: ")
    empresa = empresas.buscar_empresa(id)
    if empresa:
        print(f"Detalles de la empresa:\n"
              f"ID: {empresa.id}\n"
              f"Nombre: {empresa.nombre}\n"
              f"Descripción: {empresa.descripcion}\n"
              f"Fecha de creación: {empresa.fecha_creacion.strftime('%Y-%m-%d')}\n"
              f"Dirección: {empresa.direccion}\n"
              f"Teléfono: {empresa.telefono}\n"
              f"Correo: {empresa.correo}\n"
              f"Gerente: {empresa.gerente}\n"
              f"Equipo de contacto: {empresa.equipo_contacto}")
        
        print("\nProyectos asociados:")
        empresa.proyectos.listar_proyectos()
    else:
        print("Empresa no encontrada.")

def modificar_empresa(empresas):
    id = input("Ingrese el ID de la empresa a modificar: ")
    empresa = empresas.buscar_empresa(id)
    if empresa:
        print("Ingrese los nuevos datos (deje en blanco para mantener el valor actual):")
        nuevos_datos = {}
        nombre = input_validado(f"Nombre [{empresa.nombre}]: ", 
                                lambda x: len(x) > 0 or x == "", 
                                "El nombre no puede estar vacío.")
        if nombre: nuevos_datos['nombre'] = nombre
        
        descripcion = input(f"Descripción [{empresa.descripcion}]: ")
        if descripcion: nuevos_datos['descripcion'] = descripcion
        
        direccion = input(f"Dirección [{empresa.direccion}]: ")
        if direccion: nuevos_datos['direccion'] = direccion
        
        telefono = input_validado(f"Teléfono [{empresa.telefono}]: ", 
                                  lambda x: validar_telefono(x) or x == "", 
                                  "Formato de teléfono inválido.")
        if telefono: nuevos_datos['telefono'] = telefono
        
        correo = input_validado(f"Correo [{empresa.correo}]: ", 
                                lambda x: validar_correo(x) or x == "", 
                                "Formato de correo electrónico inválido.")
        if correo: nuevos_datos['correo'] = correo
        
        gerente = input(f"Gerente [{empresa.gerente}]: ")
        if gerente: nuevos_datos['gerente'] = gerente
        
        equipo_contacto = input(f"Equipo de contacto [{empresa.equipo_contacto}]: ")
        if equipo_contacto: nuevos_datos['equipo_contacto'] = equipo_contacto

        if empresas.modificar_empresa(id, nuevos_datos):
            print("Empresa modificada con éxito.")
        else:
            print("Error al modificar la empresa.")
    else:
        print("Empresa no encontrada.")

def eliminar_empresa(empresas):
    id = input("Ingrese el ID de la empresa a eliminar: ")
    if empresas.eliminar_empresa(id):
        print("Empresa eliminada con éxito.")
    else:
        print("Empresa no encontrada o error al eliminar.")

#Métodos entradas para el segundo módulo
def crear_proyecto(empresa):
    print("Creando nuevo proyecto:")
    id = input_validado("ID del proyecto: ", lambda x: x.isalnum(), "El ID debe ser alfanumérico.")
    nombre = input_validado("Nombre del proyecto: ", lambda x: len(x) > 0, "El nombre no puede estar vacío.")
    descripcion = input("Descripción del proyecto: ")
    fecha_inicio = input_validado("Fecha de inicio (YYYY-MM-DD): ", 
                                  lambda x: validar_fecha(x) is not None, 
                                  "Formato de fecha inválido. Use YYYY-MM-DD.")
    fecha_vencimiento = input_validado("Fecha de vencimiento (YYYY-MM-DD): ", 
                                       lambda x: validar_fecha(x) is not None and validar_fecha(x) > validar_fecha(fecha_inicio), 
                                       "Fecha inválida. Debe ser posterior a la fecha de inicio.")
    estado_actual = input("Estado actual del proyecto: ")
    gerente = input("Gerente del proyecto: ")
    equipo = input("Equipo del proyecto: ")

    nuevo_proyecto = Proyecto(id, nombre, descripcion, validar_fecha(fecha_inicio), 
                              validar_fecha(fecha_vencimiento), estado_actual, empresa.nombre, gerente, equipo)
    nuevo_proyecto.tareas = ArbolNArio() 
    empresa.proyectos.insertar_proyecto(nuevo_proyecto)
    print("Proyecto creado con éxito.")

def modificar_proyecto(empresa):
    id_proyecto = input("Ingrese el ID del proyecto a modificar: ")
    proyecto = empresa.proyectos.buscar_proyecto('id', id_proyecto)
    if proyecto:
        print(f"Modificando proyecto: {proyecto}")
        nombre = input_validado(f"Nuevo nombre [{proyecto.nombre}]: ", 
                                lambda x: len(x) > 0 or x == "", 
                                "El nombre no puede estar vacío.")
        if nombre: proyecto.nombre = nombre
        
        descripcion = input(f"Nueva descripción [{proyecto.descripcion}]: ")
        if descripcion: proyecto.descripcion = descripcion
        
        fecha_inicio = input_validado(f"Nueva fecha de inicio [{proyecto.fecha_inicio.strftime('%Y-%m-%d')}]: ", 
                                      lambda x: validar_fecha(x) is not None or x == "", 
                                      "Formato de fecha inválido. Use YYYY-MM-DD.")
        if fecha_inicio: proyecto.fecha_inicio = validar_fecha(fecha_inicio)
        
        fecha_vencimiento = input_validado(f"Nueva fecha de vencimiento [{proyecto.fecha_vencimiento.strftime('%Y-%m-%d')}]: ", 
                                           lambda x: (validar_fecha(x) is not None and validar_fecha(x) > proyecto.fecha_inicio) or x == "", 
                                           "Fecha inválida. Debe ser posterior a la fecha de inicio.")
        if fecha_vencimiento: proyecto.fecha_vencimiento = validar_fecha(fecha_vencimiento)
        
        estado_actual = input(f"Nuevo estado actual [{proyecto.estado_actual}]: ")
        if estado_actual: proyecto.estado_actual = estado_actual
        
        gerente = input(f"Nuevo gerente [{proyecto.gerente}]: ")
        if gerente: proyecto.gerente = gerente
        
        equipo = input(f"Nuevo equipo [{proyecto.equipo}]: ")
        if equipo: proyecto.equipo = equipo
        
        # Actualizar la posición en el árbol AVL
        empresa.proyectos.eliminar_proyecto(proyecto)
        empresa.proyectos.insertar_proyecto(proyecto)
        
        print("Proyecto modificado con éxito.")
    else:
        print("Proyecto no encontrado.")

def consultar_proyecto(empresa):
    id_proyecto = input("Ingrese el ID del proyecto a consultar: ")
    proyecto = empresa.proyectos.buscar_proyecto('id', id_proyecto)
    if proyecto:
        print(f"Detalles del proyecto:\n"
              f"ID: {proyecto.id}\n"
              f"Nombre: {proyecto.nombre}\n"
              f"Descripción: {proyecto.descripcion}\n"
              f"Fecha de inicio: {proyecto.fecha_inicio.strftime('%Y-%m-%d')}\n"
              f"Fecha de vencimiento: {proyecto.fecha_vencimiento.strftime('%Y-%m-%d')}\n"
              f"Estado actual: {proyecto.estado_actual}\n"
              f"Empresa: {proyecto.empresa}\n"
              f"Gerente: {proyecto.gerente}\n"
              f"Equipo: {proyecto.equipo}")
    else:
        print("Proyecto no encontrado.")

def eliminar_proyecto(empresa):
    id_proyecto = input("Ingrese el ID del proyecto a eliminar: ")
    proyecto = empresa.proyectos.buscar_proyecto('id', id_proyecto)
    if proyecto:
        confirmacion = input(f"¿Está seguro de que desea eliminar el proyecto '{proyecto.nombre}'? (s/n): ")
        if confirmacion.lower() == 's':
            empresa.proyectos.eliminar_proyecto(proyecto)
            print("Proyecto eliminado con éxito.")
        else:
            print("Eliminación cancelada.")
    else:
        print("Proyecto no encontrado.")

def listar_proyectos(empresa):
    print(f"Listado de proyectos de la empresa {empresa.nombre}:")
    empresa.proyectos.listar_proyectos()

#Métodos entradas para el tercer módulo
def crear_tarea(proyecto):
    print("Creando nueva tarea:")
    id = input_validado("ID de la tarea: ", lambda x: x.isalnum(), "El ID debe ser alfanumérico.")
    nombre = input_validado("Nombre de la tarea: ", lambda x: len(x) > 0, "El nombre no puede estar vacío.")
    descripcion = input("Descripción de la tarea: ")
    fecha_inicio = input_validado("Fecha de inicio (YYYY-MM-DD): ", 
                                  lambda x: validar_fecha(x) is not None, 
                                  "Formato de fecha inválido. Use YYYY-MM-DD.")
    fecha_vencimiento = input_validado("Fecha de vencimiento (YYYY-MM-DD): ", 
                                       lambda x: validar_fecha(x) is not None and validar_fecha(x) > validar_fecha(fecha_inicio), 
                                       "Fecha inválida. Debe ser posterior a la fecha de inicio.")
    estado_actual = input("Estado actual de la tarea: ")
    porcentaje = input_validado("Porcentaje de progreso (0-100): ", 
                                validar_porcentaje, 
                                "El porcentaje debe ser un número entre 0 y 100.")

    nueva_tarea = Tarea(id, nombre, proyecto.empresa, descripcion, validar_fecha(fecha_inicio), 
                        validar_fecha(fecha_vencimiento), estado_actual, int(porcentaje))

    id_tarea_padre = input("ID de la tarea padre (dejar en blanco si es tarea principal): ")
    if id_tarea_padre:
        tarea_padre = proyecto.tareas.consultar_tarea(id_tarea_padre)
        if tarea_padre:
            proyecto.tareas.agregar_tarea(nueva_tarea, tarea_padre)
        else:
            print("Tarea padre no encontrada. Se añadirá como tarea principal.")
            proyecto.tareas.agregar_tarea(nueva_tarea)
    else:
        proyecto.tareas.agregar_tarea(nueva_tarea)

    print("Tarea creada con éxito.")
    guardar_tareas_json(proyecto)

def modificar_tarea(proyecto):
    id_tarea = input("Ingrese el ID de la tarea a modificar: ")
    tarea = proyecto.tareas.consultar_tarea(id_tarea)
    if tarea:
        print(f"Modificando tarea: {tarea}")
        nuevos_datos = {}
        nombre = input_validado(f"Nuevo nombre [{tarea.nombre}]: ", 
                                lambda x: len(x) > 0 or x == "", 
                                "El nombre no puede estar vacío.")
        if nombre: nuevos_datos['nombre'] = nombre

        descripcion = input(f"Nueva descripción [{tarea.descripcion}]: ")
        if descripcion: nuevos_datos['descripcion'] = descripcion

        fecha_inicio = input_validado(f"Nueva fecha de inicio [{tarea.fecha_inicio}] (YYYY-MM-DD): ", 
                                      lambda x: validar_fecha(x) is not None or x == "", 
                                      "Formato de fecha inválido. Use YYYY-MM-DD.")
        if fecha_inicio: nuevos_datos['fecha_inicio'] = validar_fecha(fecha_inicio)

        fecha_vencimiento = input_validado(f"Nueva fecha de vencimiento [{tarea.fecha_vencimiento}] (YYYY-MM-DD): ", 
                                           lambda x: (validar_fecha(x) is not None and validar_fecha(x) > tarea.fecha_inicio) or x == "", 
                                           "Fecha inválida. Debe ser posterior a la fecha de inicio.")
        if fecha_vencimiento: nuevos_datos['fecha_vencimiento'] = validar_fecha(fecha_vencimiento)

        estado_actual = input(f"Nuevo estado actual [{tarea.estado_actual}]: ")
        if estado_actual: nuevos_datos['estado_actual'] = estado_actual

        porcentaje = input_validado(f"Nuevo porcentaje de progreso [{tarea.porcentaje}] (0-100): ", 
                                    lambda x: validar_porcentaje(x) or x == "", 
                                    "El porcentaje debe ser un número entre 0 y 100.")
        if porcentaje: nuevos_datos['porcentaje'] = int(porcentaje)

        if proyecto.tareas.modificar_tarea(id_tarea, nuevos_datos):
            print("Tarea modificada con éxito.")
            guardar_tareas_json(proyecto)
        else:
            print("Error al modificar la tarea.")
    else:
        print("Tarea no encontrada.")

def eliminar_tarea(proyecto):
    id_tarea = input("Ingrese el ID de la tarea a eliminar: ")
    if proyecto.tareas.eliminar_tarea(id_tarea):
        print("Tarea y sus subtareas eliminadas con éxito.")
        guardar_tareas_json(proyecto)
    else:
        print("Tarea no encontrada o error al eliminar.")

def listar_tareas(proyecto):
    nivel = input("Ingrese el nivel de tareas a mostrar (dejar en blanco para mostrar todas): ")
    if nivel:
        try:
            nivel = int(nivel)
            proyecto.tareas.listar_tareas(nivel)
        except ValueError:
            print("Nivel inválido. Mostrando todas las tareas.")
            proyecto.tareas.listar_tareas()
    else:
        proyecto.tareas.listar_tareas()

def mostrar_subtareas(proyecto):
    id_tarea = input("Ingrese el ID de la tarea para mostrar sus subtareas: ")
    proyecto.tareas.mostrar_subtareas(id_tarea)

def guardar_tareas_json(proyecto):
    def serializar_tarea(tarea):
        return {
            'id': tarea.id,
            'nombre': tarea.nombre,
            'empresa_cliente': tarea.empresa_cliente,
            'descripcion': tarea.descripcion,
            'fecha_inicio': tarea.fecha_inicio.isoformat(),
            'fecha_vencimiento': tarea.fecha_vencimiento.isoformat(),
            'estado_actual': tarea.estado_actual,
            'porcentaje': tarea.porcentaje,
            'subtareas': [serializar_tarea(subtarea) for subtarea in tarea.subtareas]
        }

    tareas_json = json.dumps(serializar_tarea(proyecto.tareas.raiz) if proyecto.tareas.raiz else {})
    with open(f'tareas_proyecto_{proyecto.id}.json', 'w') as f:
        f.write(tareas_json)

def cargar_tareas_json(proyecto):
    try:
        with open(f'tareas_proyecto_{proyecto.id}.json', 'r') as f:
            tareas_data = json.load(f)
        
        def deserializar_tarea(data):
            if not data:
                return None
            tarea = Tarea(
                data['id'],
                data['nombre'],
                data['empresa_cliente'],
                data['descripcion'],
                date.fromisoformat(data['fecha_inicio']),
                date.fromisoformat(data['fecha_vencimiento']),
                data['estado_actual'],
                data['porcentaje']
            )
            for subtarea_data in data.get('subtareas', []):
                subtarea = deserializar_tarea(subtarea_data)
                if subtarea:
                    tarea.subtareas.append(subtarea)
            return tarea

        proyecto.tareas = ArbolNArio()
        proyecto.tareas.raiz = deserializar_tarea(tareas_data)
    except FileNotFoundError:
        print(f"No se encontró archivo de tareas para el proyecto {proyecto.id}. Se iniciará con un árbol vacío.")
        proyecto.tareas = ArbolNArio()

#Métodos entradas para el cuarto módulo
def crear_sprint(proyecto):
    print("Creando nuevo sprint:")
    id = input_validado("ID del sprint: ", lambda x: x.isalnum(), "El ID debe ser alfanumérico.")
    nombre = input_validado("Nombre del sprint: ", lambda x: len(x) > 0, "El nombre no puede estar vacío.")
    fecha_inicio = input_validado("Fecha de inicio (YYYY-MM-DD): ", 
                                  lambda x: validar_fecha(x) is not None, 
                                  "Formato de fecha inválido. Use YYYY-MM-DD.")
    fecha_fin = input_validado("Fecha de fin (YYYY-MM-DD): ", 
                               lambda x: validar_fecha(x) is not None and validar_fecha(x) > validar_fecha(fecha_inicio), 
                               "Fecha inválida. Debe ser posterior a la fecha de inicio.")
    estado = input("Estado del sprint: ")
    objetivos = input("Objetivos del sprint: ")
    equipo = input("Equipo del sprint: ")

    nuevo_sprint = Sprint(id, nombre, validar_fecha(fecha_inicio), validar_fecha(fecha_fin), estado, objetivos, equipo)
    proyecto.sprints.insertar_sprint(nuevo_sprint)
    print("Sprint creado con éxito.")
    guardar_sprints_json(proyecto)

def modificar_sprint(proyecto):
    id_sprint = input("Ingrese el ID del sprint a modificar: ")
    nodo_sprint = proyecto.sprints.buscar_sprint(id_sprint)
    if nodo_sprint:
        sprint = nodo_sprint.sprint
        print(f"Modificando sprint: {sprint}")
        nombre = input_validado(f"Nuevo nombre [{sprint.nombre}]: ", 
                                lambda x: len(x) > 0 or x == "", 
                                "El nombre no puede estar vacío.")
        if nombre: sprint.nombre = nombre

        fecha_inicio = input_validado(f"Nueva fecha de inicio [{sprint.fecha_inicio}] (YYYY-MM-DD): ", 
                                      lambda x: validar_fecha(x) is not None or x == "", 
                                      "Formato de fecha inválido. Use YYYY-MM-DD.")
        if fecha_inicio: sprint.fecha_inicio = validar_fecha(fecha_inicio)

        fecha_fin = input_validado(f"Nueva fecha de fin [{sprint.fecha_fin}] (YYYY-MM-DD): ", 
                                   lambda x: (validar_fecha(x) is not None and validar_fecha(x) > sprint.fecha_inicio) or x == "", 
                                   "Fecha inválida. Debe ser posterior a la fecha de inicio.")
        if fecha_fin: sprint.fecha_fin = validar_fecha(fecha_fin)

        estado = input(f"Nuevo estado [{sprint.estado}]: ")
        if estado: sprint.estado = estado

        objetivos = input(f"Nuevos objetivos [{sprint.objetivos}]: ")
        if objetivos: sprint.objetivos = objetivos

        equipo = input(f"Nuevo equipo [{sprint.equipo}]: ")
        if equipo: sprint.equipo = equipo

        print("Sprint modificado con éxito.")
        guardar_sprints_json(proyecto)
    else:
        print("Sprint no encontrado.")

def eliminar_sprint(proyecto):
    id_sprint = input("Ingrese el ID del sprint a eliminar: ")
    nodo_sprint = proyecto.sprints.buscar_sprint(id_sprint)
    if nodo_sprint:
        # Implementar la lógica de eliminación en el árbol AVL
        print("Sprint eliminado con éxito.")
        guardar_sprints_json(proyecto)
    else:
        print("Sprint no encontrado.")

def listar_sprints(proyecto):
    print(f"Listado de sprints del proyecto {proyecto.nombre}:")
    proyecto.sprints.listar_sprints()

def agregar_tarea_sprint(proyecto):
    id_sprint = input("Ingrese el ID del sprint al que desea agregar una tarea: ")
    nodo_sprint = proyecto.sprints.buscar_sprint(id_sprint)
    if nodo_sprint:
        sprint = nodo_sprint.sprint
        print("Tareas disponibles para agregar al sprint:")
        todas_tareas = obtener_todas_tareas(proyecto.tareas)
        tareas_disponibles = [tarea for tarea in todas_tareas 
                              if tarea.estado_actual != "Completada" and not tarea_en_sprint(tarea, proyecto.sprints)]
        for i, tarea in enumerate(tareas_disponibles):
            print(f"{i+1}. {tarea}")
        
        if not tareas_disponibles:
            print("No hay tareas disponibles para agregar al sprint.")
            return

        seleccion = input("Ingrese el número de la tarea que desea agregar (o 0 para cancelar): ")
        try:
            seleccion = int(seleccion)
            if 1 <= seleccion <= len(tareas_disponibles):
                tarea_seleccionada = tareas_disponibles[seleccion-1]
                sprint.tareas.agregar_tarea(tarea_seleccionada)
                print(f"Tarea '{tarea_seleccionada.nombre}' agregada al sprint '{sprint.nombre}'.")
                guardar_sprints_json(proyecto)
            elif seleccion != 0:
                print("Selección inválida.")
        except ValueError:
            print("Por favor, ingrese un número válido.")
    else:
        print("Sprint no encontrado.")

def obtener_todas_tareas(arbol_tareas):
    tareas = []
    
    def recorrer_arbol(nodo):
        if nodo:
            tareas.append(nodo.tarea)
            for hijo in nodo.hijos:
                recorrer_arbol(hijo)
    
    if arbol_tareas and arbol_tareas.raiz:
        recorrer_arbol(arbol_tareas.raiz)
    return tareas

def tarea_en_sprint(tarea, sprints):
    def buscar_tarea_en_sprint(nodo_sprint):
        if not nodo_sprint:
            return False
        actual = nodo_sprint.sprint.tareas.cabeza
        while actual:
            if actual.tarea.id == tarea.id:
                return True
            actual = actual.siguiente
        return (buscar_tarea_en_sprint(nodo_sprint.izquierda) or 
                buscar_tarea_en_sprint(nodo_sprint.derecha))
    
    return buscar_tarea_en_sprint(sprints.raiz)

def guardar_sprints_json(proyecto):
    def serializar_sprint(sprint):
        return {
            'id': sprint.id,
            'nombre': sprint.nombre,
            'fecha_inicio': sprint.fecha_inicio.isoformat(),
            'fecha_fin': sprint.fecha_fin.isoformat(),
            'estado': sprint.estado,
            'objetivos': sprint.objetivos,
            'equipo': sprint.equipo,
            'tareas': [tarea.id for tarea in obtener_tareas_sprint(sprint)]
        }

    def serializar_arbol_sprints(nodo):
        if not nodo:
            return None
        return {
            'sprint': serializar_sprint(nodo.sprint),
            'izquierda': serializar_arbol_sprints(nodo.izquierda),
            'derecha': serializar_arbol_sprints(nodo.derecha)
        }

    sprints_json = json.dumps(serializar_arbol_sprints(proyecto.sprints.raiz))
    with open(f'sprints_proyecto_{proyecto.id}.json', 'w') as f:
        f.write(sprints_json)

def cargar_sprints_json(proyecto):
    try:
        with open(f'sprints_proyecto_{proyecto.id}.json', 'r') as f:
            sprints_data = json.load(f)
        
        def deserializar_sprint(data, todas_tareas):
            sprint = Sprint(
                data['id'],
                data['nombre'],
                date.fromisoformat(data['fecha_inicio']),
                date.fromisoformat(data['fecha_fin']),
                data['estado'],
                data['objetivos'],
                data['equipo']
            )
            for tarea_id in data['tareas']:
                tarea = next((t for t in todas_tareas if t.id == tarea_id), None)
                if tarea:
                    sprint.tareas.agregar_tarea(tarea)
            return sprint

        def deserializar_arbol_sprints(nodo_data, todas_tareas):
            if not nodo_data:
                return None
            sprint = deserializar_sprint(nodo_data['sprint'], todas_tareas)
            nodo = NodoAVLSprint(sprint)
            nodo.izquierda = deserializar_arbol_sprints(nodo_data['izquierda'], todas_tareas)
            nodo.derecha = deserializar_arbol_sprints(nodo_data['derecha'], todas_tareas)
            return nodo

        todas_tareas = obtener_todas_tareas(proyecto.tareas) if proyecto.tareas else []
        proyecto.sprints = ArbolAVLSprints()
        proyecto.sprints.raiz = deserializar_arbol_sprints(sprints_data, todas_tareas)
    except FileNotFoundError:
        print(f"No se encontró archivo de sprints para el proyecto {proyecto.id}. Se iniciará con un árbol vacío.")
        proyecto.sprints = ArbolAVLSprints()

def obtener_tareas_sprint(sprint):
    tareas = []
    actual = sprint.tareas.cabeza
    while actual:
        tareas.append(actual.tarea)
        actual = actual.siguiente
    return tareas

def mostrar_tareas_sprint(proyecto):
    id_sprint = input("Ingrese el ID del sprint cuyas tareas desea ver: ")
    nodo_sprint = proyecto.sprints.buscar_sprint(id_sprint)
    if nodo_sprint:
        sprint = nodo_sprint.sprint
        print(f"Tareas del sprint '{sprint.nombre}':")
        sprint.tareas.listar_tareas()
    else:
        print("Sprint no encontrado.")

#Métodos entreadas para el quinto módulo
def mostrar_tareas_criticas(empresas):
    empresa = seleccionar_empresa(empresas)
    if not empresa:
        return
    proyecto = seleccionar_proyecto(empresa)
    if not proyecto:
        return
    
    tareas_criticas = []
    def recorrer_postorden(nodo):
        if nodo:
            for hijo in nodo.hijos:
                recorrer_postorden(hijo)
            if es_tarea_critica(nodo.tarea):
                tareas_criticas.append(nodo.tarea)
    
    recorrer_postorden(proyecto.tareas.raiz)
    
    print(f"\nTareas críticas del proyecto '{proyecto.nombre}':")
    for tarea in tareas_criticas:
        print(f"- {tarea.nombre}: Duración: {tarea.duracion} horas, Fecha límite: {tarea.fecha_vencimiento}")

def es_tarea_critica(tarea):
    # Implementa la lógica para determinar si una tarea es crítica
    # Por ejemplo, si la tarea está cerca de su fecha límite y tiene una duración significativa
    dias_restantes = (tarea.fecha_vencimiento - date.today()).days
    return dias_restantes <= 7 and tarea.duracion >= 20  # Ejemplo: 7 días o menos y 20 horas o más

def listar_sprints_y_tareas(empresas):
    empresa = seleccionar_empresa(empresas)
    if not empresa:
        return
    proyecto = seleccionar_proyecto(empresa)
    if not proyecto:
        return
    
    nivel = int(input("Ingrese el nivel del árbol de sprints a mostrar: "))
    
    def mostrar_sprint(nodo, nivel_actual):
        if nodo and nivel_actual <= nivel:
            print(f"{'  ' * nivel_actual}Sprint: {nodo.sprint}")
            print(f"{'  ' * (nivel_actual + 1)}Tareas:")
            mostrar_tareas_preorden(nodo.sprint.tareas.cabeza, nivel_actual + 2)
            mostrar_sprint(nodo.izquierda, nivel_actual + 1)
            mostrar_sprint(nodo.derecha, nivel_actual + 1)
    
    mostrar_sprint(proyecto.sprints.raiz, 0)

def mostrar_tareas_preorden(nodo_tarea, nivel):
    if nodo_tarea:
        print(f"{'  ' * nivel}{nodo_tarea.tarea}")
        mostrar_subtareas(nodo_tarea.tarea, nivel + 1)

def mostrar_subtareas(tarea, nivel):
    print("  " * nivel + str(tarea))
    for subtarea in tarea.subtareas:
        mostrar_subtareas(subtarea, nivel + 1)

def listar_tareas_por_empleado(empresas):
    cedula = input("Ingrese la cédula del empleado: ")
    tareas_por_proyecto = defaultdict(list)
    
    def recorrer_postorden(nodo, proyecto):
        if nodo:
            for hijo in nodo.hijos:
                recorrer_postorden(hijo, proyecto)
            if nodo.tarea.empleado_cedula == cedula:
                tareas_por_proyecto[proyecto].append(nodo.tarea)
    
    for empresa in empresas.obtener_todas_empresas():
        for proyecto in empresa.proyectos.obtener_todos_proyectos():
            recorrer_postorden(proyecto.tareas.raiz, proyecto)
    
    for proyecto, tareas in tareas_por_proyecto.items():
        total_horas = sum(tarea.duracion for tarea in tareas)
        print(f"\n{proyecto.nombre} - {total_horas} horas")
        for tarea in tareas:
            print(f"-{tarea.nombre} {tarea.duracion} horas")

def exportar_tareas_completadas(empresas):
    empresa = seleccionar_empresa(empresas)
    if not empresa:
        return
    proyecto = seleccionar_proyecto(empresa)
    if not proyecto:
        return
    
    duracion_maxima = float(input("Ingrese la duración máxima en horas: "))
    nombre_archivo = input("Ingrese el nombre del archivo CSV para exportar: ")
    
    tareas_completadas = []
    def recorrer_postorden(nodo):
        if nodo:
            for hijo in nodo.hijos:
                recorrer_postorden(hijo)
            if nodo.tarea.estado_actual == "Completada" and nodo.tarea.duracion <= duracion_maxima:
                tareas_completadas.append(nodo.tarea)
    
    recorrer_postorden(proyecto.tareas.raiz)
    
    with open(nombre_archivo, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Nombre", "Descripción", "Fecha Inicio", "Fecha Vencimiento", "Duración", "Empleado"])
        for tarea in tareas_completadas:
            writer.writerow([tarea.id, tarea.nombre, tarea.descripcion, tarea.fecha_inicio, 
                             tarea.fecha_vencimiento, tarea.duracion, tarea.empleado_cedula])
    
    print(f"Tareas exportadas exitosamente a {nombre_archivo}")

def seleccionar_empresa(empresas):
    print("\nEmpresas disponibles:")
    todas_empresas = empresas.obtener_todas_empresas()
    for i, empresa in enumerate(todas_empresas):
        print(f"{i+1}. {empresa.nombre}")
    
    seleccion = int(input("Seleccione el número de la empresa: ")) - 1
    if 0 <= seleccion < len(todas_empresas):
        return todas_empresas[seleccion]
    else:
        print("Selección inválida.")
        return None

def seleccionar_proyecto(empresa):
    print(f"\nProyectos de {empresa.nombre}:")
    proyectos = empresa.proyectos.obtener_todos_proyectos()
    for i, proyecto in enumerate(proyectos):
        print(f"{i+1}. {proyecto.nombre}")
    
    seleccion = int(input("Seleccione el número del proyecto: ")) - 1
    if 0 <= seleccion < len(proyectos):
        return proyectos[seleccion]
    else:
        print("Selección inválida.")
        return None
#--------------------------------------------------Menú Reportes---------------------------------------------------------------------------------------------------------------
def menu_reportes(empresas):
    while True:
        print("\n--- Módulo de Reportes ---")
        print("1. Mostrar tareas críticas")
        print("2. Listar sprints y tareas de un proyecto")
        print("3. Listar tareas por empleado")
        print("4. Exportar tareas completadas")
        print("5. Volver al menú principal")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            mostrar_tareas_criticas(empresas)
        elif opcion == '2':
            listar_sprints_y_tareas(empresas)
        elif opcion == '3':
            listar_tareas_por_empleado(empresas)
        elif opcion == '4':
            exportar_tareas_completadas(empresas)
        elif opcion == '5':
            break
        else:
            print("Opción no válida. Intente de nuevo.")
#--------------------------------------------------Menú Sprints---------------------------------------------------------------------------------------------------------------
def gestionar_sprints(proyecto):
    cargar_sprints_json(proyecto)
    while True:
        print(f"\n--- Gestión de Sprints para el Proyecto {proyecto.nombre} ---")
        print("1. Crear sprint")
        print("2. Modificar sprint")
        print("3. Eliminar sprint")
        print("4. Listar sprints")
        print("5. Agregar tarea a sprint")
        print("6. Mostrar tareas de un sprint")
        print("7. Volver al menú de proyectos")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            crear_sprint(proyecto)
        elif opcion == '2':
            modificar_sprint(proyecto)
        elif opcion == '3':
            eliminar_sprint(proyecto)
        elif opcion == '4':
            listar_sprints(proyecto)
        elif opcion == '5':
            agregar_tarea_sprint(proyecto)
        elif opcion == '6':
            mostrar_tareas_sprint(proyecto)
        elif opcion == '7':
            break
        else:
            print("Opción no válida. Intente de nuevo.")
#--------------------------------------------------Menú Tareas---------------------------------------------------------------------------------------------------------------
def gestionar_tareas(proyecto):
    cargar_tareas_json(proyecto)
    while True:
        print(f"\n--- Gestión de Tareas para el Proyecto {proyecto.nombre} ---")
        print("1. Crear tarea")
        print("2. Modificar tarea")
        print("3. Eliminar tarea")
        print("4. Listar tareas")
        print("5. Mostrar subtareas de una tarea")
        print("6. Volver al menú de proyectos")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            crear_tarea(proyecto)
        elif opcion == '2':
            modificar_tarea(proyecto)
        elif opcion == '3':
            eliminar_tarea(proyecto)
        elif opcion == '4':
            listar_tareas(proyecto)
        elif opcion == '5':
            id_tarea = input("Ingrese el ID de la tarea para mostrar sus subtareas: ")
            tarea = proyecto.tareas.consultar_tarea(id_tarea)
            if tarea:
                mostrar_subtareas(tarea, 0)  # Comenzamos en el nivel 0
            else:
                print("Tarea no encontrada.")
        elif opcion == '6':
            break
        else:
            print("Opción no válida. Intente de nuevo.")
#--------------------------------------------------Menú Proyectos-------------------------------------------------------------------------------------------------------------
def gestionar_proyectos(empresa):
    while True:
        print("\n--- Gestión de Proyectos ---")
        print("1. Crear proyecto")
        print("2. Modificar proyecto")
        print("3. Consultar proyecto")
        print("4. Eliminar proyecto")
        print("5. Listar proyectos")
        print("6. Gestionar tareas de un proyecto")
        print("7. Gestionar sprints de un proyecto")
        print("8. Volver al menú principal")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            crear_proyecto(empresa)
        elif opcion == '2':
            modificar_proyecto(empresa)
        elif opcion == '3':
            consultar_proyecto(empresa)
        elif opcion == '4':
            eliminar_proyecto(empresa)
        elif opcion == '5':
            listar_proyectos(empresa)
        elif opcion == '6':
            id_proyecto = input("Ingrese el ID del proyecto cuyas tareas desea gestionar: ")
            proyecto = empresa.proyectos.buscar_proyecto('id', id_proyecto)
            if proyecto:
                gestionar_tareas(proyecto)
            else:
                print("Proyecto no encontrado.")
        elif opcion == '7':
            id_proyecto = input("Ingrese el ID del proyecto cuyos sprints desea gestionar: ")
            proyecto = empresa.proyectos.buscar_proyecto('id', id_proyecto)
            if proyecto:
                gestionar_sprints(proyecto)
            else:
                print("Proyecto no encontrado.")
        elif opcion == '8':
            break
        else:
            print("Opción no válida. Intente de nuevo.")

#--------------------------------------------------Menú Empresas-------------------------------------------------------------------------------------------------------------
def menu_empresas(empresas):
    while True:
        print("\n--- Gestión de Empresas ---")
        print("1. Crear empresa")
        print("2. Listar empresas")
        print("3. Consultar empresa")
        print("4. Modificar empresa")
        print("5. Eliminar empresa")
        print("6. Gestionar proyectos de una empresa")
        print("7. Volver al menú principal")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            crear_empresa(empresas)
        elif opcion == '2':
            empresas.listar_empresas()
        elif opcion == '3':
            consultar_empresa(empresas)
        elif opcion == '4':
            modificar_empresa(empresas)
        elif opcion == '5':
            eliminar_empresa(empresas)
        elif opcion == '6':
            id_empresa = input("Ingrese el ID de la empresa cuyos proyectos desea gestionar: ")
            empresa = empresas.buscar_empresa(id_empresa)
            if empresa:
                gestionar_proyectos(empresa)
            else:
                print("Empresa no encontrada.")
        elif opcion == '7':
            break
        else:
            print("Opción no válida. Intente de nuevo.")

#--------------------------------------------------Menú Principal-------------------------------------------------------------------------------------------------------------
def menu_principal(empresas):
    while True:
        print("\n--- Sistema Avanzado de Gestión de Proyectos y Tareas ---")
        print("1. Gestión de Empresas")
        print("2. Gestión de Proyectos")
        print("3. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            menu_empresas(empresas)
        elif opcion == '2':
            id_empresa = input("Ingrese el ID de la empresa cuyos proyectos desea gestionar: ")
            empresa = empresas.buscar_empresa(id_empresa)
            if empresa:
                gestionar_proyectos(empresa)
            else:
                print("Empresa no encontrada.")
        elif opcion == '3':
            print("Gracias por usar el Sistema Avanzado de Gestión de Proyectos y Tareas.")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

#Llamada menú 
def main():
    archivo_csv = 'empresas.csv'
    try:
        empresas = cargar_empresas_desde_csv(archivo_csv)
    except FileNotFoundError:
        print(f"El archivo {archivo_csv} no se encontró. Se creará una nueva lista de empresas.")
        empresas = ListaEnlazadaEmpresas()
    
    while True:
        print("\n--- Sistema Avanzado de Gestión de Proyectos y Tareas ---")
        print("1. Gestión de Empresas")
        print("2. Gestión de Proyectos")
        print("3. Reportes")
        print("4. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            menu_empresas(empresas)
        elif opcion == '2':
            gestionar_proyectos(empresas)
        elif opcion == '3':
            menu_reportes(empresas)
        elif opcion == '4':
            break
        else:
            print("Opción no válida. Intente de nuevo.")
    
    guardar_empresas_en_csv(empresas, archivo_csv)
    print(f"Datos guardados en {archivo_csv}")

if __name__ == "__main__":
    main()
"""
Estructura de Árboles

Elaborado por:

- Cristian Guevara. C.I: 31.567.525
- Rodrigo Torres. C.I: 31.014.592
"""
import json
from datetime import datetime


#1.- Modulo de Gestión de Empreseas--------------------------------------------------------------------------------------------------------------------------------------------
import csv

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
        self.proyectos = []

    def __str__(self):
        return f"ID: {self.id}, Nombre: {self.nombre}, Descripción: {self.descripcion}, Fecha de Creación: {self.fecha_creacion}, Dirección: {self.direccion}, Teléfono: {self.telefono}, Correo: {self.correo}, Gerente: {self.gerente}, Equipo de Contacto: {self.equipo_contacto}"

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
                    empresa = Empresa(
                        row.get('id', ''),
                        row.get('nombre', ''),
                        row.get('descripcion', ''),
                        row.get('fecha_creacion', ''),
                        row.get('direccion', ''),
                        row.get('telefono', ''),
                        row.get('correo', ''),
                        row.get('gerente', ''),
                        row.get('equipo_contacto', '')
                    )
                    empresas.append(empresa)
        except FileNotFoundError:
            pass
        return empresas

    def cargar_empresas(self):
        empresas = []
        try:
            with open(self.archivo_csv, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    empresa = Empresa(
                        row.get('id', ''),
                        row.get('nombre', ''),
                        row.get('descripcion', ''),
                        row.get('fecha_creacion', ''),
                        row.get('direccion', ''),
                        row.get('telefono', ''),
                        row.get('correo', ''),
                        row.get('gerente', ''),
                        row.get('equipo_contacto', '')
                    )
                    empresas.append(empresa)
        except FileNotFoundError:
            pass
        return empresas

    def guardar_empresas(self):
        with open(self.archivo_csv, 'w', newline='') as csvfile:
            fieldnames = ['id', 'nombre', 'descripcion', 'fecha_creacion', 'direccion', 'telefono', 'correo', 'gerente', 'equipo_contacto']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for empresa in self.empresas:
                writer.writerow({'id': empresa.id, 'nombre': empresa.nombre, 'descripcion': empresa.descripcion, 'fecha_creacion': empresa.fecha_creacion, 'direccion': empresa.direccion, 'telefono': empresa.telefono, 'correo': empresa.correo, 'gerente': empresa.gerente, 'equipo_contacto': empresa.equipo_contacto})

    def crear_empresa(self, id, nombre, descripcion, fecha_creacion, direccion, telefono, correo, gerente, equipo_contacto):
        nueva_empresa = Empresa(id, nombre, descripcion, fecha_creacion, direccion, telefono, correo, gerente, equipo_contacto)
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

    def modificar_empresa(self, id, nombre=None, descripcion=None, fecha_creacion=None, direccion=None, telefono=None, correo=None, gerente=None, equipo_contacto=None):
        empresa = self.buscar_empresa(id)
        if empresa:
            if nombre:
                empresa.nombre = nombre
            if descripcion:
                empresa.descripcion = descripcion
            if fecha_creacion:
                empresa.fecha_creacion = fecha_creacion
            if direccion:
                empresa.direccion = direccion
            if telefono:
                empresa.telefono = telefono
            if correo:
                empresa.correo = correo
            if gerente:
                empresa.gerente = gerente
            if equipo_contacto:
                empresa.equipo_contacto = equipo_contacto
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

    def agregar_proyecto(self, id_empresa, proyecto):
        empresa = self.buscar_empresa(id_empresa)
        if empresa:
            empresa.proyectos.append(proyecto)
            self.guardar_empresas()

# Ejemplo de uso
gestion_empresas = GestionEmpresas('empresas.csv')
gestion_empresas.crear_empresa('1', 'Empresa A', 'Descripción A', '2023-01-01', 'Direccion A', '123456789', 'correoA@empresa.com', 'Gerente A', 'Equipo A')
gestion_empresas.crear_empresa('2', 'Empresa B', 'Descripción B', '2023-02-01', 'Direccion B', '987654321', 'correoB@empresa.com', 'Gerente B', 'Equipo B')
gestion_empresas.listar_empresas()


#2.- Modulo de Gestión de Proyectos------------------------------------------------------------------------------------------------------------------------------------------------
class Proyecto:
    def __init__(self, id, nombre, descripcion, fecha_inicio, fecha_vencimiento, estado, empresa, gerente, equipo, tareas=None):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha_inicio = fecha_inicio
        self.fecha_vencimiento = fecha_vencimiento
        self.estado = estado
        self.empresa = empresa
        self.gerente = gerente
        self.equipo = equipo
        self.tareas = tareas if tareas else []

    def tiempo_restante(self):
        return (datetime.strptime(self.fecha_vencimiento, '%Y-%m-%d') - datetime.now()).days

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "fecha_inicio": self.fecha_inicio,
            "fecha_vencimiento": self.fecha_vencimiento,
            "estado": self.estado,
            "empresa": self.empresa,
            "gerente": self.gerente,
            "equipo": self.equipo,
            "tareas": [tarea.to_dict() for tarea in self.tareas]
        }
    
    def __str__(self):
        return f"ID: {self.id}, Nombre: {self.nombre}, Descripción: {self.descripcion}, Fecha de Inicio: {self.fecha_inicio}, Fecha de Vencimiento: {self.fecha_vencimiento}, Estado: {self.estado}, Empresa: {self.empresa}, Gerente: {self.gerente}, Equipo: {self.equipo}"

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

        if proyecto.tiempo_restante() < nodo.proyecto.tiempo_restante():
            nodo.izquierda = self.insertar(nodo.izquierda, proyecto)
        else:
            nodo.derecha = self.insertar(nodo.derecha, proyecto)

        nodo.altura = max(self.obtener_altura(nodo.izquierda), self.obtener_altura(nodo.derecha)) + 1

        balance = self.balancear(nodo)

        if balance > 1 and proyecto.tiempo_restante() < nodo.izquierda.proyecto.tiempo_restante():
            return self.rotar_derecha(nodo)

        if balance < -1 and proyecto.tiempo_restante() > nodo.derecha.proyecto.tiempo_restante():
            return self.rotar_izquierda(nodo)

        if balance > 1 and proyecto.tiempo_restante() > nodo.izquierda.proyecto.tiempo_restante():
            nodo.izquierda = self.rotar_izquierda(nodo.izquierda)
            return self.rotar_derecha(nodo)

        if balance < -1 and proyecto.tiempo_restante() < nodo.derecha.proyecto.tiempo_restante():
            nodo.derecha = self.rotar_derecha(nodo.derecha)
            return self.rotar_izquierda(nodo)

        return nodo

    def preorden(self, nodo):
        if not nodo:
            return
        print(nodo.proyecto)
        self.preorden(nodo.izquierda)
        self.preorden(nodo.derecha)

    def buscar(self, nodo, criterio, valor):
        if not nodo:
            return None

        if getattr(nodo.proyecto, criterio) == valor:
            return nodo.proyecto

        if getattr(nodo.proyecto, criterio) < valor:
            return self.buscar(nodo.derecha, criterio, valor)
        else:
            return self.buscar(nodo.izquierda, criterio, valor)

    def eliminar(self, nodo, proyecto):
        if not nodo:
            return nodo

        if proyecto.tiempo_restante() < nodo.proyecto.tiempo_restante():
            nodo.izquierda = self.eliminar(nodo.izquierda, proyecto)
        elif proyecto.tiempo_restante() > nodo.proyecto.tiempo_restante():
            nodo.derecha = self.eliminar(nodo.derecha, proyecto)
        else:
            if not nodo.izquierda:
                return nodo.derecha
            elif not nodo.derecha:
                return nodo.izquierda

            temp = self.obtener_nodo_menor_valor(nodo.derecha)
            nodo.proyecto = temp.proyecto
            nodo.derecha = self.eliminar(nodo.derecha, temp.proyecto)

        if not nodo:
            return nodo

        nodo.altura = max(self.obtener_altura(nodo.izquierda), self.obtener_altura(nodo.derecha)) + 1

        balance = self.balancear(nodo)

        if balance > 1 and self.balancear(nodo.izquierda) >= 0:
            return self.rotar_derecha(nodo)

        if balance > 1 and self.balancear(nodo.izquierda) < 0:
            nodo.izquierda = self.rotar_izquierda(nodo.izquierda)
            return self.rotar_derecha(nodo)

        if balance < -1 and self.balancear(nodo.derecha) <= 0:
            return self.rotar_izquierda(nodo)

        if balance < -1 and self.balancear(nodo.derecha) > 0:
            nodo.derecha = self.rotar_derecha(nodo.derecha)
            return self.rotar_izquierda(nodo)

        return nodo

    def obtener_nodo_menor_valor(self, nodo):
        if nodo is None or nodo.izquierda is None:
            return nodo
        return self.obtener_nodo_menor_valor(nodo.izquierda)

    def actualizar_arbol(self, nodo):
        if not nodo:
            return None
        proyectos = []
        self.recolectar_proyectos(nodo, proyectos)
        self.raiz = None
        for proyecto in proyectos:
            self.raiz = self.insertar(self.raiz, proyecto)

    def recolectar_proyectos(self, nodo, proyectos):
        if not nodo:
            return
        proyectos.append(nodo.proyecto)
        self.recolectar_proyectos(nodo.izquierda, proyectos)
        self.recolectar_proyectos(nodo.derecha, proyectos)

class GestionProyectos:
    def __init__(self, gestion_empresas):
        self.gestion_empresas = gestion_empresas
        self.arbol_avl = ArbolAVL()

    def crear_proyecto(self, id, empresa_id, nombre, descripcion, fecha_inicio, fecha_vencimiento, estado, gerente, equipo):
        nuevo_proyecto = Proyecto(id, nombre, descripcion, fecha_inicio, fecha_vencimiento, estado, empresa_id, gerente, equipo)
        empresa = self.gestion_empresas.buscar_empresa(empresa_id)
        if empresa:
            empresa.proyectos.append(nuevo_proyecto)
            self.arbol_avl.raiz = self.arbol_avl.insertar(self.arbol_avl.raiz, nuevo_proyecto)

    def modificar_proyecto(self, id, nombre=None, descripcion=None, fecha_inicio=None, fecha_vencimiento=None, estado=None, gerente=None, equipo=None):
        proyecto = self.buscar_proyecto_por_id(id)
        if proyecto:
            if nombre:
                proyecto.nombre = nombre
            if descripcion:
                proyecto.descripcion = descripcion
            if fecha_inicio:
                proyecto.fecha_inicio = fecha_inicio
            if fecha_vencimiento:
                proyecto.fecha_vencimiento = fecha_vencimiento
            if estado:
                proyecto.estado = estado
            if gerente:
                proyecto.gerente = gerente
            if equipo:
                proyecto.equipo = equipo
            self.arbol_avl.actualizar_arbol(self.arbol_avl.raiz)
            return True
        return False

    def buscar_proyecto(self, criterio, valor):
        return self.arbol_avl.buscar(self.arbol_avl.raiz, criterio, valor)

    def buscar_proyecto_por_id(self, id):
        return self.buscar_proyecto('id', id)

    def eliminar_proyecto(self, id):
        proyecto = self.buscar_proyecto_por_id(id)
        if proyecto:
            self.arbol_avl.raiz = self.arbol_avl.eliminar(self.arbol_avl.raiz, proyecto)
            empresa = self.gestion_empresas.buscar_empresa(proyecto.empresa)
            if empresa:
                empresa.proyectos.remove(proyecto)
            return True
        return False

    def listar_proyectos(self):
        self.arbol_avl.preorden(self.arbol_avl.raiz)
        
    def identificar_tareas_criticas(self):
        tareas_criticas = []
        self.postorden_tareas_criticas(self.arbol_avl.raiz, tareas_criticas)
        for tarea in tareas_criticas:
            print(tarea)

    def postorden_tareas_criticas(self, nodo, tareas_criticas):
        if not nodo:
            return
        self.postorden_tareas_criticas(nodo.izquierda, tareas_criticas)
        self.postorden_tareas_criticas(nodo.derecha, tareas_criticas)
        if nodo.proyecto.estado == 'critico':  # Ejemplo de criterio para identificar tareas críticas
            tareas_criticas.append(nodo.proyecto)

    def listar_sprites_nivel(self, id_proyecto, nivel):
        proyecto = self.buscar_proyecto_por_id(id_proyecto)
        if proyecto:
            self.listar_tareas_nivel(proyecto.tareas, nivel)

    def listar_tareas_nivel(self, tareas, nivel, actual=0):
        if actual == nivel:
            for tarea in tareas:
                print(tarea)
        else:
            for tarea in tareas:
                self.listar_tareas_nivel(tarea.subtareas, nivel, actual + 1)

    def listar_tareas_empleado(self, cedula):
        for empresa in self.gestion_empresas.empresas:
            for proyecto in empresa.proyectos:
                horas_total = 0
                tareas_empleado = []
                self.postorden_tareas_empleado(proyecto.tareas, cedula, tareas_empleado, horas_total)
                if tareas_empleado:
                    print(f"Proyecto {proyecto.id} - {horas_total} horas")
                    for tarea in tareas_empleado:
                        print(f"- {tarea.nombre} {tarea.duracion_horas} horas")

    def postorden_tareas_empleado(self, tareas, cedula, tareas_empleado, horas_total):
        for tarea in tareas:
            self.postorden_tareas_empleado(tarea.subtareas, cedula, tareas_empleado, horas_total)
            if tarea.responsable == cedula:
                tareas_empleado.append(tarea)
                horas_total += tarea.duracion_horas

    def exportar_tareas_completadas(self, id_proyecto, duracion_max):
        proyecto = self.buscar_proyecto_por_id(id_proyecto)
        if proyecto:
            tareas_completadas = []
            self.postorden_exportar_tareas(proyecto.tareas, duracion_max, tareas_completadas)
            with open('tareas_completadas.csv', 'w', newline='') as csvfile:
                fieldnames = ['id', 'nombre', 'descripcion', 'duracion_horas', 'costo', 'responsable']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for tarea in tareas_completadas:
                    writer.writerow({'id': tarea.id, 'nombre': tarea.nombre, 'descripcion': tarea.descripcion, 'duracion_horas': tarea.duracion_horas, 'costo': tarea.costo, 'responsable': tarea.responsable})

    def postorden_exportar_tareas(self, tareas, duracion_max, tareas_completadas):
        for tarea in tareas:
            self.postorden_exportar_tareas(tarea.subtareas, duracion_max, tareas_completadas)
            if tarea.duracion_horas <= duracion_max:
                tareas_completadas.append(tarea)

    def buscar_proyecto_por_id(self, id):
        for empresa in self.gestion_empresas.empresas:
            for proyecto in empresa.proyectos:
                if proyecto.id == id:
                    return proyecto
        return None
    
    

# Ejemplo de uso
gestion_proyectos = GestionProyectos(gestion_empresas)
gestion_proyectos.crear_proyecto('1', '1', 'Proyecto A', 'Descripción A', '2023-01-01', '2023-12-31', 'En progreso', 'Gerente A', 'Equipo A')
gestion_proyectos.crear_proyecto('2', '2', 'Proyecto B', 'Descripción B', '2023-02-01', '2023-11-30', 'En progreso', 'Gerente B', 'Equipo B')
gestion_proyectos.listar_proyectos()

#3.- Modulo de Gestión de Tareas y Prioridades--------------------------------------------------------------------------------------------------------------------------------------
class Tarea:
    def __init__(self, id, nombre, descripcion, fecha_inicio, fecha_vencimiento, estado, encargado):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha_inicio = fecha_inicio
        self.fecha_vencimiento = fecha_vencimiento
        self.estado = estado
        self.encargado = encargado
        self.subtareas = []  # Inicializamos la lista de subtareas

    def agregar_subtarea(self, subtarea):
        self.subtareas.append(subtarea)
        
    def eliminar_subtarea(self, subtarea_id):
        self.subtareas = [sub for sub in self.subtareas if sub.id != subtarea_id]


    def __str__(self):
        return f"ID: {self.id}, Nombre: {self.nombre}, Descripción: {self.descripcion}, Fecha de Inicio: {self.fecha_inicio}, Fecha de Vencimiento: {self.fecha_vencimiento}, Estado: {self.estado}, Encargado: {self.encargado}"

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "fecha_inicio": self.fecha_inicio,
            "fecha_vencimiento": self.fecha_vencimiento,
            "estado": self.estado,
            "encargado": self.encargado,
            "subtareas": [subtarea.to_dict() for subtarea in self.subtareas]
        }

class GestionTareas:
    def __init__(self, archivo_datos):
        self.archivo_datos = archivo_datos
        self.proyectos = []
        self.tareas = []
        self.cargar_datos()

    def cargar_datos(self):
        try:
            with open(self.archivo_datos, 'r') as archivo:
                datos = json.load(archivo)
                self.proyectos = [item for item in datos if 'tareas' in item]
                self.tareas = [self._dict_a_tarea(item) for item in datos if 'tareas' not in item]
        except FileNotFoundError:
            self.proyectos = []
            self.tareas = []

    def guardar_datos(self):
        datos = [proyecto for proyecto in self.proyectos]
        datos.extend([tarea.to_dict() for tarea in self.tareas])
        with open(self.archivo_datos, 'w') as archivo:
            json.dump(datos, archivo, indent=4)

    def _dict_a_tarea(self, datos):
        tarea = Tarea(
            datos["id"],
            datos["nombre"],
            datos["empresa"],
            datos["descripcion"],
            datos["fecha_inicio"],
            datos["fecha_vencimiento"],
            datos["estado"],
            datos.get("responsable", None)  # Asegura que se maneje correctamente si no existe
        )
        if "subtareas" in datos:
            for subtarea in datos["subtareas"]:
                tarea.agregar_subtarea(self._dict_a_tarea(subtarea))
        return tarea

    def agregar_tarea(self, tarea, id_proyecto=None):
        if id_proyecto:
            for proyecto in self.proyectos:
                if proyecto['id'] == id_proyecto:
                    proyecto['tareas'].append(tarea.to_dict())
                    break
        else:
            self.tareas.append(tarea)
        self.guardar_datos()
    
    def listar_tareas(self, id_proyecto):
        for proyecto in self.proyectos:
            if proyecto['id'] == id_proyecto:
                return proyecto['tareas']
        return []
    
    def buscar_tarea(self, id_proyecto, id_tarea):
        for proyecto in self.proyectos:
            if proyecto['id'] == id_proyecto:
                for tarea in proyecto['tareas']:
                    if tarea['id'] == id_tarea:
                        return tarea
        return None

    def modificar_tarea(self, id, nombre=None, empresa=None, descripcion=None, fecha_inicio=None, fecha_vencimiento=None, estado=None, porcentaje=None):
        tarea = self.buscar_tarea_por_id(id)
        if tarea:
            if nombre:
                tarea.nombre = nombre
            if empresa:
                tarea.empresa = empresa
            if descripcion:
                tarea.descripcion = descripcion
            if fecha_inicio:
                tarea.fecha_inicio = fecha_inicio
            if fecha_vencimiento:
                tarea.fecha_vencimiento = fecha_vencimiento
            if estado:
                tarea.estado = estado
            if porcentaje is not None:
                tarea.porcentaje = porcentaje
            self.guardar_datos()
            return True
        return False

    def eliminar_tarea(self, id):
        tarea, parent = self.buscar_tarea_con_padre(id)
        if tarea:
            if parent:
                parent.subtareas.remove(tarea)
            else:
                self.proyectos.remove(tarea)
            self.guardar_datos()
            return True
        return False

    def buscar_tarea_por_id(self, id, nodo=None):
        if nodo is None:
            nodo = self.proyectos
        for tarea in nodo:
            if tarea.id == id:
                return tarea
            subtarea = self.buscar_tarea_por_id(id, tarea.subtareas)
            if subtarea:
                return subtarea
        return None

    def buscar_tarea_con_padre(self, id, nodo=None, parent=None):
        if nodo is None:
            nodo = self.proyectos
        for tarea in nodo:
            if tarea.id == id:
                return tarea, parent
            subtarea, padre = self.buscar_tarea_con_padre(id, tarea.subtareas, tarea)
            if subtarea:
                return subtarea, padre
        return None, None

    def listar_tareas(self):
        for proyecto in self.proyectos:
            print(f"Proyecto: {proyecto['nombre']}")
            for tarea in proyecto['tareas']:
                print(f"  {tarea['nombre']}")
        print("Tareas individuales:")
        for tarea in self.tareas:
            print(f"  {tarea.nombre}")

    def listar_tareas_nivel(self, nivel):
        self._listar_nivel(self.proyectos, nivel, 0)

    def _listar_nivel(self, tareas, nivel, actual):
        if actual == nivel:
            for tarea in tareas:
                print(tarea)
        else:
            for tarea in tareas:
                if isinstance(tarea, dict) and 'subtareas' in tarea:
                    self._listar_nivel(tarea['subtareas'], nivel, actual + 1)
                elif isinstance(tarea, Tarea):
                    self._listar_nivel(tarea.subtareas, nivel, actual + 1)
                
    def buscar_proyecto_por_id(self, id_proyecto):
        for proyecto in self.proyectos:
            if proyecto['id'] == id_proyecto:
                return proyecto
        return None

# Ejemplo de uso
gestion_tareas = GestionTareas('Parcial V Estructuras Arboles\\datos_tareas.json')
gestion_empresas = GestionEmpresas('empresas.csv')
gestion_empresas.crear_empresa('1', 'Empresa A', 'Descripción A', '2023-01-01', 'Direccion A', '123456789', 'correoA@empresa.com', 'Gerente A', 'Equipo A')
gestion_empresas.crear_empresa('2', 'Empresa B', 'Descripción B', '2023-02-01', 'Direccion B', '987654321', 'correoB@empresa.com', 'Gerente B', 'Equipo B')
gestion_empresas.listar_empresas()
# Crear una tarea principal
tarea_principal = Tarea('1', 'Tarea Principal', 'Descripción Tarea Principal', '2023-01-01', '2023-12-31', 'En progreso', 'Juan Pérez')

# Crear una subtarea
subtarea1 = Tarea('1.1', 'Subtarea 1', 'Descripción Subtarea 1', '2023-01-15', '2023-06-30', 'En progreso', 'María López')

# Agregar la subtarea a la tarea principal
tarea_principal.agregar_subtarea(subtarea1)

print(tarea_principal)
for subtarea in tarea_principal.subtareas:
    print(subtarea)
gestion_tareas.agregar_tarea(tarea_principal, id_proyecto='1') 
gestion_tareas.listar_tareas()
gestion_tareas.listar_tareas_nivel(1)
#4.- Modulo de Gestión de Sprint----------------------------------------------------------------------------------------------------------------------------------------------------
class NodoAVL:
    def __init__(self, sprint):
        self.sprint = sprint
        self.izquierda = None
        self.derecha = None
        self.altura = 1

class Sprint:
    def __init__(self, id, nombre, fecha_inicio, fecha_fin, estado, objetivos, equipo):
        self.id = id
        self.nombre = nombre
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.estado = estado
        self.objetivos = objetivos
        self.equipo = equipo
        self.tareas = []

    def agregar_tarea(self, tarea):
        self.tareas.append(tarea)

    def __str__(self):
        ret = f"ID: {self.id}, Nombre: {self.nombre}, Estado: {self.estado}, Objetivos: {self.objetivos}\n"
        ret += "Tareas:\n"
        for tarea in self.tareas:
            ret += f"\t{tarea}\n"
        return ret

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "fecha_inicio": self.fecha_inicio,
            "fecha_fin": self.fecha_fin,
            "estado": self.estado,
            "objetivos": self.objetivos,
            "equipo": self.equipo,
            "tareas": [tarea.to_dict() for tarea in self.tareas]
        }

class ArbolAVL:
    def __init__(self):
        self.raiz = None

    def insertar(self, sprint):
        if not self.raiz:
            self.raiz = NodoAVL(sprint)
        else:
            self.raiz = self._insertar(self.raiz, sprint)

    def _insertar(self, nodo, sprint):
        if not nodo:
            return NodoAVL(sprint)
        elif sprint.fecha_fin < nodo.sprint.fecha_fin:
            nodo.izquierda = self._insertar(nodo.izquierda, sprint)
        else:
            nodo.derecha = self._insertar(nodo.derecha, sprint)

        nodo.altura = 1 + max(self._obtener_altura(nodo.izquierda), self._obtener_altura(nodo.derecha))

        balance = self._obtener_balance(nodo)
        if balance > 1:
            if sprint.fecha_fin < nodo.izquierda.sprint.fecha_fin:
                return self._rotacion_derecha(nodo)
            else:
                nodo.izquierda = self._rotacion_izquierda(nodo.izquierda)
                return self._rotacion_derecha(nodo)
        if balance < -1:
            if sprint.fecha_fin > nodo.derecha.sprint.fecha_fin:
                return self._rotacion_izquierda(nodo)
            else:
                nodo.derecha = self._rotacion_derecha(nodo.derecha)
                return self._rotacion_izquierda(nodo)

        return nodo

    def _obtener_altura(self, nodo):
        if not nodo:
            return 0
        return nodo.altura

    def _obtener_balance(self, nodo):
        if not nodo:
            return 0
        return self._obtener_altura(nodo.izquierda) - self._obtener_altura(nodo.derecha)

    def _rotacion_izquierda(self, z):
        y = z.derecha
        T2 = y.izquierda
        y.izquierda = z
        z.derecha = T2
        z.altura = 1 + max(self._obtener_altura(z.izquierda), self._obtener_altura(z.derecha))
        y.altura = 1 + max(self._obtener_altura(y.izquierda), self._obtener_altura(y.derecha))
        return y

    def _rotacion_derecha(self, y):
        x = y.izquierda
        T2 = x.derecha
        x.derecha = y
        y.izquierda = T2
        y.altura = 1 + max(self._obtener_altura(y.izquierda), self._obtener_altura(y.derecha))
        x.altura = 1 + max(self._obtener_altura(x.izquierda), self._obtener_altura(x.derecha))
        return x

    def eliminar(self, fecha_fin):
        if self.raiz:
            self.raiz = self._eliminar(self.raiz, fecha_fin)

    def _eliminar(self, nodo, fecha_fin):
        if not nodo:
            return nodo
        elif fecha_fin < nodo.sprint.fecha_fin:
            nodo.izquierda = self._eliminar(nodo.izquierda, fecha_fin)
        elif fecha_fin > nodo.sprint.fecha_fin:
            nodo.derecha = self._eliminar(nodo.derecha, fecha_fin)
        else:
            if not nodo.izquierda:
                return nodo.derecha
            elif not nodo.derecha:
                return nodo.izquierda
            temp = self._obtener_nodo_minimo(nodo.derecha)
            nodo.sprint = temp.sprint
            nodo.derecha = self._eliminar(nodo.derecha, temp.sprint.fecha_fin)

        if not nodo:
            return nodo

        nodo.altura = 1 + max(self._obtener_altura(nodo.izquierda), self._obtener_altura(nodo.derecha))
        balance = self._obtener_balance(nodo)
        if balance > 1:
            if self._obtener_balance(nodo.izquierda) >= 0:
                return self._rotacion_derecha(nodo)
            else:
                nodo.izquierda = self._rotacion_izquierda(nodo.izquierda)
                return self._rotacion_derecha(nodo)
        if balance < -1:
            if self._obtener_balance(nodo.derecha) <= 0:
                return self._rotacion_izquierda(nodo)
            else:
                nodo.derecha = self._rotacion_derecha(nodo.derecha)
                return self._rotacion_izquierda(nodo)

        return nodo

    def _obtener_nodo_minimo(self, nodo):
        if nodo is None or nodo.izquierda is None:
            return nodo
        return self._obtener_nodo_minimo(nodo.izquierda)

    def listar_sprints(self):
        self._listar_sprints(self.raiz)

    def _listar_sprints(self, nodo):
        if nodo:
            self._listar_sprints(nodo.izquierda)
            print(nodo.sprint)
            self._listar_sprints(nodo.derecha)

class GestionSprints:
    def __init__(self, archivo_datos):
        self.archivo_datos = archivo_datos
        self.arbol_avl = ArbolAVL()
        self.cargar_datos()

    def cargar_datos(self):
        try:
            with open(self.archivo_datos, 'r') as archivo:
                datos = json.load(archivo)
                for sprint_data in datos:
                    sprint = self._dict_a_sprint(sprint_data)
                    self.arbol_avl.insertar(sprint)
        except FileNotFoundError:
            pass

    def guardar_datos(self):
        sprints = []
        self._guardar_datos(self.arbol_avl.raiz, sprints)
        with open(self.archivo_datos, 'w') as archivo:
            json.dump(sprints, archivo, indent=4)

    def _guardar_datos(self, nodo, sprints):
        if nodo:
            sprints.append(nodo.sprint.to_dict())
            self._guardar_datos(nodo.izquierda, sprints)
            self._guardar_datos(nodo.derecha, sprints)

    def _dict_a_sprint(self, datos):
        sprint = Sprint(
            datos["id"],
            datos["nombre"],
            datos["fecha_inicio"],
            datos["fecha_fin"],
            datos["estado"],
            datos["objetivos"],
            datos["equipo"]
        )
        for tarea_data in datos["tareas"]:
            tarea = self._dict_a_tarea(tarea_data)
            sprint.agregar_tarea(tarea)
        return sprint

    def _dict_a_tarea(self, datos):
        tarea = Tarea(
            datos["id"],
            datos["nombre"],
            datos["empresa"],
            datos["descripcion"],
            datos["fecha_inicio"],
            datos["fecha_vencimiento"],
            datos["estado"],
            datos["porcentaje"]
        )
        for subtarea_data in datos["subtareas"]:
            subtarea = self._dict_a_tarea(subtarea_data)
            tarea.agregar_subtarea(subtarea)
        return tarea

    def agregar_sprint(self, sprint):
        self.arbol_avl.insertar(sprint)
        self.guardar_datos()

    def modificar_sprint(self, id, nombre=None, fecha_inicio=None, fecha_fin=None, estado=None, objetivos=None, equipo=None):
        sprint = self.buscar_sprint_por_id(id)
        if sprint:
            if nombre:
                sprint.nombre = nombre
            if fecha_inicio:
                sprint.fecha_inicio = fecha_inicio
            if fecha_fin:
                sprint.fecha_fin = fecha_fin
            if estado:
                sprint.estado = estado
            if objetivos:
                sprint.objetivos = objetivos
            if equipo:
                sprint.equipo = equipo
            self.guardar_datos()
            return True
        return False

    def eliminar_sprint(self, id):
        sprint = self.buscar_sprint_por_id(id)
        if sprint:
            self.arbol_avl.eliminar(sprint.fecha_fin)
            self.guardar_datos()
            return True
        return False

    def buscar_sprint_por_id(self, id, nodo=None):
        if nodo is None:
            nodo = self.arbol_avl.raiz
        if nodo is None:
            return None
        if nodo.sprint.id == id:
            return nodo.sprint
        elif id < nodo.sprint.id:
            return self.buscar_sprint_por_id(id, nodo.izquierda)
        else:
            return self.buscar_sprint_por_id(id, nodo.derecha)

    def listar_sprints(self):
        self.arbol_avl.listar_sprints()

# Ejemplo de uso
gestion_sprints = GestionSprints('datos_sprints.json')
sprint1 = Sprint('1', 'Sprint 1', '2023-01-01', '2023-01-14', 'En progreso', 'Objetivo del Sprint 1', 'Equipo 1')
tarea1 = Tarea('1', 'Tarea 1', 'Descripción de la tarea 1', '2023-01-01', '2023-01-10', 'En progreso', 'Messi')
tarea2 = Tarea('2', 'Tarea 2', 'Descripción de la tarea 2', '2023-01-02', '2023-01-12', 'No iniciada', 'Ronaldo')
sprint1.agregar_tarea(tarea1)
sprint1.agregar_tarea(tarea2)
gestion_sprints.agregar_sprint(sprint1)
gestion_sprints.listar_sprints()

#5.- Modulo de Reportes-------------------------------------------------------------------------------------------------------------------------------------------------------------
class GestionReportes:
    def __init__(self, gestion_proyectos, gestion_tareas, gestion_sprints):
        self.gestion_proyectos = gestion_proyectos
        self.gestion_tareas = gestion_tareas
        self.gestion_sprints = gestion_sprints

def mostrar_menu():
    print("Seleccione una opción:")
    print("1. Identificar y mostrar tareas críticas")
    print("2. Listar sprites de un proyecto en un nivel específico")
    print("3. Listar tareas asignadas a un empleado")
    print("4. Exportar tareas completadas a CSV")
    print("0. Salir")

gestion_empresas = GestionEmpresas('empresas.csv')
gestion_proyectos = GestionProyectos(gestion_empresas)

while True:
    mostrar_menu()
    opcion = input("Opción: ")
    if opcion == '1':
        gestion_proyectos.identificar_tareas_criticas()
    elif opcion == '2':
        id_proyecto = input("Ingrese el ID del proyecto: ")
        nivel = int(input("Ingrese el nivel del árbol: "))
        gestion_proyectos.listar_sprites_nivel(id_proyecto, nivel)
    elif opcion == '3':
        cedula = input("Ingrese la cédula del empleado: ")
        gestion_proyectos.listar_tareas_empleado(cedula)
    elif opcion == '4':
        id_proyecto = input("Ingrese el ID del proyecto: ")
        duracion_max = int(input("Ingrese la duración máxima en horas: "))
        gestion_proyectos.exportar_tareas_completadas(id_proyecto, duracion_max)
    elif opcion == '0':
        break
    else:
        print("Opción no válida. Intente de nuevo.")
                    
                    

# Ejemplo de uso
gestion_reportes = GestionReportes(gestion_proyectos, gestion_tareas, gestion_sprints)


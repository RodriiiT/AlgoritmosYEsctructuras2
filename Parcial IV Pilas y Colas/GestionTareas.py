"""
Parcial IV. TDA. Listas Enlazadas, Pilas y Colas

Elaborado por:

- Cristian Guevara. C.I: 31.567.525
- Rodrigo Torres. C.I: 31.014.592
"""

#1.- Módulo de Gestión de Proyectos
import json
from datetime import datetime
from datetime import timedelta
from collections import deque

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
        self.tareas = []
        
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
        self.siguiente = None

    def agregar_subtarea(self, subtarea):
        self.subtareas.append(subtarea)

class Subtarea:
    def __init__(self, id_s, nombre_s, descripcion_s, estado_s):
        self.id_s = id_s
        self.nombre_s = nombre_s
        self.descripcion_s = descripcion_s
        self.estado_s = estado_s
        


#2.- Módulo de Gestión de Tareas y Prioridades
class ListaEnlazadaTareas:
    def __init__(self):
        self.cabeza = None

    def agregar_tarea(self, id_t, nombre_t, empresa_cliente, descripcion_t, fecha_inicio_t, fecha_vencimiento_t, estado_t, porcentaje):
        nuevo_nodo = Tarea(id_t, nombre_t, empresa_cliente, descripcion_t, fecha_inicio_t, fecha_vencimiento_t, estado_t, porcentaje)
        if not self.cabeza:
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo

    def insertar_al_principio(self, id_t, nombre_t, empresa_cliente, descripcion_t, fecha_inicio_t, fecha_vencimiento_t, estado_t, porcentaje):
        nuevo_nodo = Tarea(id_t, nombre_t, empresa_cliente, descripcion_t, fecha_inicio_t, fecha_vencimiento_t, estado_t, porcentaje)
        nuevo_nodo.siguiente = self.cabeza
        self.cabeza = nuevo_nodo
    
    def mostrar_tareas(self):
        actual = self.cabeza
        while actual:
            print("Nombre:", actual.nombre_t)
            print()
            actual = actual.siguiente

    def buscar_tarea(self, nombre):
        actual = self.cabeza
        while actual:
            if actual.nombre_t == nombre:
                return True
            actual = actual.siguiente
        return False

    def eliminar_tarea(self, nombre):
        if not self.cabeza:
            return
        if self.cabeza.nombre_t == nombre:
            self.cabeza = self.cabeza.siguiente
            return
        anterior = None
        actual = self.cabeza
        while actual and actual.nombre_t != nombre:
            anterior = actual
            actual = actual.siguiente
        if actual:
            anterior.siguiente = actual.siguiente

    def modificar_tarea(self, nombre_antiguo, id_t, nuevo_nombre, empresa_cliente, descripcion_t, fecha_inicio_t, fecha_vencimiento_t, estado_t, porcentaje):
        actual = self.cabeza
        while actual:
            if actual.nombre_t == nombre_antiguo:
                actual.id_t = id_t
                actual.nombre_t = nuevo_nombre
                actual.empresa_cliente = empresa_cliente
                actual.descripcion_t = descripcion_t
                actual.fecha_inicio_t = fecha_inicio_t
                actual.fecha_vencimiento_t = fecha_vencimiento_t
                actual.estado_t = estado_t
                actual.porcentaje = porcentaje
                return True
            actual = actual.siguiente
        return False

    def obtener_posicion(self, nombre):
        actual = self.cabeza
        pos = 0
        while actual:
            if actual.nombre_t == nombre:
                return pos
            actual = actual.siguiente
            pos += 1
        return -1
    
class PilaTareasPrioritarias:
    def __init__(self):
        self.cabeza = None

    def agregar_tprioritaria(self, nombre_antiguo, id_t, nuevo_nombre, empresa_cliente, descripcion_t, fecha_inicio_t, fecha_vencimiento_t, estado_t, porcentaje):
        nuevo_nodo = Tarea(nombre_antiguo, id_t, nuevo_nombre, empresa_cliente, descripcion_t, fecha_inicio_t, fecha_vencimiento_t, estado_t, porcentaje)
        if not self.cabeza:
            self.cabeza = nuevo_nodo
        else:
            nuevo_nodo.siguiente = self.cabeza
            self.cabeza = nuevo_nodo

    def mostrar_tprioritaria(self):
        actual = self.cabeza    
        print("Nombre:", actual.nombre_t)
    

    def buscar_tarea(self, nombre):
        actual = self.cabeza
        while actual:
            if actual.nombre_t == nombre:
                return True
            actual = actual.siguiente
        return False

    def eliminar_tprioritaria(self):
        if not self.cabeza:
            return None
        eliminado = self.cabeza
        self.cabeza = self.cabeza.siguiente
        return eliminado
    
    def mostrar_tp(self):
        actual = self.cabeza
        while actual:
            print("Nombre:", actual.nombre_t)
            diferencia = actual.fecha_vencimiento_t - actual.fecha_inicio_t
            print(f"Diferencia: {diferencia}")
            dias = diferencia.days
            segundos_totales = diferencia.seconds
            horas = segundos_totales // 3600
            minutos = (segundos_totales % 3600) // 60
            segundos = (segundos_totales % 3600) % 60
            print(f"Tiempo total: {dias} días, {horas} horas, {minutos} minutos y {segundos} segundos")
            print()
            actual = actual.siguiente

class ColaTareasVencimiento:
    def __init__(self):
        self.cola = deque()
        
    def agregar_tarea(self, tarea):
        self.cola.append(tarea)
        
    def eliminar_tarea(self):
        if self.cola:
            return self.cola.popleft()
        else:
            return None
        
    def consultar_proxima_tarea(self):
        if self.cola:
            return self.cola[0]
        else:
            return None
        
    def tiempo_total_tareas(self):
        total = timedelta()
        for tarea in self.cola:
            total += tarea.fecha_vencimiento_t - datetime.now()
        return total

#3.- Módulo de Reportes
class Reportes:
    
    def consultar_tareas_por_estado(proyectos, estado):
        tareas = []
        for proyecto in proyectos:
            for tarea in proyecto.tareas:
                if tarea.estado_t == estado:
                    tareas.append(tarea)
        return tareas

    def filtrar_tareas_por_fecha(proyectos, fecha_inicio=None, fecha_vencimiento=None):
        tareas = []
        for proyecto in proyectos:
            for tarea in proyecto.tareas:
                if ((fecha_inicio is None or tarea.fecha_inicio_t >= fecha_inicio) and 
                    (fecha_vencimiento is None or tarea.fecha_vencimiento_t <= fecha_vencimiento)):
                    tareas.append(tarea)
        return tareas

    def filtrar_proyectos(proyectos, fecha_inicio=None, fecha_vencimiento=None, estado=None, empresa=None):
        proyectos_filtrados = []
        for proyecto in proyectos:
            if ((fecha_inicio is None or proyecto.fecha_inicio >= fecha_inicio) and 
                (fecha_vencimiento is None or proyecto.fecha_vencimiento <= fecha_vencimiento) and 
                (estado is None or proyecto.estado_act == estado) and 
                (empresa is None or proyecto.empresa == empresa)):
                proyectos_filtrados.append(proyecto)
        return proyectos_filtrados

    def listar_subtareas(proyectos, proyecto_id=None, proyecto_nombre=None):
        resultado = []
        for proyecto in proyectos:
            if proyecto_id is not None and proyecto.ide != proyecto_id:
                continue
            if proyecto_nombre is not None and proyecto.nombre != proyecto_nombre:
                continue
            for tarea in proyecto.tareas:
                subtareas_info = [{"id": subtarea.id_s, "nombre": subtarea.nombre_s, "descripcion": subtarea.descripcion_s, "estado": subtarea.estado_s} for subtarea in tarea.subtareas]
                resultado.append({"tarea_id": tarea.id_t, "tarea_nombre": tarea.nombre_t, "subtareas": subtareas_info})
        return resultado


#4.- Módulo de importación y exportación de datos


class Carga:
    def __init__(self, nombre_archivo):
        self.nombre_archivo = nombre_archivo

    def cargar_datos_desde_json(self):
        proyectos = []
        try:
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
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo '{self.nombre_archivo}'.")
        except json.JSONDecodeError:
            print("Error: No se pudo decodificar el archivo JSON.")
        except Exception as e:
            print(f"Error: {e}")
        return proyectos
    
def menu():
    proyectos = []
    lista_tareas = ListaEnlazadaTareas()
    pila_tareas = PilaTareasPrioritarias()
    cola_tareas = ColaTareasVencimiento()
    
    #Lee los proyectos desde el archivo JSON
    prueba = Carga("C:\\Users\\USUARIO\\Desktop\\AlgoritmosYEstructuras2\\Parcial IV Pilas y Colas\\datos_prueba.json")
    proyectos = prueba.cargar_datos_desde_json()

    for proyecto in proyectos:
        for tarea in proyecto.tareas:
            lista_tareas.agregar_tarea(
                tarea.id_t, tarea.nombre_t, tarea.empresa_cliente, tarea.descripcion_t,
                tarea.fecha_inicio_t, tarea.fecha_vencimiento_t, tarea.estado_t, tarea.porcentaje
            )
            
    #Imprimir proyectos cargados
    print("Proyectos cargados desde el archivo JSON:")
    for proyecto in proyectos:
        print(f"ID: {proyecto.ide}, Nombre: {proyecto.nombre}, Estado: {proyecto.estado_act}")

    cent = input("¿Desea continuar? (s/n): ")
    while cent.lower() == 's':
        print("\n****Gestión de Proyectos y Tareas****")
        print("\nMenú de opciones:")
        print("1.- Crear un proyecto")
        print("2.- Modificar proyecto")
        print("3.- Consultar proyecto")
        print("4.- Eliminar proyecto")
        print("5.- Listar proyectos")
        print("6.- Crear tarea")
        print("7.- Mostrar tareas")
        print("8.- Agregar tarea a pila de prioridades")
        print("9.- Mostrar tareas prioritarias")
        print("10.- Agregar tarea a cola de vencimiento")
        print("11.- Mostrar tareas por vencimiento")
        print("12.- Salir")

        opcion = input("\nSeleccione una opción: ")

        if opcion == '1':
            print("\nOpción 1 seleccionada (Crear un proyecto)")
            id_opc = input("Ingrese el id del proyecto: ")
            nombre_opc = input("Ingrese el nombre del proyecto: ")
            descripcion_opc = input("Ingrese la descripción del proyecto: ")
            fecha_inicio_opc = datetime.strptime(input("Ingrese la fecha de inicio del proyecto (YYYY-MM-DD): "), "%Y-%m-%d")
            fecha_vencimiento_opc = datetime.strptime(input("Ingrese la fecha de vencimiento del proyecto (YYYY-MM-DD): "), "%Y-%m-%d")
            estado_act_opc = input("Ingrese el estado actual del proyecto: ")
            empresa_opc = input("Ingrese la empresa del proyecto: ")
            gerente_opc = input("Ingrese el gerente del proyecto: ")
            equipo_opc = input("Ingrese el equipo del proyecto: ")
            proyecto = Proyecto(id_opc, nombre_opc, descripcion_opc, fecha_inicio_opc, fecha_vencimiento_opc, estado_act_opc, empresa_opc, gerente_opc, equipo_opc)
            proyectos.append(proyecto)
            print("\nProyecto creado y añadido a la lista.")

        elif opcion == '2':
            print("\nOpción 2 seleccionada (Modificar proyecto)")
            buscar_id = input("Introduzca el id del proyecto a modificar: ")
            for proyecto in proyectos:
                if proyecto.ide == buscar_id:
                    proyecto.nombre = input("Nuevo nombre: ")
                    proyecto.descripcion = input("Nueva descripción: ")
                    proyecto.fecha_inicio = datetime.strptime(input("Nueva fecha de inicio (YYYY-MM-DD): "), "%Y-%m-%d")
                    proyecto.fecha_vencimiento = datetime.strptime(input("Nueva fecha de vencimiento (YYYY-MM-DD): "), "%Y-%m-%d")
                    proyecto.estado_act = input("Nuevo estado: ")
                    proyecto.empresa = input("Nueva empresa: ")
                    proyecto.gerente = input("Nuevo gerente: ")
                    proyecto.equipo = input("Nuevo equipo: ")
                    print("\nProyecto modificado.")
                    break
            else:
                print("\nProyecto no encontrado.")

        elif opcion == '3':
            print("\nOpción 3 seleccionada (Consultar proyecto)")
            buscar_id = input("Introduzca el id del proyecto a consultar: ")
            for proyecto in proyectos:
                if proyecto.ide == buscar_id:
                    print(f"Nombre: {proyecto.nombre}")
                    print(f"Descripción: {proyecto.descripcion}")
                    print(f"Fecha de inicio: {proyecto.fecha_inicio}")
                    print(f"Fecha de vencimiento: {proyecto.fecha_vencimiento}")
                    print(f"Estado: {proyecto.estado_act}")
                    print(f"Empresa: {proyecto.empresa}")
                    print(f"Gerente: {proyecto.gerente}")
                    print(f"Equipo: {proyecto.equipo}")
                    break
            else:
                print("\nProyecto no encontrado.")

        elif opcion == '4':
            print("\nOpción 4 seleccionada (Eliminar proyecto)")
            buscar_id = input("Introduzca el id del proyecto a eliminar: ")
            for i, proyecto in enumerate(proyectos):
                if proyecto.ide == buscar_id:
                    proyectos.pop(i)
                    print("\nProyecto eliminado.")
                    break
            else:
                print("\nProyecto no encontrado.")

        elif opcion == '5':
            print("\nOpción 5 seleccionada (Listar proyectos)")
            for proyecto in proyectos:
                print(f"ID: {proyecto.ide}, Nombre: {proyecto.nombre}, Estado: {proyecto.estado_act}")

        elif opcion == '6':
            print("\nOpción 6 seleccionada (Crear tarea)")
            id_t = input("Ingrese el id de la tarea: ")
            nombre_t = input("Ingrese el nombre de la tarea: ")
            empresa_cliente = input("Ingrese la empresa cliente: ")
            descripcion_t = input("Ingrese la descripción de la tarea: ")
            fecha_inicio_t = datetime.strptime(input("Ingrese la fecha de inicio de la tarea (YYYY-MM-DD): "), "%Y-%m-%d")
            fecha_vencimiento_t = datetime.strptime(input("Ingrese la fecha de vencimiento de la tarea (YYYY-MM-DD): "), "%Y-%m-%d")
            estado_t = input("Ingrese el estado de la tarea: ")
            porcentaje = float(input("Ingrese el porcentaje de la tarea: "))
            lista_tareas.agregar_tarea(id_t, nombre_t, empresa_cliente, descripcion_t, fecha_inicio_t, fecha_vencimiento_t, estado_t, porcentaje)
            print("\nTarea creada y añadida a la lista enlazada.")

        elif opcion == '7':
            print("\nOpción 7 seleccionada (Mostrar tareas)")
            lista_tareas.mostrar_tareas()

        elif opcion == '8':
            print("\nOpción 8 seleccionada (Agregar tarea a pila de prioridades)")
            nombre_antiguo = input("Ingrese el nombre antiguo de la tarea: ")
            id_t = input("Ingrese el id de la tarea: ")
            nuevo_nombre = input("Ingrese el nuevo nombre de la tarea: ")
            empresa_cliente = input("Ingrese la empresa cliente: ")
            descripcion_t = input("Ingrese la descripción de la tarea: ")
            fecha_inicio_t = datetime.strptime(input("Ingrese la fecha de inicio de la tarea (YYYY-MM-DD): "), "%Y-%m-%d")
            fecha_vencimiento_t = datetime.strptime(input("Ingrese la fecha de vencimiento de la tarea (YYYY-MM-DD): "), "%Y-%m-%d")
            estado_t = input("Ingrese el estado de la tarea: ")
            porcentaje = float(input("Ingrese el porcentaje de la tarea: "))
            pila_tareas.agregar_tprioritaria(nombre_antiguo, id_t, nuevo_nombre, empresa_cliente, descripcion_t, fecha_inicio_t, fecha_vencimiento_t, estado_t, porcentaje)
            print("\nTarea añadida a la pila de tareas prioritarias.")

        elif opcion == '9':
            print("\nOpción 9 seleccionada (Mostrar tareas prioritarias)")
            for proyecto in proyectos:
                for tarea in proyecto.tareas:
                    pila_tareas.agregar_tprioritaria(
                        tarea.id_t, tarea.nombre_t, tarea.empresa_cliente, tarea.descripcion_t,
                        tarea.fecha_inicio_t, tarea.fecha_vencimiento_t, tarea.estado_t, tarea.porcentaje
                    )
            pila_tareas.mostrar_tprioritaria()
            pila_tareas.mostrar_tp()

        elif opcion == '10':
            print("\nOpción 10 seleccionada (Agregar tarea a cola de vencimiento)")
            id_t = input("Ingrese el id de la tarea: ")
            nombre_t = input("Ingrese el nombre de la tarea: ")
            empresa_cliente = input("Ingrese la empresa cliente: ")
            descripcion_t = input("Ingrese la descripción de la tarea: ")
            fecha_inicio_t = datetime.strptime(input("Ingrese la fecha de inicio de la tarea (YYYY-MM-DD): "), "%Y-%m-%d")
            fecha_vencimiento_t = datetime.strptime(input("Ingrese la fecha de vencimiento de la tarea (YYYY-MM-DD): "), "%Y-%m-%d")
            estado_t = input("Ingrese el estado de la tarea: ")
            porcentaje = float(input("Ingrese el porcentaje de la tarea: "))
            tarea = Tarea(id_t, nombre_t, empresa_cliente, descripcion_t, fecha_inicio_t, fecha_vencimiento_t, estado_t, porcentaje)
            cola_tareas.agregar_tarea(tarea)
            print("\nTarea añadida a la cola de vencimiento.")

        elif opcion == '11':
            print("\nOpción 11 seleccionada (Mostrar tareas por vencimiento)")
            for tarea in cola_tareas.cola:
                print(f"ID: {tarea.id_t}, Nombre: {tarea.nombre_t}, Vence: {tarea.fecha_vencimiento_t}")
            
        elif opcion == '12':
            cent = input("¿Desea continuar? (s/n): ")

menu()

# Creamos algunos proyectos, tareas y subtareas para realizar pruebas

"""proyecto1 = Proyecto(
    ide=1,
    nombre="Proyecto 1",
    descripcion="Descripción del Proyecto 1",
    fecha_inicio=datetime(2023, 1, 1),
    fecha_vencimiento=datetime(2023, 12, 31),
    estado_act="activo",
    empresa="Empresa 1",
    gerente="Gerente 1",
    equipo=["Equipo 1"]
)

tarea1 = Tarea(
    id_t=1,
    nombre_t="Tarea 1",
    empresa_cliente="Empresa Cliente 1",
    descripcion_t="Descripción de la Tarea 1",
    fecha_inicio_t=datetime(2023, 1, 1),
    fecha_vencimiento_t=datetime(2023, 6, 30),
    estado_t="pendiente",
    porcentaje=50
)

subtarea1 = Subtarea(
    id_s=1,
    nombre_s="Subtarea 1",
    descripcion_s="Descripción de la Subtarea 1",
    estado_s="completada"
)
subtarea2 = Subtarea(
    id_s=1,
    nombre_s="Subtarea 2",
    descripcion_s="Descripción de la Subtarea 2",
    estado_s="completada"
)

# Agregar subtarea a la tarea
tarea1.agregar_subtarea(subtarea1)
tarea1.agregar_subtarea(subtarea2)

# Agregar tarea al proyecto
proyecto1.agregar_tarea(tarea1)

# Crear un segundo proyecto para pruebas
proyecto2 = Proyecto(
    ide=2,
    nombre="Proyecto 2",
    descripcion="Descripción del Proyecto 2",
    fecha_inicio=datetime(2023, 2, 1),
    fecha_vencimiento=datetime(2023, 11, 30),
    estado_act="completado",
    empresa="Empresa 2",
    gerente="Gerente 2",
    equipo=["Equipo 2"]
)

tarea2 = Tarea(
    id_t=2,
    nombre_t="Tarea 2",
    empresa_cliente="Empresa Cliente 2",
    descripcion_t="Descripción de la Tarea 2",
    fecha_inicio_t=datetime(2023, 3, 1),
    fecha_vencimiento_t=datetime(2023, 8, 30),
    estado_t="en progreso",
    porcentaje=75
)

# Agregar tarea al proyecto
proyecto2.agregar_tarea(tarea2)

# Lista de proyectos para pruebas
proyectos = [proyecto1, proyecto2]

# Realizamos pruebas de las funciones de reporte
# 1. Consulta de Tareas por Estado
tareas_pendientes = Reportes.consultar_tareas_por_estado(proyectos, "pendiente")
print("Tareas Pendientes:")
for tarea in tareas_pendientes:
    print(f"- {tarea.nombre_t}: {tarea.descripcion_t}")

# 2. Filtrado por Fecha
tareas_por_fecha = Reportes.filtrar_tareas_por_fecha(proyectos, fecha_inicio=datetime(2023, 1, 1), fecha_vencimiento=datetime(2023, 6, 30))
print("\nTareas entre 2023-01-01 y 2023-06-30:")
for tarea in tareas_por_fecha:
    print(f"- {tarea.nombre_t}: {tarea.descripcion_t}")

# 3. Filtrado de Proyectos
proyectos_filtrados = Reportes.filtrar_proyectos(proyectos, estado="activo")
print("\nProyectos Activos:")
for proyecto in proyectos_filtrados:
    print(f"- {proyecto.nombre}: {proyecto.descripcion}")

# 4. Listar Subtareas
subtareas_listadas = Reportes.listar_subtareas(proyectos, proyecto_id=1)
print("\nSubtareas del Proyecto 1:")
for tarea in subtareas_listadas:
    print(f"Tarea {tarea['tarea_id']} - {tarea['tarea_nombre']}:")
    for subtarea in tarea["subtareas"]:
        print(f"  - {subtarea['nombre']}: {subtarea['descripcion']}")
"""

import csv
from datetime import datetime


#----Modulo 1----------------------------------------------------------------------------------
class Nodo:
    def __init__(self, empresa):
        self.empresa = empresa
        self.siguiente = None

class ListaEnlazada:
    def __init__(self):
        self.cabeza = None

    def agregar(self, empresa):
        nuevo_nodo = Nodo(empresa)
        if not self.cabeza:
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo

    def eliminar(self, id):
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

    def buscar(self, id):
        actual = self.cabeza
        while actual:
            if actual.empresa.id == id:
                return actual.empresa
            actual = actual.siguiente
        return None

    def listar(self):
        empresas = []
        actual = self.cabeza
        while actual:
            empresas.append(actual.empresa)
            actual = actual.siguiente
        return empresas

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

class Proyecto:
    def __init__(self, id, nombre, descripcion, fecha_inicio, fecha_vencimiento, estado_actual, gerente, equipo):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha_inicio = fecha_inicio
        self.fecha_vencimiento = fecha_vencimiento
        self.estado_actual = estado_actual
        self.gerente = gerente
        self.equipo = equipo

    def __str__(self):
        return f"Nombre: {self.nombre}, Descripción: {self.descripcion}"

class GestionEmpresas:
    def __init__(self, archivo_csv):
        self.archivo_csv = archivo_csv
        self.empresas = ListaEnlazada()
        self.cargar_empresas()
        self.gestion_proyectos = GestionProyectos()

    def cargar_empresas(self):
        try:
            with open(self.archivo_csv, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    empresa = Empresa(
                        row['id'],
                        row['nombre'],
                        row['descripcion'],
                        row['fecha_creacion'],
                        row['direccion'],
                        row['telefono'],
                        row['correo'],
                        row['gerente'],
                        row['equipo_contacto']
                    )
                    self.empresas.agregar(empresa)
        except FileNotFoundError:
            print(f"El archivo {self.archivo_csv} no se encontró. Se creará uno nuevo.")

    def guardar_empresas(self):
        with open(self.archivo_csv, 'w', newline='') as csvfile:
            fieldnames = ['id', 'nombre', 'descripcion', 'fecha_creacion', 'direccion', 'telefono', 'correo', 'gerente', 'equipo_contacto']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for empresa in self.empresas.listar():
                writer.writerow({
                    'id': empresa.id,
                    'nombre': empresa.nombre,
                    'descripcion': empresa.descripcion,
                    'fecha_creacion': empresa.fecha_creacion,
                    'direccion': empresa.direccion,
                    'telefono': empresa.telefono,
                    'correo': empresa.correo,
                    'gerente': empresa.gerente,
                    'equipo_contacto': empresa.equipo_contacto
                })

    def crear_empresa(self, id, nombre, descripcion, fecha_creacion, direccion, telefono, correo, gerente, equipo_contacto):
        nueva_empresa = Empresa(id, nombre, descripcion, fecha_creacion, direccion, telefono, correo, gerente, equipo_contacto)
        self.empresas.agregar(nueva_empresa)
        self.guardar_empresas()

    def listar_empresas(self):
        for empresa in self.empresas.listar():
            print(empresa)

    def buscar_empresa(self, id_empresa):
        return self.empresas.buscar(id_empresa)

    def modificar_empresa(self, id, **kwargs):
        empresa = self.buscar_empresa(id)
        if empresa:
            for key, value in kwargs.items():
                setattr(empresa, key, value)
            self.guardar_empresas()
            return True
        return False

    def eliminar_empresa(self, id):
        if self.empresas.eliminar(id):
            self.guardar_empresas()
            return True
        return False

    def agregar_proyecto(self, id_empresa, id, nombre, descripcion, fecha_inicio, fecha_vencimiento, estado_actual, gerente, equipo):
        empresa = self.buscar_empresa(id_empresa)
        if empresa:
            proyecto = Proyecto(id, nombre, descripcion, fecha_inicio, fecha_vencimiento, estado_actual, gerente, equipo)
            empresa.proyectos.append(proyecto)
            return True
        return False

    def listar_proyectos(self, id_empresa):
        empresa = self.buscar_empresa(id_empresa)
        if empresa:
            if empresa.proyectos:
                print("Proyectos de la empresa:", empresa.nombre)
                for proyecto in empresa.proyectos:
                    print(f"ID: {proyecto.id}, Nombre: {proyecto.nombre}, Descripción: {proyecto.descripcion}, Fecha de inicio: {proyecto.fecha_inicio}, Fecha de vencimiento: {proyecto.fecha_vencimiento}, Estado actual: {proyecto.estado_actual}, Gerente: {proyecto.gerente}, Equipo: {', '.join(proyecto.equipo)}")
                return True
            else:
                print("La empresa no tiene proyectos.")
                return False
        else:
            print("No se encontró la empresa con el ID proporcionado.")
            return False
        
    def listar_proyectos_empresa(gestion_empresas):
        id = input("Ingrese el ID de la empresa para listar sus proyectos: ")
        if gestion_empresas.listar_proyectos(id):
            print("Listado de proyectos completado.")
        else:
            print("No se encontró la empresa o no tiene proyectos.")

#---Modulo 2-----------------------------------------------------------------------------------------------

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
        y.altura = max(self.altura(y.izquierda), self.altura(y.derecha)) + 1
        x.altura = max(self.altura(x.izquierda), self.altura(x.derecha)) + 1
        return x

    def rotacion_izquierda(self, x):
        y = x.derecha
        T2 = y.izquierda
        y.izquierda = x
        x.derecha = T2
        x.altura = max(self.altura(x.izquierda), self.altura(x.derecha)) + 1
        y.altura = max(self.altura(y.izquierda), self.altura(y.derecha)) + 1
        return y

    def insertar(self, raiz, proyecto):
        if not raiz:
            return NodoAVL(proyecto)
        if proyecto.tiempo_restante > raiz.proyecto.tiempo_restante:
            raiz.izquierda = self.insertar(raiz.izquierda, proyecto)
        else:
            raiz.derecha = self.insertar(raiz.derecha, proyecto)

        raiz.altura = 1 + max(self.altura(raiz.izquierda), self.altura(raiz.derecha))
        balance = self.balance(raiz)

        if balance > 1:
            if proyecto.tiempo_restante > raiz.izquierda.proyecto.tiempo_restante:
                return self.rotacion_derecha(raiz)
            else:
                raiz.izquierda = self.rotacion_izquierda(raiz.izquierda)
                return self.rotacion_derecha(raiz)

        if balance < -1:
            if proyecto.tiempo_restante <= raiz.derecha.proyecto.tiempo_restante:
                return self.rotacion_izquierda(raiz)
            else:
                raiz.derecha = self.rotacion_derecha(raiz.derecha)
                return self.rotacion_izquierda(raiz)

        return raiz

    def insertar_proyecto(self, proyecto):
        self.raiz = self.insertar(self.raiz, proyecto)

    def buscar(self, raiz, criterio, valor):
        if not raiz:
            return []
        resultados = []
        if getattr(raiz.proyecto, criterio) == valor:
            resultados.append(raiz.proyecto)
        resultados.extend(self.buscar(raiz.izquierda, criterio, valor))
        resultados.extend(self.buscar(raiz.derecha, criterio, valor))
        return resultados

    def buscar_proyecto(self, criterio, valor):
        return self.buscar(self.raiz, criterio, valor)

    def actualizar_tiempo_restante(self):
        self.actualizar_tiempo_restante_recursivo(self.raiz)

    def actualizar_tiempo_restante_recursivo(self, nodo):
        if nodo:
            nodo.proyecto.actualizar_tiempo_restante()
            self.actualizar_tiempo_restante_recursivo(nodo.izquierda)
            self.actualizar_tiempo_restante_recursivo(nodo.derecha)

class Proyecto:
    def __init__(self, id, nombre, descripcion, fecha_inicio, fecha_vencimiento, estado_actual, empresa, gerente, equipo):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
        self.fecha_vencimiento = datetime.strptime(fecha_vencimiento, "%Y-%m-%d")
        self.estado_actual = estado_actual
        self.empresa = empresa
        self.gerente = gerente
        self.equipo = equipo
        self.tiempo_restante = (self.fecha_vencimiento - datetime.now()).days

    def actualizar_tiempo_restante(self):
        self.tiempo_restante = (self.fecha_vencimiento - datetime.now()).days

    def __str__(self):
        return f"ID: {self.id}, Nombre: {self.nombre}, Descripción: {self.descripcion}, Fecha de inicio: {self.fecha_inicio.strftime('%Y-%m-%d')}, Fecha de vencimiento: {self.fecha_vencimiento.strftime('%Y-%m-%d')}, Estado actual: {self.estado_actual}, Empresa: {self.empresa}, Gerente: {self.gerente}, Equipo: {self.equipo}, Tiempo restante: {self.tiempo_restante} días"

class GestionProyectos:
    def __init__(self):
        self.proyectos = ArbolAVL()

    def crear_proyecto(self, id, nombre, descripcion, fecha_inicio, fecha_vencimiento, estado_actual, empresa, gerente, equipo):
        nuevo_proyecto = Proyecto(id, nombre, descripcion, fecha_inicio, fecha_vencimiento, estado_actual, empresa, gerente, equipo)
        self.proyectos.insertar_proyecto(nuevo_proyecto)

    def buscar_proyectos(self, criterio, valor):
        return self.proyectos.buscar_proyecto(criterio, valor)

    def modificar_proyecto(self, id, **kwargs):
        proyecto = self.buscar_proyectos('id', id)[0]
        if proyecto:
            for key, value in kwargs.items():
                setattr(proyecto, key, value)
            proyecto.actualizar_tiempo_restante()
            return True
        return False

    def eliminar_proyecto(self, id):
        # Implementación simplificada: reconstruir el árbol sin el proyecto eliminado
        proyectos = self.listar_proyectos()
        self.proyectos = ArbolAVL()
        for proyecto in proyectos:
            if proyecto.id != id:
                self.proyectos.insertar_proyecto(proyecto)
        return True

    def listar_proyectos(self):
        return self.proyectos.buscar_proyecto('id', '')  # Retorna todos los proyectos

    def actualizar_tiempos_restantes(self):
        self.proyectos.actualizar_tiempo_restante()



gestion_empresas = GestionEmpresas("empresas.csv")

#Menú principal
def menu_principal():
    gestion_empresas = GestionEmpresas("empresas.csv")
    while True:
        print("\nMenu Principal")
        print("1. Gestionar Empresas")
        print("2. Gestionar Proyectos")
        print("3. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            menu_gestion_empresas(gestion_empresas)
        elif opcion == '2':
            menu_gestion_proyectos(gestion_empresas)
        elif opcion == '3':
            break
        else:
            print("Opción no válida. Intente de nuevo.")
            
#Menú para opc 1
def menu_gestion_empresas(gestion_empresas):
    while True:
        print("\nMenu de Gestión de Empresas")
        print("1. Listar Empresas")
        print("2. Agregar Empresa")
        print("3. Modificar Empresa")
        print("4. Eliminar Empresa")
        print("5. Listar Proyectos de una Empresa")
        print("6. Agregar Proyecto a una Empresa")
        print("7. Volver al Menú Principal")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            gestion_empresas.listar_empresas()
        elif opcion == '2':
            agregar_empresa(gestion_empresas)
        elif opcion == '3':
            modificar_empresa(gestion_empresas)
        elif opcion == '4':
            eliminar_empresa(gestion_empresas)
        elif opcion == '5':
            listar_proyectos_empresa(gestion_empresas)
        elif opcion == '6':
            agregar_proyecto_empresa(gestion_empresas)
        elif opcion == '7':
            break
        else:
            print("Opción no válida. Intente de nuevo.")

def agregar_empresa(gestion_empresas):
    try:
        id = input("Ingresa el id de la empresa: ")
        nombre = input("Ingresar el nombre de la empresa: ")
        descripcion = input("Descripcion de la empresa: ")
        fecha_creacion = input("Ingresa la fecha de creación (YYYY-MM-DD): ")
        direccion = input("Ingrese la direccion de la empresa: ")
        telefono = input("Ingrese el numero de telefono de la empresa: ")
        correo = input("Ingrese el correo de la empresa: ")
        gerente = input("Ingrese el gerente de la empresa: ")
        equipo_contacto = input("Ingrese el equipo de contacto de la empresa: ")

        gestion_empresas.crear_empresa(id, nombre, descripcion, fecha_creacion, direccion, telefono, correo, gerente, equipo_contacto)
        print("Empresa agregada con éxito.")
    except Exception as e:
        print(f"Ocurrió un error al agregar una empresa: {e}")

def modificar_empresa(gestion_empresas):
    id = input("Ingrese el ID de la empresa a modificar: ")
    empresa = gestion_empresas.buscar_empresa(id)
    if empresa:
        print("Deje en blanco los campos que no desea modificar.")
        nombre = input(f"Nuevo nombre ({empresa.nombre}): ") or empresa.nombre
        descripcion = input(f"Nueva descripción ({empresa.descripcion}): ") or empresa.descripcion
        direccion = input(f"Nueva dirección ({empresa.direccion}): ") or empresa.direccion
        telefono = input(f"Nuevo teléfono ({empresa.telefono}): ") or empresa.telefono
        correo = input(f"Nuevo correo ({empresa.correo}): ") or empresa.correo
        gerente = input(f"Nuevo gerente ({empresa.gerente}): ") or empresa.gerente
        equipo_contacto = input(f"Nuevo equipo de contacto ({empresa.equipo_contacto}): ") or empresa.equipo_contacto

        if gestion_empresas.modificar_empresa(id, nombre=nombre, descripcion=descripcion, direccion=direccion, 
                                              telefono=telefono, correo=correo, gerente=gerente, equipo_contacto=equipo_contacto):
            print("Empresa modificada con éxito.")
        else:
            print("No se pudo modificar la empresa.")
    else:
        print("Empresa no encontrada.")

def eliminar_empresa(gestion_empresas):
    id = input("Ingrese el ID de la empresa a1 eliminar: ")
    if gestion_empresas.eliminar_empresa(id):
        print("Empresa eliminada con éxito.")
    else:
        print("No se pudo eliminar la empresa. Verifique el ID.")

def listar_proyectos_empresa(gestion_empresas):
    id = input("Ingrese el ID de la empresa para listar sus proyectos: ")
    if gestion_empresas.listar_proyectos(id):
        print("Listado de proyectos completado.")
    else:
        print("No se encontró la empresa o no tiene proyectos.")

def agregar_proyecto_empresa(gestion_empresas):
    id_empresa = input("Ingrese el ID de la empresa a la que desea agregar un proyecto: ")
    id = input("Ingrese el ID del proyecto: ")
    nombre_proyecto = input("Ingrese el nombre del proyecto: ")
    descripcion_proyecto = input("Ingrese la descripción del proyecto: ")
    fecha_inicio = input("Ingrese la fecha de inicio (YYYY-MM-DD): ")
    fecha_vencimiento = input("Ingrese la fecha de vencimiento (YYYY-MM-DD): ")
    estado_actual = input("Ingrese el estado actual del proyecto: ")
    gerente = input("Ingrese el nombre del gerente del proyecto: ")
    equipo = input("Ingrese los miembros del equipo (separados por comas): ").split(',')

    if gestion_empresas.agregar_proyecto(id_empresa, id, nombre_proyecto, descripcion_proyecto, fecha_inicio, fecha_vencimiento, estado_actual, gerente, equipo):
        print("Proyecto agregado con éxito.")
    else:
        print("No se pudo agregar el proyecto. Verifique el ID de la empresa.")

#Menú para el modulo 2
def menu_gestion_proyectos(gestion_empresas):
    while True:
        print("\nMenu de Gestión de Proyectos")
        print("1. Listar Proyectos")
        print("2. Agregar Proyecto")
        print("3. Modificar Proyecto")
        print("4. Eliminar Proyecto")
        print("5. Buscar Proyectos")
        print("6. Actualizar Tiempos Restantes")
        print("7. Volver al Menú Principal")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            id_empresa = input("Ingrese el ID de la empresa: ")
            gestion_empresas.listar_proyectos(id_empresa)
        elif opcion == '2':
            agregar_proyecto(gestion_empresas)
        elif opcion == '3':
            modificar_proyecto(gestion_empresas)
        elif opcion == '4':
            eliminar_proyecto(gestion_empresas)
        elif opcion == '5':
            buscar_proyectos(gestion_empresas)
        elif opcion == '6':
            gestion_empresas.gestion_proyectos.actualizar_tiempos_restantes()
            print("Tiempos restantes actualizados.")
        elif opcion == '7':
            break
        else:
            print("Opción no válida. Intente de nuevo.")

def agregar_proyecto(gestion_empresas):
    id_empresa = input("Ingrese el ID de la empresa: ")
    id = input("Ingrese el ID del proyecto: ")
    nombre = input("Ingrese el nombre del proyecto: ")
    descripcion = input("Ingrese la descripción del proyecto: ")
    fecha_inicio = input("Ingrese la fecha de inicio (YYYY-MM-DD): ")
    fecha_vencimiento = input("Ingrese la fecha de vencimiento (YYYY-MM-DD): ")
    estado_actual = input("Ingrese el estado actual del proyecto: ")
    gerente = input("Ingrese el nombre del gerente del proyecto: ")
    equipo = input("Ingrese los miembros del equipo (separados por comas): ").split(',')

    if gestion_empresas.agregar_proyecto(id_empresa, id, nombre, descripcion, fecha_inicio, fecha_vencimiento, estado_actual, gerente, equipo):
        print("Proyecto agregado con éxito.")
    else:
        print("No se pudo agregar el proyecto. Verifique el ID de la empresa.")

def modificar_proyecto(gestion_empresas):
    id = input("Ingrese el ID del proyecto a modificar: ")
    # Implementar la lógica para modificar el proyecto

def eliminar_proyecto(gestion_empresas):
    id = input("Ingrese el ID del proyecto a eliminar: ")
    if gestion_empresas.gestion_proyectos.eliminar_proyecto(id):
        print("Proyecto eliminado con éxito.")
    else:
        print("No se pudo eliminar el proyecto. Verifique el ID.")

def buscar_proyectos(gestion_empresas):
    criterio = input("Ingrese el criterio de búsqueda (id, nombre, gerente, fecha_inicio, fecha_vencimiento, estado_actual): ")
    valor = input("Ingrese el valor a buscar: ")
    proyectos = gestion_empresas.gestion_proyectos.buscar_proyectos(criterio, valor)
    for proyecto in proyectos:
        print(proyecto)


if __name__ == "__main__":
    menu_principal()
import requests
from database import Data_Base
from prestamo import Prestamo
from libro import Libro
from empleado import Empleado

class Biblioteca:
    __empleados:list
    __clientes: list
    __libros:list
    __prestamos:list
    def __init__(self):
        self.__empleados = []
        self.__clientes = []
        self.__libros = []
        self.__prestamos = []
        self.__db = Data_Base()
    
    def registrar_empleado(self,empleado):
        self.__empleados.append(empleado)
        if self.__db.insertar_empleado(empleado):
            return f"Empleado '{empleado.get_nombre()}' registrado"
        return f"Error: El email '{empleado.get_email()}' ya está registrado"

    def buscar_empleado_db(self, email):

        empleado = self.__db.buscar_empleado_email(email)
        if empleado:

            return Empleado(empleado[1], empleado[2], empleado[3], empleado[4], empleado[5], empleado[6])

        return None
    
    def registrar_cliente(self,cliente):
        self.__clientes.append(cliente)
        self.__db.insertar_cliente(cliente)
        return f"Cliente '{cliente.get_nombre()}' registrado"

    def agregar_libro(self, libro):
        self.__libros.append(libro)
        self.__db.insertar_libro(libro)
        print(f"Libro '{libro.get_titulo()}' registrado")

    def buscar_cliente_db(self, cedula):
        cli = self.__db.buscar_cliente_cedula(cedula)
        if cli:
            from cliente import Cliente
            return Cliente(cli[1], cli[2], cli[3], cli[4])
        return None
    
    def buscar_libro_db(self, criterio):
        lib = self.__db.buscar_libro_criterio(criterio)
        if lib:
            return Libro(lib[0], lib[1], lib[2], lib[3], lib[4], lib[6])
        return None
    
    def buscar_en_api(self, isbn):
        url = f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data"
        respuesta = requests.get(url, timeout=30)
        
        if respuesta.status_code == 200:
            datos = respuesta.json()
            clave = f"ISBN:{isbn}"
            
            if clave in datos:
                info = datos[clave]
                titulo = info.get("title", "Sin título")
                autor = info.get("authors", [{}])[0].get("name", "Sin autor")
                editorial = info.get("publishers", [{}])[0].get("name", "Sin editorial")
                año = info.get("publish_date", "Sin año")
                print(f"Libro encontrado: {titulo}")
                return titulo, autor, editorial, año
        
        print("ISBN no encontrado en la biblioteca")
        return None
    
    def cargar_libros(self):

        if not self.__db.hay_libros():
            pagina = 0
            print("Cargando libros...")
            
            while True:
                url = f"https://openlibrary.org/search.json?q=novela&limit=100&offset={pagina}&fields=isbn,title,author_name,publisher,first_publish_year"
                respuesta = requests.get(url)
                datos = respuesta.json()

                if pagina >= 200:
                    break

                if not datos["docs"]:
                    break

                for doc in datos["docs"]:
                    isbn = doc.get("isbn", [None])[0]
                    titulo = doc.get("title", "Sin título")
                    autor = doc.get("author_name", ["Sin autor"])[0]
                    editorial = doc.get("publisher", ["Sin editorial"])[0] if doc.get("publisher") else "Sin editorial"
                    año = str(doc.get("first_publish_year", "Sin año"))

                    if isbn:
                        libro = Libro(isbn, titulo, autor, editorial, año, 3)
                        self.agregar_libro(libro)

                pagina += 100
                print(f"Libros cargados: {pagina}")

        else:
            print("Libros ya cargados ")

    def hacer_prestamo(self, empleado, cedula_cliente, isbn_libro):
        cliente = self.buscar_cliente_db(cedula_cliente)
        libro = self.buscar_libro_db(isbn_libro)
        print(f"Disponibles antes: {libro.get_disponibles()}") 

        if not cliente:
            return "Cliente no encontrado "
        if not libro:
            return "Libro no encontrado "
        if not libro.esta_disponible():
            return "Libro no disponible "

        libro.prestar()
        print(f"Disponibles después: {libro.get_disponibles()}") 
        prestamo = Prestamo(libro, cliente, empleado)
        self.__prestamos.append(prestamo)
        empleado.agregar_prestamo(prestamo)
        self.__db.insertar_prestamo(prestamo)
        self.__db.restar_disponible(libro.get_isbn())
        print(f"Guardado en DB: {libro.get_disponibles()}")
        return "Préstamo registrado exitosamente "

    def buscar_prestamo_por_isbn(self, isbn):
        return self.__db.buscar_prestamo_activo_isbn(isbn)
    
    def recibir_devolucion(self, empleado, id_prestamo):
        isbn = self.__db.obtener_isbn_prestamo(id_prestamo)

        if not isbn:
            return "Préstamo no encontrado "
        
        self.__db.cerrar_prestamo(id_prestamo, empleado.get_email())
        self.__db.sumar_disponible(isbn)
        return "Devolución registrada exitosamente "
    
    def login(self, email, password, bcrypt):
        emp = self.__db.buscar_empleado_email(email)
        if emp:
            if bcrypt.check_password_hash(emp[4], password):
                return Empleado(emp[1], emp[2], emp[3], emp[4], emp[5], emp[6])
        return None
    
    def obtener_libros(self):
        return self.__db.obtener_libros()
    
    def cargar_libros_db(self):
        libros = self.__db.obtener_libros()

        for lib in libros:
            libro = Libro(lib[0],lib[1],lib[2], lib[3], lib[4], lib[5])
            self.__libros.append(libro)
        return f"{len(libros)} Cargados con exitoso"
    
    def hay_libros(self):
        return self.__db.hay_libros()
    
    def obtener_prestamos_activos(self):
        return self.__db.obtener_prestamos_activos()
    
    def obtener_clientes(self):
        return self.__db.obtener_clientes_db()
    
    def prestamos_activos(self,isbn):
        prestamos_activos = self.__db.verificar_prestamos_activos_libros(isbn)

        if prestamos_activos:
            return "No se puede eliminar por que hay prestamos activos"
        else: 
            self.__db.eliminar_libro(isbn)
            return "Libro eliminado"

    def eliminar_libro(self, isbn):
        prestamos_activos = self.__db.verificar_prestamos_activos_libros(isbn)

        if prestamos_activos:
            return "No se puede eliminar por que hay prestamos activos"
        else: 
            self.__db.eliminar_libro(isbn)
            return "Libro eliminado"

    def obtener_historial_prestamos(self):
        return self.__db.obtener_prestamos()

    def existe_libro_db(self,isbn):
        self.__db.existe_libro(isbn)


    




















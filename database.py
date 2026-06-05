import sqlite3
from cliente import Cliente
from flask_bcrypt import Bcrypt
from datetime import datetime

bcrypt = Bcrypt()

class Data_Base:
    __conexion: sqlite3.Connection
    __cursor: sqlite3.Cursor

    def __init__(self):
        self.__conexion = sqlite3.connect("biblioteca.db", check_same_thread=False)
        self.__cursor =  self.__conexion.cursor()
        self.__crear_tablas()
        self.crear_admin_inicial()

    def __crear_tablas(self):
        self.__cursor.execute("""
            CREATE TABLE IF NOT EXISTS empleados(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            cedula TEXT,
            email TEXT UNIQUE,
            password TEXT,
            turno TEXT,
            rol TEXT,
            activo INTEGER DEFAULT 1
            )
            """)
        
        self.__cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            cedula TEXT,
            email TEXT UNIQUE,
            telefono TEXT,
            direccion TEXT,
            activo INTEGER DEFAULT 1
            )
            """)

        self.__cursor.execute("""
            CREATE TABLE IF NOT EXISTS libros(
            isbn TEXT PRIMARY KEY,
            titulo  TEXT,
            autor TEXT,
            editorial TEXT,
            año INTEGER,
            cantidad INTEGER,
            disponibles INTEGER              
            )
            """)

        self.__cursor.execute("""
        CREATE TABLE IF NOT EXISTS prestamos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            isbn_libro TEXT,
            cedula_cliente TEXT,
            email_empleado_presto TEXT,
            email_empleado_recibio TEXT,
            fecha_prestamo TEXT,
            fecha_vencimiento TEXT,
            fecha_devolucion TEXT,
            estado TEXT DEFAULT 'activo'
        )
        """)

        self.__conexion.commit()
        print("Tablas creadas ")

    def crear_admin_inicial(self):
        try:
            self.__cursor.execute(
                "SELECT * FROM empleados WHERE rol = ?",
                ("admin",)
            )

            password_admin = bcrypt.generate_password_hash("200728").decode("utf-8")

            if self.__cursor.fetchone() is None:
                self.__cursor.execute(
                    """INSERT INTO empleados
                    (nombre, cedula, email, password, turno, rol)
                    VALUES (?, ?, ?, ?, ?, ?)""",
                    ("Edwin López", "1065880632", "edwin@mail.com",
                    password_admin, "mañana", "admin")
                )
                self.__conexion.commit()
        except Exception as e:
            print(f"Error al crear administrador inicial: {e}")
            raise

    def insertar_empleado(self, empleado):
        try:
            self.__cursor.execute(
                "SELECT * FROM empleados WHERE email = ?",
                (empleado.get_email(),)
            )
            
            if self.__cursor.fetchone() is None:
                self.__cursor.execute("""
                INSERT INTO empleados 
                (nombre, email, password, cedula, turno, rol) 
                VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    empleado.get_nombre(),
                    empleado.get_email(),
                    empleado.get_password(),
                    empleado.get_cedula(),
                    empleado.get_turno(),
                    empleado.get_rol()
                ))

                self.__conexion.commit()
                return True

            return False

        except Exception as e:
            print(f"Error al insertar empleado: {e}")
            return False
        
    def insertar_cliente(self, cliente):
        try:
            self.__cursor.execute("""
            INSERT INTO clientes
            (nombre, cedula,email, telefono, direccion)
            VALUES (?, ?, ?, ?, ?)
            """, (
                cliente.get_nombre(),
                cliente.get_cedula(),
                cliente.get_email(),
                cliente.get_telefono(),
                cliente.get_direccion()
            ))

            self.__conexion.commit()
            print(f"Cliente '{cliente.get_nombre()}' guardado en DB")
            return True

        except Exception as e:
            print(f"Error al insertar cliente: {e}")
            return False

    def insertar_libro(self, libro):
        try:
            self.__cursor.execute(
                "SELECT * FROM libros WHERE isbn = ?",
                (libro.get_isbn(),)
            )

            libro_db = self.__cursor.fetchone()

            if not libro_db:
                self.__cursor.execute("""
                    INSERT INTO libros
                    (isbn, titulo, autor, editorial, año, cantidad, disponibles)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    libro.get_isbn(),
                    libro.get_titulo(),
                    libro.get_autor(),
                    libro.get_editorial(),
                    libro.get_año(),
                    libro.get_cantidad(),
                    libro.get_disponibles()
                ))

                self.__conexion.commit()
                print(f"Libro '{libro.get_titulo()}' guardado en DB")
                return True

            return False

        except Exception as e:
            print(f"Error al insertar libro: {e}")
            return False

    def insertar_prestamo(self, prestamo):
        try:
            self.__cursor.execute("""
                INSERT INTO prestamos
                (isbn_libro, cedula_cliente, email_empleado_presto,
                fecha_prestamo, fecha_vencimiento, estado)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                prestamo.get_libro().get_isbn(),
                prestamo.get_cliente().get_cedula(),
                prestamo.get_empleado_presto().get_email(),
                prestamo.get_fecha_prestamo(),
                prestamo.get_fecha_vencimiento(),
                prestamo.get_estado()
            ))

            self.__conexion.commit()
            print("Préstamo guardado en DB")
            return True

        except Exception as e:
            print(f"Error al guardar préstamo: {e}")
            return False
    
    def obtener_empleados(self):
        self.__cursor.execute("SELECT * FROM empleados")
        return self.__cursor.fetchall()

    def obtener_clientes_db(self):
       clientes = []
       rows = self.__cursor.execute("SELECT * FROM clientes").fetchall()
       for row in rows:
            cliente = Cliente(row[0],row[1], row[2], row[3], row[4], row[5])
            clientes.append(cliente) 
       return clientes
    
    def obtener_libros(self):
        self.__cursor.execute("SELECT * FROM libros")
        return self.__cursor.fetchall()

    def obtener_prestamos(self):
        self.__cursor.execute("SELECT * FROM prestamos")
        return self.__cursor.fetchall()

    def hay_libros(self):
        self.__cursor.execute("SELECT COUNT(*) FROM libros")
        cantidad = self.__cursor.fetchone()[0]
        return cantidad > 0
    
    def buscar_cliente_cedula(self, cedula):
        self.__cursor.execute(
            "SELECT * FROM clientes WHERE cedula = ?", (cedula,)
        )
        return self.__cursor.fetchone()
    
    def buscar_empleado_email(self, email):
        self.__cursor.execute(
            "SELECT * FROM empleados WHERE email = ?", (email,)
        )
        return self.__cursor.fetchone()

    def buscar_prestamo_activo_isbn(self, isbn):
        self.__cursor.execute("""
            SELECT * FROM prestamos 
            WHERE isbn_libro = ? AND estado = 'activo'
        """, (isbn,))
        prestamo = self.__cursor.fetchone()
        
        if prestamo:
            self.__cursor.execute("SELECT titulo FROM libros WHERE isbn = ?", (isbn,))
            titulo = self.__cursor.fetchone()[0]

            self.__cursor.execute("SELECT nombre FROM clientes WHERE cedula = ?", (prestamo[2],))
            cliente = self.__cursor.fetchone()[0]
            
            self.__cursor.execute("SELECT nombre FROM empleados WHERE email = ?", (prestamo[3],))
            empleado = self.__cursor.fetchone()[0]
            
            return (prestamo[0], titulo, cliente, empleado, prestamo[4], prestamo[5], prestamo[6])
        return None
    
    def cerrar_prestamo(self, id_prestamo, email_empleado):

        try:
            self.__cursor.execute("""
                UPDATE prestamos
                SET estado = 'devuelto',
                    email_empleado_recibio = ?,
                    fecha_devolucion = ?
                WHERE id = ?
            """, (
                email_empleado,
                datetime.now().strftime('%Y-%m-%d %H:%M'),
                id_prestamo
            ))

            self.__conexion.commit()
            return True

        except Exception as e:
            print(f"Error al cerrar préstamo: {e}")
            return False

    def obtener_prestamos_activos(self):
        self.__cursor.execute("""
            SELECT * FROM prestamos 
            WHERE estado = 'activo'
        """)
        return self.__cursor.fetchall()
    
    def restar_disponible(self, isbn):
        try:
            self.__cursor.execute("""
                UPDATE libros
                SET disponibles = disponibles - 1
                WHERE isbn = ?
            """, (isbn,))

            self.__conexion.commit()
            return True

        except Exception as e:
            print(f"Error al restar disponible: {e}")
            return False

    def sumar_disponible(self, isbn):
        try:
            self.__cursor.execute("""
                UPDATE libros
                SET disponibles = disponibles + 1
                WHERE isbn = ?
            """, (isbn,))

            self.__conexion.commit()
            return True

        except Exception as e:
            print(f"Error al sumar disponible: {e}")
            return False
        
    def obtener_isbn_prestamo(self, id_prestamo):
        self.__cursor.execute(
            "SELECT isbn_libro FROM prestamos WHERE id = ?",
            (id_prestamo,)
        )
        resultado = self.__cursor.fetchone()
        return resultado[0] if resultado else None
    
    def verificar_prestamos_activos_libros(self,isbn):
        self.__cursor.execute("""
            SELECT * FROM prestamos 
            WHERE isbn_libro = ? AND estado = 'activo'
        """, (isbn,))
        return self.__cursor.fetchall()
    
    def eliminar_libro(self, isbn):
        try:
            self.__cursor.execute("""
                DELETE FROM libros
                WHERE isbn = ?
            """, (isbn,))

            self.__conexion.commit()
            print(f"Libro con ISBN '{isbn}' eliminado de DB")
            return True

        except Exception as e:
            print(f"Error al eliminar el libro: {e}")
            return False

    def existe_libro(self,isbn):
        
        self.__cursor.execute(
            "SELECT 1 FROM libros WHERE isbn = ?",
            (isbn,)
        )
        resultado = self.__cursor.fetchone()

        return resultado is not None

    def buscar_libro_criterio(self, criterio):
        self.__cursor.execute(
            "SELECT * FROM libros WHERE isbn = ? OR LOWER(titulo) = LOWER(?)",
            (criterio, criterio)
        )
        return self.__cursor.fetchone()
    
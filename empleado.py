from persona import Persona

class Empleado(Persona):
    __rol: str
    __prestamos: list
    __turno: str

    def __init__(self, nombre: str = "",cedula: str = "", email: str = "",password: str = "", turno: str = "", rol: str = ""):
        super().__init__(nombre, email, cedula)
        self.__password = password
        self.__rol = rol
        self.__prestamos = []
        self.__turno = turno
        
    def login(self, email: str, password: str) -> bool:
        if self.get_email() == email and self.get_password() == password:
            print(f"Bienvenido {self.get_nombre()}")
            return True
        return False
            
    def tipo_usuario(self) -> str:
        return "Empleado"
    
    def get_password(self):
        return self.__password

    def agregar_prestamo(self, prestamo):
        self.__prestamos.append(prestamo)
        print(f"Préstamo registrado por {self.get_nombre()}")
    
    def recibir_libro(self, prestamo):
        if prestamo in self.__prestamos:
            self.__prestamos.remove(prestamo)
            print(f"Libro recibido por {self.get_nombre()} ")
        else:
            print("Este préstamo no existe ")
    
    def get_rol(self):
        return self.__rol
    
    def get_prestamos(self):
        return self.__prestamos
    
    def get_turno(self):
        return self.__turno
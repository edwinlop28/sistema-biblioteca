from persona import Persona

class Empleado(Persona):
    __rol: str
    __turno: str

    def __init__(self, nombre: str = "",cedula: str = "", email: str = "",password: str = "", turno: str = "", rol: str = ""):
        super().__init__(nombre, email, cedula)
        self.__password = password
        self.__rol = rol
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

    def get_rol(self):
        return self.__rol
    
    def get_prestamos(self):
        return self.__prestamos
    
    def get_turno(self):
        return self.__turno
from persona import Persona

class Empleado(Persona):
    __rol: str
    __turno: str

    def __init__(self, id: int = 0, nombre: str = "", cedula: str = "", email: str = "", password: str = "", turno: str = "", rol: str = ""):
        super().__init__(id, nombre, email, cedula)
        self.__password = password
        self.__rol = rol
        self.__turno = turno
        
            
    def tipo_usuario(self) -> str:
        return "Empleado"
    
    def get_password(self):
        return self.__password

    def get_rol(self):
        return self.__rol
    
    def get_turno(self):
        return self.__turno
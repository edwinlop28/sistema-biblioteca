from persona import Persona

class Empleado(Persona):
    __rol: str
    __turno: str

    def __init__(self, id=0, nombre="", cedula="", email="", password="", turno="", rol=""):
        super().__init__(id, nombre, cedula, email)
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
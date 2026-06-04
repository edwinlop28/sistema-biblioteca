from persona import Persona
class Cliente(Persona):
    __telefono: str
    __direccion: str
    
    def __init__(self,id: int = 0, nombre: str = "", cedula: str = "", email: str = "", telefono: str = "", direccion: str = ""):
        super().__init__(id,nombre, email, cedula)
        self.__telefono = telefono
        self.__direccion = direccion

    def get_telefono(self):
        return self.__telefono
    
    def get_direccion(self):
        return self.__direccion
    
    def get_prestamos(self):
        return self.__prestamos

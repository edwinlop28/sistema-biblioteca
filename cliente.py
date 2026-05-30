from persona import Persona
class Cliente(Persona):
    __telefono: str
    __direccion: str
    __prestamos: list
    def __init__(self, nombre: str = "", cedula: str = "", email: str = "", telefono: str = "", direccion: str = ""):
        super().__init__(nombre, email, cedula)
        self.__telefono = telefono
        self.__direccion = direccion
        self.__prestamos = []
    
    def ver_prestamos(self):
        if self.__prestamos:
            print(f"Prestamos de {self.get_nombre()}:")
            for prestamo in self.__prestamos:
                print(f" - {prestamo}")
        else:
            print("No tienes préstamos activos.")
    
    def tiene_prestamos(self,libro) -> bool:
        if libro in self.__prestamos:
            print("El cliente ya tiene este libro ")
            return True
        return False

    def get_telefono(self):
        return self.__telefono
    
    def get_direccion(self):
        return self.__direccion
    
    def get_prestamos(self):
        return self.__prestamos

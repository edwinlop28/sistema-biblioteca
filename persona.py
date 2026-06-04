class Persona():
    
    def __init__(self,id: int = 0, nombre: str = "", email: str = "", cedula: str = "", ):
        self.__id = id
        self.__nombre = nombre
        self.__email = email
        self.__cedula = cedula
        self._activo = True

    def get_id(self):
        return self.__id

    def get_nombre(self):
        return self.__nombre

    def get_email(self):
        return self.__email
    
    def get_cedula(self):   
        return self.__cedula

    def get_activo(self):
        return self._activo
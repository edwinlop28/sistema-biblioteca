from abc import ABC, abstractmethod
from datetime import datetime

class Persona(ABC):
    _id_contador: int = 1
    
    def __init__(self, nombre: str = "", email: str = "", cedula: str = ""):
        self.__id = Persona._id_contador
        self.__nombre = nombre
        self.__email = email
        self.__cedula = cedula

        self._activo = True
        Persona._id_contador += 1

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
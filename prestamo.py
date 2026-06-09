from datetime import datetime, timedelta

class Prestamo():
    __libro: object
    __cliente: object
    __empleado_presto: object
    __fecha_prestamo: datetime
    __fecha_vencimiento: datetime
    __estado: str

    def __init__(self, libro, cliente, empleado_presto):
        self.__libro = libro
        self.__cliente = cliente
        self.__empleado_presto = empleado_presto
        self.__fecha_prestamo = datetime.now()
        self.__fecha_vencimiento = datetime.now() + timedelta(days=15)
        self.__estado = "activo"

    def get_libro(self):
        return self.__libro

    def get_cliente(self):
        return self.__cliente

    def get_empleado_presto(self):
        return self.__empleado_presto

    def get_fecha_prestamo(self):
        return self.__fecha_prestamo.strftime('%Y-%m-%d %H:%M')

    def get_fecha_vencimiento(self):
        return self.__fecha_vencimiento.strftime('%Y-%m-%d %H:%M')
    
    def get_estado(self):
        return self.__estado
    
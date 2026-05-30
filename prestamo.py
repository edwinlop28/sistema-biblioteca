from datetime import datetime, timedelta

class Prestamo():
    _id_contador: int = 1
    __libro: object
    __cliente: object
    __empleado_presto: object
    __empleado_recibio: object
    __fecha_prestamo: datetime
    __fecha_vencimiento: datetime
    __fecha_devolucion: datetime
    __estado: str

    def __init__(self, libro, cliente, empleado_presto):
        self.__id = Prestamo._id_contador
        self.__libro = libro
        self.__cliente = cliente
        self.__empleado_presto = empleado_presto
        self.__empleado_recibio = None
        self.__fecha_prestamo = datetime.now()
        self.__fecha_vencimiento = datetime.now() + timedelta(days=15)
        self.__fecha_devolucion = None
        self.__estado = "activo"
        Prestamo._id_contador += 1

    def cerrar(self, empleado_recibio):
        if self.__estado == "activo":
            self.__empleado_recibio = empleado_recibio
            self.__fecha_devolucion = datetime.now()
            self.__estado = "devuelto"
            self.__libro.devolver()
            print(f"Préstamo #{self.__id} cerrado")
            print(f"Recibido por: {empleado_recibio.get_nombre()}")
        else:
            print("Este préstamo ya fue cerrado")
    
    def esta_vencido(self) -> bool:
        if datetime.now() > self.__fecha_vencimiento and self.__estado == "activo":
            print(f"Préstamo #{self.__id} está vencido ")
            return True
        return False
    
    def ver_info(self):
        print(f"ID Préstamo  : {self.__id}\nLibro        : {self.__libro.get_titulo()}\nCliente      : {self.__cliente.get_nombre()}\nPrestado por : {self.__empleado_presto.get_nombre()}\nRecibido por : {self.__empleado_recibio.get_nombre() if self.__empleado_recibio else 'Aún no devuelto'}\nFecha préstamo: {self.__fecha_prestamo.strftime('%Y-%m-%d')}\nVence        : {self.__fecha_vencimiento.strftime('%Y-%m-%d')}\nEstado       : {self.__estado}")

    def get_id(self):
        return self.__id

    def get_estado(self):
        return self.__estado

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
    
    
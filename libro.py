class Libro():
    __isbn : str         
    __titulo : str     
    __autor: str 
    __editorial: str  
    __año: int       
    __cantidad : int    
    __disponibles: int

    def __init__(self,isbn = "", titulo = "",autor = "", editorial = "", año = 0, cantidad = 0) :
        self.__isbn = isbn
        self.__titulo = titulo
        self.__autor = autor
        self.__editorial = editorial
        self.__año = año
        self.__cantidad = cantidad
        self.__disponibles = cantidad
    
    def esta_disponible(self) -> bool:
        if self.__disponibles <= 0:
            print("No hay ejemplares disponibles")
            return False
        else:
            return True
    
    def prestar(self):

        if self.esta_disponible():
            self.__disponibles -= 1
            print(f"Libro '{self.__titulo}' prestado")
        else:
            print("No se puede prestar")
        
    def devolver(self):
        
        if self.__disponibles < self.__cantidad:
            self.__disponibles += 1
            print(f"Libro '{self.__titulo}' devuelto")
        else:
            print("Todos los ejemplares ya están en biblioteca")
    
    def ver_info(self):
        print(f"ISBN       : {self.__isbn}\nTítulo     : {self.__titulo}\nAutor      : {self.__autor}\nEditorial  : {self.__editorial}\nAño        : {self.__año}\nDisponibles: {self.__disponibles}/{self.__cantidad}")

    def get_isbn(self):
        return self.__isbn

    def get_titulo(self):
        return self.__titulo

    def get_autor(self):
        return self.__autor

    def get_editorial(self):
        return self.__editorial

    def get_año(self):
        return self.__año

    def get_cantidad(self):
        return self.__cantidad

    def get_disponibles(self):
        return self.__disponibles
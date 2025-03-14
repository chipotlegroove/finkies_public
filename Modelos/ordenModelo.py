###     NO TOQUEN ESTA ATROCIDAD, SE HARÁ DE NUEVO LA MADRE DE ORDEN
###
###
###
class Orden:
    idpedido: int
    idproductos: list
    cantidad: list
    nombre: list
    precio:list
    imagen: list
    direccion: str
    def __init__(self, idpedido:int, idproductos:list,cantidad:list,nombre:list,precio:list,imagen:list, direccion:str):
        self.idpedido=idpedido
        self.idproductos=idproductos
        self.cantidad=cantidad
        self.nombre=nombre
        self.precio=precio
        self.imagen=imagen
        self.direccion=direccion
    
    def __init__():
        pass

    def set_idpedido(self, idpedido: int):
            self._idpedido = idpedido

    def get_idpedido(self):
        return self._idpedido

    # Getters y setters para el atributo idproductos
    def set_idproductos(self, idproductos: list):
        self._idproductos = idproductos

    def get_idproductos(self):
        return self._idproductos

    # Getters y setters para el atributo cantidad
    def set_cantidad(self, cantidad: list):
        self._cantidad = cantidad

    def get_cantidad(self):
        return self._cantidad

    # Getters y setters para el atributo nombre
    def set_nombre(self, nombre: list):
        self._nombre = nombre

    def get_nombre(self):
        return self._nombre

    # Getters y setters para el atributo precio
    def set_precio(self, precio: list):
        self._precio = precio

    def get_precio(self):
        return self._precio

    # Getters y setters para el atributo imagen
    def set_imagen(self, imagen: list):
        self._imagen = imagen

    def get_imagen(self):
        return self._imagen

    # Getters y setters para el atributo direccion
    def set_direccion(self, direccion: str):
        self._direccion = direccion

    def get_direccion(self):
        return self._direccion

    

    




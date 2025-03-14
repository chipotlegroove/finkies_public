from Modelos.productoModelo import Producto
from secretsFinkies import db 
from Modelos.favoritoModelo import Favorito

def agregarFavorito(idUsuario: int, idProducto: int, cantidadPorProducto: int):
    favorito=encontrarFavoritoPorProducto(idUsuario,idProducto)
    if isinstance(favorito,Favorito):    
        favorito.cantidadPorProducto=int(favorito.cantidadPorProducto)+int(cantidadPorProducto)
        db.session.merge(favorito)
        db.session.flush()
    else:
        favorito = Favorito(idUsuario=idUsuario,idProducto=idProducto,cantidadPorProducto=cantidadPorProducto)
        db.session.add(favorito)
    db.session.commit()

def listarFavoritos(idUsuario: int) ->list:
    return db.session.query(Producto, Favorito.cantidadPorProducto).join(Favorito, Producto.idProducto==Favorito.idProducto).filter(Favorito.idUsuario==idUsuario).all()


def encontrarFavoritoPorProducto(idUsuario: int,idProducto: int) -> Favorito:
    return db.session.query(Favorito).filter_by(idUsuario=idUsuario, idProducto=idProducto).first()

def limpiarFavoritos(idUsuario: int):
    favoritos=db.session.query(Favorito).filter(Favorito.idUsuario==idUsuario).all()
    for favorito in favoritos:
        db.session.delete(favorito)
        db.session.commit()

def eliminarFavorito(idUsuario: int, idProducto:int):
    favorito=db.session.query(Favorito).filter_by(idUsuario=idUsuario, idProducto=idProducto).first()
    db.session.delete(favorito)
    db.session.commit()

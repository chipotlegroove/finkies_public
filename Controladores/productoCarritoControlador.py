from secretsFinkies import db 
from Modelos.productoCarritoModelo import productoCarrito

def agregarProductos(productos) -> int:
    id = encontrarIDCarrito()
    for id_producto, producto in productos.items():
        productoCarritoNuevo = productoCarrito(idCarrito=id, idProducto=id_producto, cantidad=producto['cantidad'])
        db.session.add(productoCarritoNuevo)
    db.session.commit()
    return id

def encontrarIDCarrito() -> int:
    id = db.session.query(productoCarrito, db.func.max(productoCarrito.idCarrito)).first()[1]
    if id == None:
        id = 1
    else:
        id += 1
    return id

def listarProductoCarrito(idCarrito: int)-> list:
    productos=db.session.query(productoCarrito).filter_by(idCarrito=idCarrito).all()
    return productos
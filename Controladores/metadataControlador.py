from secretsFinkies import db
from Modelos.metadataModelo import Metadata

def actualizarProductoMes(idProducto:int)->bool:
    try:
        metadata=db.session.query(Metadata).filter(Metadata.llave=='productodelmes').first()
        metadata.valor=idProducto
        db.session.commit()
        return True
    except:
        return False
    

def conseguirIdProductoMes()->int:
    return db.session.query(Metadata).filter(Metadata.llave=='productodelmes').first().valor
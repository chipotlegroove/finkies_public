from secretsFinkies import db
from Modelos.categoriaModelo import Categoria

def conseguirIdCategoria(nombre:str)->int:
    categoria=db.session.query(Categoria).filter(Categoria.categoria==nombre.lower()).first()
    if categoria == None:
        return -1
    return categoria.idCategoria
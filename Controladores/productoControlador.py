from secretsFinkies import db
from Modelos.productoModelo import Producto
from Modelos.categoriaModelo import Categoria
def listarProductos()->list:
    listaProductos=[]
    query=db.session.query(Producto).filter(Producto.idCategoria==Categoria.idCategoria).all()
    for objeto in query:
        diccionarioProducto=crearDiccionarioProducto(objeto)
        listaProductos.append(diccionarioProducto)
    return listaProductos

def actualizarProducto(producto:Producto)->bool:
    try:
        db.session.merge(producto)
        db.session.commit()
        return True
    except:
        return False
    
def crearDiccionarioProducto(producto:Producto)->dict:
        diccionarioProducto={}
        diccionarioProducto['idProducto']=producto.idProducto
        diccionarioProducto['imagen']=producto.imagen
        diccionarioProducto['nombre']=producto.nombre
        diccionarioProducto['descripcionResumida']=producto.descripcionResumida
        diccionarioProducto['costo']=producto.costo
        diccionarioProducto['descripcionGeneral']=producto.descripcionGeneral
        diccionarioProducto['fechaProducto']=producto.fechaProducto
        diccionarioProducto['activo']=producto.activo
        diccionarioProducto['idCategoria']=producto.idCategoria
        return diccionarioProducto

def listarProductosCategoria(listaProductos:list,categoriaString:str)->list:
    categoria=db.session.query(Categoria).filter(Categoria.categoria==categoriaString).first()
    listaProductoCategoria=[]
    if categoria == None:
         return listaProductoCategoria
    for producto in listaProductos:
        if(producto['idCategoria']==categoria.idCategoria):
            listaProductoCategoria.append(producto)
    return listaProductoCategoria

def encontrarProductoPorId(id:int)->Producto:
    return db.session.query(Producto).filter_by(idProducto=id).first()

def listarProductosPorAntiguos(lista:list)->list:
    return sorted(lista, key=lambda x: x['fechaProducto'])

def listarProductosPorRecientes(lista:list)->list:
    return sorted(lista, key=lambda x: x['fechaProducto'],reverse=True)

def purgarInactivos(lista:list)->list:
    listaActivos=[]
    for producto in lista:
        if(producto['activo']==1):
            listaActivos.append(producto)
    return listaActivos
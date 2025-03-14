from secretsFinkies import db
from Modelos.pedidoModelo import Pedido
from Controladores.productoCarritoControlador import agregarProductos
from Modelos.productoCarritoModelo import productoCarrito
from Controladores.direccionUsuarioControlador import direccionCompleta2, direccionCompleta3
from Modelos.productoModelo import Producto
from Controladores.direccionControlador import encontrarDireccionPorId
from utils.correos import formatearDireccion
from datetime import datetime

def guardarPedido(carrito:dict,usuario:int,direccion:int,datos_pago:dict,direcionUsuario:int):
    idCarrito = agregarProductos(carrito)
    fecha = datetime.now()
    costo = datos_pago['purchase_units'][0]['amount']['value']
    email = datos_pago['payer']['email_address']
    estado_envio = 'En camino'
    estado_pago = datos_pago['purchase_units'][0]['payments']['captures'][0]['status']
    pedidoNuevo = Pedido(idUsuario=usuario,idCarrito=idCarrito,costo=costo,fecha=fecha,email=email,idDireccion=direccion,estado_envio=estado_envio,estado_pago=estado_pago,idDireccionUsuario=direcionUsuario)
    db.session.add(pedidoNuevo)
    db.session.commit()

def crearListaPedidos1(usuario:int) -> dict:
    pedidos = db.session.query(Pedido).filter_by(idUsuario=usuario).all()
    listaCarritos = formatearListaCarritos(db.session.query(Pedido.idCarrito).filter_by(idUsuario=usuario).all())
    listaProductos = crearListaImagenes(listaCarritos)
    dict_pedidos = {}
    for pedido in pedidos:
        dict_pedidos[pedido.idPedido] = {}
        dict_pedidos[pedido.idPedido]['id']= pedido.idPedido
        dict_pedidos[pedido.idPedido]['productos'] = []
        dict_pedidos[pedido.idPedido]['fecha'] = pedido.fecha
        dict_pedidos[pedido.idPedido]['costo'] = pedido.costo
        dict_pedidos[pedido.idPedido]['estado_envio'] = pedido.estado_envio
    for producto in listaProductos:
        if len(dict_pedidos[producto[0]]['productos']) == 4:
            pass
        else:
            dict_pedidos[producto[0]]['productos'].append(producto[1])
    return dict_pedidos

def formatearListaCarritos(listaCarritos:list)->list:
    listaFormateada = []
    for carrito in listaCarritos:
        listaFormateada.append(carrito[0])
    return listaFormateada

def encontrarIdCarritoPorIdPedido(idPedido: int):
    pedido=db.session.query(Pedido).filter_by(idPedido=idPedido).first()
    return pedido.idCarrito
def crearListaImagenes(idsCarrito:list)->list:
    return db.session.query(Pedido.idPedido,Producto.imagen).join(productoCarrito, Pedido.idCarrito==productoCarrito.idCarrito).join(Producto, productoCarrito.idProducto==Producto.idProducto).filter(productoCarrito.idCarrito.in_(idsCarrito)).all()
def encontrarIdDireccionPorIdPedido(idPedido: int):
    pedido=db.session.query(Pedido).filter_by(idPedido=idPedido).first()
    return pedido.idDireccion

def crearListaPedidos()->list:
    lista = []
    listaPedidos = db.session.query(Pedido).all()
    for pedido in listaPedidos:
        dict_pedidos= {}
        dict_pedidos['id']= pedido.idPedido
        dict_pedidos['costo'] = pedido.costo
        dict_pedidos['email'] = pedido.email
        lista.append(dict_pedidos)
    return lista
def cambiarEstadoPedidoDB(idpedido:int):
    pedido = db.session.query(Pedido).filter_by(idPedido=idpedido).first()
    print("holaaa")
    if(pedido.estado_envio=="No enviado"):
        pedido.estado_envio="Enviado"
    else:
        pedido.estado_envio="No enviado"
    db.session.merge(pedido)
    db.session.flush()
    db.session.commit()

def crearDiccionarioPedido(idpedido:int)->dict:
    print("ijsoi")
    print(idpedido)
    pedido = db.session.query(Pedido).filter_by(idPedido=idpedido).first()
    pedido_dict = {}
    pedido_dict['productos'] = crearListaProductos(pedido.idCarrito)
    pedido_dict['idPedido'] = pedido.idPedido
    pedido_dict['estado_envio'] = pedido.estado_envio
    pedido_dict['costo'] = pedido.costo
    pedido_dict['fecha'] = pedido.fecha
    pedido_dict['email'] = pedido.email
    pedido_dict['direccion'] = formatearDireccion(encontrarDireccionPorId(pedido.idDireccion).direccion)
    print(pedido_dict['direccion'])
    print("Arriba")
    direccionUsuario = direccionCompleta3(pedido.idDireccionUsuario)
    pedido_dict['nombres'] = direccionUsuario['nombres']
    pedido_dict['apellidos'] = direccionUsuario['apellidos']
    pedido_dict['telefono'] = direccionUsuario['telefono']
    pedido_dict['email'] = direccionUsuario['email']
    return pedido_dict


def crearListaProductos(idCarrito:int)->list:
    return db.session.query(Producto, productoCarrito.cantidad).join(productoCarrito, Producto.idProducto==productoCarrito.idProducto).filter(productoCarrito.idCarrito==idCarrito).all()


def listaIdPedidos(idUsuario:int)->list:
    listaids = []
    lista_fea = db.session.query(Pedido.idPedido).filter_by(idUsuario=idUsuario).all()
    for tupla in lista_fea:
        listaids.append(tupla[0])
    return listaids
#----funciones viejas----------------

def encontrarPedidosPorId(id:int)->list:
    return Pedido.query.filter_by(idUsuario=id).all()



#-----------------------------------

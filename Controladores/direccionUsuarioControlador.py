from secretsFinkies import db
from Modelos.direccionUsuarioModelo import direccionUsuario
from Controladores.direccionControlador import *
from utils.correos import formatearDireccion, separarDireccion

def encontrarDirecciones(idUsuario:int) -> list[direccionUsuario]:
    direcciones = db.session.query(direccionUsuario).filter(direccionUsuario.idUsuario == idUsuario).all()
    return direcciones
    
def direccionCompleta1(idUsuario:int,num_direccion:int) -> dict:
    direcciones = encontrarDirecciones(idUsuario)
    idDireccion = direcciones[num_direccion].idDireccion
    direccion = encontrarDireccionPorId(idDireccion).direccion
    nombres = direcciones[num_direccion].nombres
    apellidos = direcciones[num_direccion].apellidos
    email = direcciones[num_direccion].email
    telefono = direcciones[num_direccion].telefono
    direccionCompleta = {
        'direccion': formatearDireccion(direccion),
        'nombres': nombres,
        'apellidos': apellidos,
        'email': email,
        'telefono': telefono
    }
    return direccionCompleta
def direccionCompleta2(idUsuario:int) -> dict:
    direcciones = encontrarDirecciones(idUsuario)
    diccionarioDirecciones = {}
    for direccionUsuario in direcciones:
        idDireccionUsuario = direccionUsuario.idDireccionUsuario
        idDireccion = direccionUsuario.idDireccion
        direccion = encontrarDireccionPorId(idDireccion).direccion
        nombres = direccionUsuario.nombres
        apellidos = direccionUsuario.apellidos
        email = direccionUsuario.email
        telefono = direccionUsuario.telefono
        direccionCompleta = {
            'idDireccionUsuario': idDireccionUsuario,
            'idDireccion' : idDireccion,
            'direccion': separarDireccion(direccion),
            'nombres': nombres,
            'apellidos': apellidos,
            'email': email,
            'telefono': telefono
        }
        diccionarioDirecciones[idDireccionUsuario] = direccionCompleta
    return diccionarioDirecciones

def direccionCompleta3(idDireccionUsuario:int) -> dict:
    direccionUsuario_encontrado = db.session.query(direccionUsuario).filter(direccionUsuario.idDireccionUsuario == idDireccionUsuario).first()
    idDireccionUsuario = direccionUsuario_encontrado.idDireccionUsuario
    idDireccion = direccionUsuario_encontrado.idDireccion
    direccion = encontrarDireccionPorId(idDireccion).direccion
    nombres = direccionUsuario_encontrado.nombres
    apellidos = direccionUsuario_encontrado.apellidos
    email = direccionUsuario_encontrado.email
    telefono = direccionUsuario_encontrado.telefono
    direccionCompleta = {
        'idDireccionUsuario': idDireccionUsuario,
        'idDireccion' : idDireccion,
        'direccion': separarDireccion(direccion),
        'nombres': nombres,
        'apellidos': apellidos,
        'email': email,
        'telefono': telefono
    }
    return direccionCompleta

def crearDireccionUsuario(datos,idUsuario):
    direccion=f"{datos.get('calle')},{datos.get('numero')},{datos.get('colonia')},{datos.get('codigoPostal')},{datos.get('ciudad')},{datos.get('estado')}"
    idDireccion=encontrarDireccionPorDireccion(direccion).idDireccion
    nombres=datos.get('nombre')
    apellidos=datos.get('apellido')
    email=datos.get('correo')
    telefono=datos.get('telefono')
    direccionNueva = direccionUsuario(idDireccion=idDireccion,idUsuario=idUsuario,nombres=nombres,apellidos=apellidos,email=email,telefono=telefono)
    db.session.add(direccionNueva)
    db.session.commit()
    return direccionNueva.idDireccionUsuario

def editarDireccionUsuario(datos,id):
    usuarioDireccion = db.session.query(direccionUsuario).filter(direccionUsuario.idDireccionUsuario == id).first()
    direccion=f"{datos.get('calle')},{datos.get('numero')},{datos.get('colonia')},{datos.get('codigoPostal')},{datos.get('ciudad')},{datos.get('estado')}"
    print(direccion)
    usuarioDireccion.idDireccion=encontrarDireccionPorDireccion(direccion).idDireccion
    usuarioDireccion.nombres=datos.get('nombre')
    usuarioDireccion.apellidos=datos.get('apellido')
    usuarioDireccion.email=datos.get('correo')
    usuarioDireccion.telefono=datos.get('telefono')
    db.session.merge(usuarioDireccion)
    db.session.flush()
    db.session.commit()

def eliminarDirecciones(idDireccionUsuario: int):
    direccion=db.session.query(direccionUsuario).filter(direccionUsuario.idDireccionUsuario==idDireccionUsuario).first()
    db.session.delete(direccion)
    db.session.commit()
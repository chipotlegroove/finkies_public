import hashlib
from secretsFinkies import db
from Modelos.usuarioModelo import Usuario

def encriptarContrasena(contrasena:str)->str:
    hash_object = hashlib.sha256()
    hash_object.update(contrasena.encode('utf-8'))
    hash_password = hash_object.hexdigest()
    return hash_password

def crearDiccUsuario(usuario:Usuario)-> dict:
    diccionario={}
    diccionario['idUsuario']=usuario.idUsuario
    diccionario['nombreUsuario']=usuario.nombreUsuario
    diccionario['correo']=usuario.correo
    diccionario['nombre']=usuario.nombre
    diccionario['apellido1']=usuario.apellido1
    diccionario['apellido2']=usuario.apellido2
    return diccionario
    
def crearUsuario(datos):
    usuario_nuevo = Usuario(nombreUsuario=datos.get('username'),nombre=datos.get('nombre'),apellido1=datos.get('apellido1'),apellido2=datos.get('apellido2'),correo=datos.get('correo'),contrasena=encriptarContrasena(datos.get('contrasena')))
    db.session.add(usuario_nuevo)
    db.session.commit()
    
def verificarContrasena(correo:str, contrasena_ingresada:str)->Usuario:
    return db.session.query(Usuario).filter_by(correo=correo, contrasena=contrasena_ingresada).first()

def correoExistente(correo:str) ->bool:
    usuario=db.session.query(Usuario).filter_by(correo=correo).first()
    return isinstance(usuario,Usuario)
def encontrarUsuarioPorCorreo(correo:str)->Usuario:
    return db.session.query(Usuario).filter_by(correo=correo).first()

def actualizarContrasena(usuario: Usuario, contrasena:str):
    usuario.contrasena=encriptarContrasena(contrasena)
    db.session.merge(usuario)
    db.session.flush()
    db.session.commit()
def actualizarDatosUsuario(datos,session):
    correo=datos.get('correo')
    usuario=db.session.query(Usuario).filter(Usuario.correo==correo).first()
    if (len(datos.get('password'))==0):
        usuario.nombreUsuario=datos.get("nombreUsuario")
        usuario.nombre=datos.get("nombre")
        usuario.apellido1=datos.get("apellido1")
        usuario.apellido2=datos.get("apellido2")
    else:
        usuario.nombreUsuario=datos.get("nombreUsuario")
        usuario.nombre=datos.get("nombre")
        usuario.apellido1=datos.get("apellido1")
        usuario.apellido2=datos.get("apellido2")
        usuario.contrasena=encriptarContrasena(datos.get('password'))
    db.session.merge(usuario)
    db.session.flush()
    db.session.commit()
    session['usuario']=crearDiccUsuario(usuario)
from secretsFinkies import db
from Modelos.administradorModelo import Administrador

def verificarAdmin(correo:str, contrasena_ingresada:str)->Administrador:
    return db.session.query(Administrador).filter_by(correo=correo, contrasena=contrasena_ingresada).first()

def encontrarAdmin(correo:str)->Administrador:
    return db.session.query(Administrador).filter_by(correo=correo).first()

def crearDiccAdmin(admin:Administrador)-> dict:
    diccionario={}
    diccionario['idAdministrador']=admin.idAdministrador
    diccionario['correo']=admin.correo
    diccionario['nombre']=admin.nombre
    diccionario['apellido1']=admin.apellido1
    diccionario['apellido2']=admin.apellido2
    return diccionario
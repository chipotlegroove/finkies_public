from secretsFinkies import db
from Modelos.direccionModelo import Direccion

def encontrarDireccionPorId(id:int)->Direccion:
    return db.session.query(Direccion).filter_by(idDireccion=id).first()
def encontrarDireccionPorDireccion(direccion:str)->Direccion:
    return db.session.query(Direccion).filter_by(direccion=direccion).first()
def crearDireccion(datos):
    direccion=f"{datos.get('calle')},{datos.get('numero')},{datos.get('colonia')},{datos.get('codigoPostal')},{datos.get('ciudad')},{datos.get('estado')}"
    print(direccion)
    if not isinstance(encontrarDireccionPorDireccion(direccion),Direccion):
        direccionNueva = Direccion(direccion=direccion)
        db.session.add(direccionNueva)
        db.session.commit()

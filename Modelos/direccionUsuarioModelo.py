from secretsFinkies import db


class direccionUsuario(db.Model):
    __tablename__ = 'direccionUsuario'
    idDireccionUsuario = db.Column(db.Integer, primary_key=True)
    idDireccion =  db.Column(db.Integer, db.ForeignKey('direcciones.idDireccion'), nullable=False)
    idUsuario = db.Column(db.Integer, db.ForeignKey('usuarios.idUsuario'), nullable=False)
    nombres = db.Column(db.String(255), nullable=False)
    apellidos = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    telefono = db.Column(db.String(255), nullable=False)

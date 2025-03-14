from secretsFinkies import db

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    idUsuario = db.Column(db.Integer, primary_key=True)
    nombreUsuario = db.Column(db.String(100))
    correo = db.Column(db.String(100), nullable=False, unique=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido1 = db.Column(db.String(100), nullable=False)
    apellido2 = db.Column(db.String(100))
    contrasena = db.Column(db.String(100), nullable=False)



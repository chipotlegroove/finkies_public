from secretsFinkies import db

class Direccion(db.Model):
    __tablename__ = 'direcciones'
    idDireccion = db.Column(db.Integer, primary_key=True)
    direccion = db.Column(db.String(255), nullable=False)
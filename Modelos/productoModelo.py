from secretsFinkies import db

class Producto(db.Model):
    __tablename__ = 'productos'

    idProducto = db.Column(db.Integer, primary_key=True)
    imagen = db.Column(db.String(100), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    descripcionResumida = db.Column(db.String(100))
    costo = db.Column(db.Float, nullable=False)
    descripcionGeneral = db.Column(db.String(100))
    fechaProducto = db.Column(db.Date, nullable=False)
    activo = db.Column(db.Boolean, nullable=False)

    idCategoria = db.Column(db.Integer, db.ForeignKey('categorias.idCategoria'), nullable=False)
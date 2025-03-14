from secretsFinkies import db

class productoCarrito(db.Model):
    __tablename__ = 'productoCarrito'
    idProductoCarrito = db.Column(db.Integer, primary_key=True)
    idCarrito = db.Column(db.Integer, nullable=False)
    idProducto = db.Column(db.Integer, db.ForeignKey('productos.idProducto'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
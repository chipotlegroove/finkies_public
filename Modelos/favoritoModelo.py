from secretsFinkies import db

class Favorito(db.Model):
    __tablename__='favoritos'
    idFavorito = db.Column(db.Integer, primary_key=True)
    idUsuario = db.Column(db.Integer, db.ForeignKey('usuarios.idUsuario'),nullable=False)
    idProducto = db.Column(db.Integer, db.ForeignKey('productos.idProducto'),nullable=False)
    cantidadPorProducto = db.Column(db.Integer, nullable=False)
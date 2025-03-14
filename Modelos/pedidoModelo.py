from sqlalchemy import ForeignKey
from secretsFinkies import db

class Pedido(db.Model):
    __tablename__ = 'pedidos'
    idPedido = db.Column(db.Integer, primary_key=True)
    idUsuario = db.Column(db.Integer, db.ForeignKey('usuarios.idUsuario'), nullable=False)
    idCarrito = db.Column(db.Integer, nullable=False)
    costo = db.Column(db.Float, nullable=False)
    fecha = db.Column(db.DateTime, nullable=False)
    email = db.Column(db.String(255), nullable=False)
    idDireccion = db.Column(db.Integer, db.ForeignKey('direcciones.idDireccion'), nullable=False)
    idDireccionUsuario = db.Column(db.Integer, db.ForeignKey('direccionUsuario.idDireccionUsuario'), nullable=False)
    estado_envio = db.Column(db.String(255), nullable=False)
    estado_pago = db.Column(db.String(255), nullable=False)
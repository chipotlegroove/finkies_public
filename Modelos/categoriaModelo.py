from secretsFinkies import db

class Categoria(db.Model):
    __tablename__ = 'categorias'
    idCategoria = db.Column(db.Integer, primary_key=True)
    categoria = db.Column(db.String(100), nullable=False)
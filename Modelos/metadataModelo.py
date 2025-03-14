from secretsFinkies import db

class Metadata(db.Model):
    __tablename__ = 'finkies_metadata'

    idMetadata = db.Column(db.Integer, primary_key=True)
    llave = db.Column(db.String(255), nullable=False)
    valor = db.Column(db.String(255), nullable=False)
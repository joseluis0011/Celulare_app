from project import db


class Product(db.Model):

    __tablename__ = 'celular'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(128), nullable=False)
    cantidad = db.Column(db.Integer(), nullable=False)
    serie = db.Column(db.String(128), nullable=False)
    modelo = db.Column(db.String(128), nullable=False)
    marca = db.Column(db.String(128), nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'cantidad': self.cantidad,
            'serie': self.serie,
            'modelo': self.modelo,
            'marca': self.marca
        }

    def __init__(self, nombre, cantidad, serie, modelo, marca):
        self.nombre = nombre
        self.cantidad = cantidad
        self.serie = serie
        self.modelo = modelo
        self.marca = marca

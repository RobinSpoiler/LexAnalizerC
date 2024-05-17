from flask_sqlalchemy import SQLAlchemy

# Crear una instancia de SQLAlchemy
db = SQLAlchemy()

# Definir el modelo de la base de datos
class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100))
    content = db.Column(db.Text)

    def __repr__(self):
        return f'<File {self.filename}>'

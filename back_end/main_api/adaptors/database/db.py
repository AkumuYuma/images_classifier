from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Img(db.Model):
    # Modello dell'immagine.
    # id -> la primary_key del db
    # img -> buffer dell'immagine
    # name -> Nome immagine
    # mimetype -> estensione immagine
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.Text, unique=True, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)

def db_init(app):
    # Inizializzatore del db.
    # Il db viene auto generato ad ogni run dell'api e crea la tabels
    db.init_app(app)

    with app.app_context():
        db.create_all()

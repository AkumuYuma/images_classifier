from flask import Flask, render_template, request, make_response, abort
import json
from flask_cors import CORS
from flask_pymongo import PyMongo


# Configuro la connessione a mongodb.
def db_init(app):
    dbName = "images"
    app.config[ "MONGO_URI" ] = "mongodb://localhost:27017/" + dbName
    mongo = PyMongo(app)
    return mongo

app = Flask(__name__)
# Permetto le richieste CORS
CORS(app)


# Main path (test)
@app.route('/')
def hello_world():
    return render_template("home.html")

# Route per l'upload di un file
@app.route('/upload', methods=["POST"])
def upload():
    """
        Path per l'upload di un file mandato tramite richiesta POST.
        Il file viene salvato nel database Mongo.
    """
    file = request.files["inputFile"]
    if not file:
        abort(
            404,
            description = "No file Selected"
        )
    # Metodo di flask_pymongo per salvare i file di grandi dimensioni (tramite GridFS)
    # Nota che se non specificato, il formato viene indovinato tramite guess_type()
    # È possibile passare altri attributi da salvare nel db (tipo stato: processato/non processato exx)
    # Vedi documentazione flask_pymongo
    # TODO trovare il modo di salvare il file con un indice incrementale
    mongo.save_file(file.filename, file)
    return make_response(f"File {file.filename} uploaded")

# get del file tramite il filename
@app.route("/read/<path:filename>")
def get_file(filename):
    return mongo.send_file(filename)

# TODO possibilità di leggere la lista di tutte le foto
@app.route("/read")
def read_all():
    return make_response(str(mongo.cx.fs.files.find()))


if __name__ == "__main__":
    mongo = db_init(app)
    app.run(host="0.0.0.0", debug=True)

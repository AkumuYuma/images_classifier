from flask import Flask, render_template, request, abort, jsonify
from flask_cors import CORS
from Database_adaptor import Database_adaptor


app = Flask(__name__)



# Main path (test)
@app.route('/')
def hello_world():
    """
        Main page con html per il caricamento
    """
    return render_template("home.html")


# Route per l'upload di un file
@app.route('/api/upload/input=<inputFile>', methods=["POST"])
def upload(inputFile):
    """
        Path per l'upload di un file mandato tramite richiesta POST.
        Il file viene salvato nel database Mongo.
        :param: immagine
        :return: json con id del file caricato
    """
    file = request.files[inputFile]
    if not file:
        abort(
            404,
            description="No file Selected"
        )

    # stato del file. Metadati. Per il momento solo processato (dal ML) e permaSaved (nell'OS)
    # Gli altri servizi andranno a cercare nel db tramite lo stato del file
    # prenderanno i file di interesse, li processeranno e modificheranno lo stato del file nel db.
    fileId = database.save_image(file.filename, file, processed=False, permaSaved=False, classification=None)
    return jsonify({"id": str(fileId)})

# Route per fare la query allo stato del file nel db da parte degli altri servizi


@app.route('/api/get_state/id=<file_Id>')
def get_state(file_Id):
    """
        :param: fileId -> Id del file da controllare.
        :return: json con stato dell'oggetto, 404 se file inesistente
    """
    file_Id = database.type_conversion(file_Id)
    file_obj = database.find_one({"_id": file_Id})
    if not file_obj:
        abort(
            404,
            description="Invalid id"
        )
    res = {
        "processed": file_obj["processed"],
        "permaSaved": file_obj["permaSaved"],
        "classification": file_obj["classification"]
    }
    return jsonify(res)


# get del file tramite il filename
# NOTA: questo metodo è di debug, il filename non è detto che sia unico
@app.route('/api/view_one/name=<file_name>')
def get_file(file_name):
    """
        :param: fileName -> nome del file
        :return: prima occorrenza dell'immagine con nome richiesto
    """
    return database.send_image(file_name)


if __name__ == "__main__":
    database = Database_adaptor(app, "images")
    # Permetto le richieste CORS
    CORS(app)
    app.run(host="0.0.0.0", debug=True)

from flask_pymongo import PyMongo
from bson.objectid import ObjectId

class Database_adaptor():
    def __init__(self, app, db_name):
        """
            Inizializzatore dell'adattatore.
            :param: app-> Flask app
            :param: db_name -> Nome del db da creare
        """
        app.config[ "MONGO_URI" ] = "mongodb://localhost:27017/" + db_name
        self._adaptor = PyMongo(app)

    def save_image(self, image_name, image, **kwargs):
        """
            Salva l'immagine mandata.
            :param: image_name -> Nome dell'immagine
            :param: image -> File
            :param: **kwargs -> Ulteriori dati arbitrari da aggiungere
            :return: ObjectId, indica l'id univoco nel db
        """
        return self._adaptor.save_file(image_name, image, **kwargs)

    def send_image(self, image_name):
        """
            Restituisce l'immagine
            :param: image_name -> Nome immagine
            :return: prima occorrenza dell'immagine con quel nome
        """
        return self._adaptor.send_file(image_name)

    def find_one(self, query):
        """
            Fa una query ad db e restituisce la prima occorrenza.
            :param: query -> Criterio per ricerca
            :return: prima occorrenza dell'oggetto oppure none
        """
        return self._adaptor.db.fs.files.find_one(query)

    def type_conversion(self, fileId):
        """
            Converte l'id passato come argomento nel tipo corretto da utilizzare come
            primary key (o id) del database
            :param: fileId : stringa -> Id da convertire
            :return: fileId del giusto tipo
        """
        return ObjectId(fileId)

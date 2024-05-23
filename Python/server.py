# server.py

from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from parser import compareFilesWithTokens, compareFilesAsText,cleanTokensList
from tables import db, File
from semanticDiff import getSemanticValues
import io

def getPlainText(file):
    with io.BytesIO(file.read()) as f:  # Lee el contenido del archivo en un buffer en memoria
        return f.read()


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, methods=["GET", "POST"], allow_headers=["Content-Type"])

# Configurar la base de datos SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Ruta de la base de datos
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #No queremos que registre quien hace las llamadas, solo consume recursos

db.init_app(app)

# Crear las tablas en la base de datos
with app.app_context():
    db.create_all()

# ===================================Rutas para BD==============================================

# Ruta para agregar un nuevo archivo a la base de datos
@app.route('/addFile', methods=['POST'])
def add_file():
    # Verificar si se han enviado archivos
    if 'files' not in request.files:
        return jsonify({'error': 'No se han enviado archivos'}), 400

    # Obtener los archivos enviados
    files = request.files.getlist('files')

    # Iterar sobre los archivos y guardarlos en la base de datos
    for file in files:
        filename = file.filename
        content = file.read()  # Leer el contenido del archivo
        new_file = File(filename=filename, content=content)
        db.session.add(new_file)
    db.session.commit()

    print(content)
    return jsonify({'message': 'Archivos agregados correctamente'}), 200

# Ruta para obtener todos los archivos de la base de datos
@app.route('/getFiles', methods=['GET'])
def get_files():
    ##Prueba
    files = File.query.all()
    file_data = {}
    for file in files:
        file_data[file.id] = {'id': file.id, 'filename': file.filename, 'content': file.content}
    for key in file_data:
        file_data[key]['content'] = file_data[key]['content'].decode('utf-8')
    # print(file_data)
    return jsonify(file_data), 200


# Ruta para llamar los alogitmos de comparacion
@app.route('/compare', methods=['POST'])
def compare_files():
    file1 = request.files['file1']
    file2 = request.files['file2']

    if not (file1 and file2):
        return jsonify({'error': 'Debes proporcionar dos archivos'}), 400


    # Para obtener línea por línea lo que está ocurriendo
    file1Text = getPlainText(file1).decode("utf-8").splitlines()
    file2Text = getPlainText(file2).decode("utf-8").splitlines()

    # Realizar la comparación de archivos
    text_similarity = compareFilesAsText(file1, file2)
    
    token_similarity_kind, token_similarity_value, tokensList1, tokensList2 = compareFilesWithTokens(file1, file2)
    cleanTokens1 = cleanTokensList(tokensList1)
    cleanTokens2 = cleanTokensList(tokensList2)

    comparison_results = {
        'text_similarity': text_similarity,
        'token_similarity_kind': token_similarity_kind,
        'token_similarity_value': token_similarity_value,
        'tokensList1': tokensList1,
        'tokensList2': tokensList2,
        'cleanTokensList1': cleanTokens1,
        'cleanTokensList2': cleanTokens2,

        'fileA': {
            'string': {},
            'tokenizado': {},
            'semantico': getSemanticValues(file1Text, cleanTokens1)
        },
        'fileB': {
            'string': {},
            'tokenizado': {},
            'semantico': getSemanticValues(file2Text, cleanTokens2)
        }
    }

    ##regresa valores para highlight
    return jsonify(comparison_results)
    """
    fileA: {
        string: {
            similitud: [
                { lineNumber: int (desde 1), indices: [[int, int] ... }
            ]
        }
        token: {
            similitud: [
                { lineNumber: int (desde 1), indices: [[int, int] ... }
            ]
        }
        semántico: {
            variables: [
                { lineNumber: int (desde 1), indices: [[int, int] ... }
            ]
            ciclos: [
                { lineNumber: int (desde 1), indices: [[int, int] ... }
            ]
            operators: [
                { lineNumber: int (desde 1), indices: [[int, int] ... }
            ]
            argumentos: [
                { lineNumber: int (desde 1), indices: [[int, int] ... }
            ]
        }
    fileB: {
        string: {
            similitud: [
                { lineNumber: int (desde 1), indices: [[int, int] ... }
            ]
        }
        token: {
            similitud: [
                { lineNumber: int (desde 1), indices: [[int, int] ... }
            ]
        }
        semántico: {
            variables: [
                { lineNumber: int (desde 1), indices: [[int, int] ... }
            ]
            ciclos: [
                { lineNumber: int (desde 1), indices: [[int, int] ... }
            ]
            operators: [
                { lineNumber: int (desde 1), indices: [[int, int] ... }
            ]
            argumentos: [
                { lineNumber: int (desde 1), indices: [[int, int] ... }
            ]
        }
    }
    """

if __name__ == '__main__':
    app.run(debug=True)
# server.py

from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from parser import compareFilesWithTokens, compareFilesAsText, cleanTokensList
from tables import db, File
from semanticDiff import getSemanticValues
# import io

def getPlainText(file):
    with io.BytesIO(file.read()) as f:  # Lee el contenido del archivo en un buffer en memoria
        return f.read()

import collections

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

    # Delete all existing files from the database before adding new ones
    db.session.query(File).delete()
    db.session.commit()
    
    # Obtener los archivos enviados
    files = request.files.getlist('files')

    # Iterar sobre los archivos y guardarlos en la base de datos
    for file in files:
        filename = file.filename
        content = file.read()  # Leer el contenido del archivo
        new_file = File(filename=filename, content=content)
        db.session.add(new_file)
    db.session.commit()

    # print(content)
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

@app.route('/getFileByName', methods=['GET'])
def get_file_by_name():
    file_name = request.args.get('name')

    # print("filename: ", file_name)
    if not file_name:
        return jsonify({"error": "No file name provided"}), 400

    file = File.query.filter_by(filename=file_name).first()
    if not file:
        return jsonify({"error": "File not found"}), 404

    file_data = {
        'id': file.id,
        'filename': file.filename,
        'content': file.content.decode('utf-8')
    }

    return jsonify(file_data), 200

# Ruta para llamar los alogitmos de comparacion
@app.route('/compare', methods=['POST'])
def compare_files():
    
    data = {
        # "comp1": {
        #     "id": "Paola vs Marco",
        #     "file_names": ["prueba1.py", "prueba2.py"],
        #     "porcentaje": 78
    }
    

    # Para obtener línea por línea lo que está ocurriendo
    # Realizar la comparación de archivos
    allFilesRequest = request.json
    compNum = 1
    # print(len(allFilesRequest["body"]))
    for alumno1 in allFilesRequest["body"]:
        fileContent1 = allFilesRequest["body"][alumno1]["content"]
        fileName1 = allFilesRequest["body"][alumno1]["filename"]
        for alumno2 in allFilesRequest["body"]:
            if(alumno1 != alumno2):
                fileContent2 = allFilesRequest["body"][alumno2]["content"]
                fileName2 = allFilesRequest["body"][alumno2]["filename"]
                text_similarity = compareFilesAsText(fileContent1, fileContent2)
                similarityKind, similarityValue,tokensList1, tokensList2 = compareFilesWithTokens(fileName1, fileName2,fileContent1, fileContent2)
                porcentaje = (similarityKind + similarityValue + text_similarity) // 3

                # print('\n')
                # print(fileContent1, fileName1, fileContent2,fileName2)
                data[compNum] = {"id": '%s vs %s' % (fileName1, fileName2), "file_names":[fileName1,fileName2], "porcentaje": porcentaje}
                compNum += 1
    # data = sorted(data.items(), key=lambda x: x, reverse=True) 
    # print(data)
    
    
    # comparison_results = {
    #     'text_similarity': text_similarity,
    #     'token_similarity_kind': token_similarity_kind,
    #     'token_similarity_value': token_similarity_value,
    #     'tokensList1': tokensList1,
    #     'tokensList2': tokensList2,
    #     'cleanTokensList1': cleanTokens1,
    #     'cleanTokensList2': cleanTokens2,
    #     'variables1' : highVariables1,
    #     'variables2' : highVariables2,
    #     'ifstatements1' : hightIfelse1,
    #     'ifstatements2' :hightIfelse2,
    #     'loops1': highLoops1,
    #     'loops2': highLoops2,

    
    #     }
    # return jsonify(comparison_results)
    return data


@app.route('/highlight', methods=['POST'])
def highlight():
    comparison_results = {

        # 'fileA': {
        #     'string': {},
        #     'tokenizado': {},
        #     'semantico': getSemanticValues(file1Text, cleanTokens1)
        # },
        # 'fileB': {
        #     'string': {},
        #     'tokenizado': {},
        #     'semantico': getSemanticValues(file2Text, cleanTokens2)
        # }
    }

    allFilesRequest = request.json

    # print(allFilesRequest["body"])
    arrNames = []
    for filename in allFilesRequest["body"]:
        arrNames.append(filename)
    
    fileContent1 = allFilesRequest["body"][arrNames[0]]
    fileContent2 = allFilesRequest["body"][arrNames[1]]

    similarityKind, similarityValue, tokensList1, tokensList2 = compareFilesWithTokens(arrNames[0], arrNames[1],fileContent1, fileContent2)

    cleanTokens1 = cleanTokensList(tokensList1)
    cleanTokens2 = cleanTokensList(tokensList2)

    #Simple text comparisson

    textSimilarityFile1, textSimilarityFile2 = compareFilesAsText(fileContent1, fileContent2)
    comparison_results[arrNames[0]] = {"string": textSimilarityFile1}
    comparison_results[arrNames[1]] = {"string": textSimilarityFile2}


    comparison_results[arrNames[0]] = {"semantico": getSemanticValues(fileContent1, cleanTokens1)}
    comparison_results[arrNames[1]] = {"semantico": getSemanticValues(fileContent2, cleanTokens2)}

    print(comparison_results)
    return jsonify(comparison_results), 200



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
# server.py

from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from parser import compareFilesWithTokens, compareFilesAsText,cleanTokensList, variables, ifStatement, loops
from tables import db, File
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
    print(file_data)
    return jsonify(file_data), 200

@app.route('/getFileByName', methods=['GET'])
def get_file_by_name():
    file_name = request.args.get('name')

    print("filename: ", file_name)
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
    
    # Realizar la comparación de archivos
    allFilesRequest = request.json
    compNum = 1
    print(len(allFilesRequest["body"]))
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

                print('\n')
                print(fileContent1, fileName1, fileContent2,fileName2)
                data[compNum] = {"id": '%s vs %s' % (fileName1, fileName2), "file_names":[fileName1,fileName2], "porcentaje": porcentaje}
                compNum += 1
    # data = sorted(data.items(), key=lambda x: x, reverse=True) 
    print(data)
    
    
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


# @app.route('/compare2', methods=['GET'])
# def compare_files():
#     file1 = request.files['file1']
#     file2 = request.files['file2']
#     #Ultimo de la

#     if not (file1 and file2):
#         return jsonify({'error': 'Debes proporcionar dos archivos'}), 400

#     # Realizar la comparación de archivos
#     text_similarity = compareFilesAsText(file1, file2)
#     token_similarity_kind, token_similarity_value,tokensList1, tokensList2 = compareFilesWithTokens(file1, file2)
#     cleanTokens = cleanTokensList(tokensList1)
#     highVariables = variables(cleanTokens)

#     comparison_results = {
#         'text_similarity': text_similarity,
#         'token_similarity_kind': token_similarity_kind,
#         'token_similarity_value': token_similarity_value,
#         'tokensList1': tokensList1,
#         'tokensList2': tokensList2,
#         'cleanTokensList': cleanTokens,
#         'variables': highVariables,
        
#     }
    ##regresa valores para highlight
    

    return jsonify(comparison_results)


# @app.route('/')
# def index():
#     response = make_response('Hello, World!')
#     response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5173'
#     return response

# @app.route('/overviewMatrix')
# def index():
#     response = make_response('Hello, World!')
#     response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5173'
#     return response

if __name__ == '__main__':
    app.run(debug=True)
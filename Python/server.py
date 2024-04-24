# server.py

from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from parser_1 import compareFilesWithTokens, compareFilesAsText

app = Flask(__name__)
CORS(app, methods=["GET", "POST"], allow_headers=["Content-Type"])

@app.route('/compare', methods=['POST'])
def compare_files():
    file1 = request.files['file1']
    file2 = request.files['file2']

    if not (file1 and file2):
        return jsonify({'error': 'Debes proporcionar dos archivos'}), 400

    # Realizar la comparación de archivos
    text_similarity = compareFilesAsText(file1, file2)
    token_similarity_kind, token_similarity_value = compareFilesWithTokens(file1, file2)
    
    comparison_results = {
        'text_similarity': text_similarity,
        'token_similarity_kind': token_similarity_kind,
        'token_similarity_value': token_similarity_value
    }

    return jsonify(comparison_results)

@app.route('/')
def index():
    response = make_response('Hello, World!')
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5173'
    return response

if __name__ == '__main__':
    app.run(debug=True)

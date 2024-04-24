from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from parser import compareFilesWithTokens, compareFilesAsText

app = Flask(__name__)
CORS(app, methods=["GET", "POST"], allow_headers=["Content-Type"])

@app.route('/compare', methods=['POST'])
def compare_files():
    files = request.files
    print(files)
    if len(files) != 2:
        return jsonify({'error': 'Exactly two files must be provided'}), 400
    
    file1 = files[0]
    file2 = files[1]

    
    # Perform comparison
    comparison_results = {}
    comparison_results['text_similarity'] = compareFilesAsText(file1, file2)
    comparison_results['token_similarity'] = compareFilesWithTokens(file1, file2)
    
    return jsonify(comparison_results)

@app.route('/')
def index():
    response = make_response('Hello, World!')
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:5173'
    return response

if __name__ == '__main__':
    app.run(debug=True)

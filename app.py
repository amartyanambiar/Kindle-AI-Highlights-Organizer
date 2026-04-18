from flask import Flask, request, jsonify, render_template, make_response
import os
from werkzeug.utils import secure_filename

try:
    from flask_cors import CORS
    _CORS_AVAILABLE = True
except Exception:
    _CORS_AVAILABLE = False

BASE_DIR = os.path.dirname(__file__)
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
ORGANIZED_DIR = os.path.join(BASE_DIR, 'organized_clippings')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if _CORS_AVAILABLE:
    CORS(app)
else:
    @app.after_request
    def _add_cors_headers(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        response.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS'
        return response


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'no file part'}), 400
    f = request.files['file']
    if f.filename == '':
        return jsonify({'error': 'empty filename'}), 400
    filename = secure_filename(f.filename)
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    f.save(save_path)
    return jsonify({'filename': filename})


@app.route('/organize', methods=['POST'])
def organize():
    data = request.get_json() or {}
    filename = data.get('filename')
    if not filename:
        return jsonify({'error': 'filename required'}), 400
    upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(upload_path):
        return jsonify({'error': 'uploaded file not found'}), 404
    try:
        import organize_clippings
        # The function writes files into organized_clippings directory
        organize_clippings.organize_clippings(input_file=upload_path, output_dir=ORGANIZED_DIR)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    # List generated .txt files in organized_clippings
    files = []
    if os.path.isdir(ORGANIZED_DIR):
        files = [f for f in os.listdir(ORGANIZED_DIR) if f.endswith('.txt')]
    return jsonify(files)


@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.get_json() or {}
    book_filename = data.get('book_filename')
    if not book_filename:
        return jsonify({'error': 'book_filename required'}), 400
    organized_path = os.path.join(ORGANIZED_DIR, book_filename)
    if not os.path.exists(organized_path):
        return jsonify({'error': 'organized file not found'}), 404
    try:
        import summarize_clippings
        # Read file content and pass to summarize_text
        with open(organized_path, 'r', encoding='utf-8') as f:
            content = f.read()
        # If summarize_clippings expects to call requests and Ollama, failures will raise
        summary = summarize_clippings.summarize_text(content)
        return jsonify({'summary': summary})
    except Exception as e:
        # Provide helpful 503 if external services missing
        msg = str(e)
        hint = 'Summarization depends on requests and an Ollama server. Ensure requests is installed and Ollama is running.'
        return make_response(jsonify({'error': msg, 'hint': hint}), 503)


if __name__ == '__main__':
    app.run(debug=True, port=5000)

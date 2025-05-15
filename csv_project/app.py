from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from dotenv import load_dotenv
from rag_service.data_loader import CSVDataLoader
from rag_service.vector_store import VectorStoreManager
from rag_service.rag_manager import RAGManager
import pandas as pd

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize services
data_loader = CSVDataLoader()
vector_store_manager = VectorStoreManager()
rag_manager = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    global rag_manager
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Process CSV with RAG service
        chunks = data_loader.load_and_split(filepath)
        vector_store = vector_store_manager.create_vector_store(chunks)
        rag_manager = RAGManager(vector_store_manager.get_retriever())
        
        # Get preview data
        df = pd.read_csv(filepath)
        preview_data = {
            'columns': df.columns.tolist(),
            'rows': df.head(5).fillna('').values.tolist()
        }
        
        return jsonify({
            'filename': filename,
            'rowCount': len(df),
            'columnCount': len(df.columns),
            'preview': preview_data,
            'message': 'CSV loaded successfully into RAG system'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/chat', methods=['POST'])
def chat():
    if not rag_manager:
        return jsonify({'error': 'No document loaded. Please upload a CSV first.'}), 400
    
    data = request.json
    question = data.get('message', '').strip()
    
    if not question:
        return jsonify({'error': 'Empty question'}), 400
    
    try:
        answer = rag_manager.query(question)
        return jsonify({
            'message': answer,
            'type': 'text'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
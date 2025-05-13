from flask import Flask, render_template, request, jsonify
from langchain_utils import generate_summary
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        transcript = request.form.get('transcript')
        if not transcript:
            return render_template('index.html', error="Please paste a session transcript.")
        
        summary = generate_summary(transcript)
        return render_template('index.html', summary=summary, transcript=transcript)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request
import time
import concurrent.futures
from extractor import extract_text_from_bytes

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    uploaded_files = request.files.getlist('files')

    if not uploaded_files or not uploaded_files[0].filename:
        return "Please select at least one PDF file to upload."

    pdf_data = []
    for file in uploaded_files:
        if file.filename.lower().endswith('.pdf'):
            pdf_data.append((file.filename, file.read()))

    if not pdf_data:
        return "No valid PDF files were uploaded."
    
    start_time = time.time()
    
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = list(executor.map(extract_text_from_bytes, pdf_data))

    end_time = time.time()
    duration = f"{end_time - start_time:.2f}"

    return render_template('results.html', results=results, duration=duration)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)

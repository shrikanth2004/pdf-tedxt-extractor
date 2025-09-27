import fitz

def extract_text_from_bytes(file_data):
    filename, file_bytes = file_data
    try:
        with fitz.open(stream=file_bytes, filetype="pdf") as pdf_document:
            full_text = ""
            for page in pdf_document:
                full_text += page.get_text()
        
        print(f"✅ Success: {filename}")
        return {"filename": filename, "text": full_text, "error": None}
        
    except Exception as e:
        error_message = f"Error processing PDF: {e}"
        print(f"❌ Failed: {filename} - {error_message}")
        return {"filename": filename, "text": None, "error": error_message}


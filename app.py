import streamlit as st
import time
import concurrent.futures
from extractor import extract_text_from_bytes

# --- Page Configuration ---
st.set_page_config(
    page_title="Parallel PDF Extractor",
    page_icon="🚀",
    layout="centered"
)

# --- Function to load and inject CSS ---
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Call the function to load the CSS
load_css("style.css")


# --- Main App UI ---
st.title("Parallel PDF Extractor")
st.markdown('<p class="form-description">Click to select files or drag and drop them into the box below.</p>', unsafe_allow_html=True)


# Use Streamlit's file uploader
uploaded_files = st.file_uploader(
    "Drag and drop your PDF files here",
    type="pdf",
    accept_multiple_files=True,
    label_visibility="collapsed" # Hides the default label
)

if uploaded_files:
    st.info(f"{len(uploaded_files)} file(s) selected. Click the button below to start extraction.")
    
    if st.button("Extract Text from PDFs"):
        pdf_data = []
        for file in uploaded_files:
            pdf_data.append((file.name, file.read()))

        start_time = time.time()
        
        with st.spinner("Extracting text... this may take a moment."):
            with concurrent.futures.ProcessPoolExecutor() as executor:
                results = list(executor.map(extract_text_from_bytes, pdf_data))

        end_time = time.time()
        duration = f"{end_time - start_time:.2f}"
        
        st.success(f"✅ Done! Processed {len(results)} files in {duration} seconds.")
        st.balloons()

        st.header("Extraction Results")
        for result in results:
            if result["text"]:
                st.subheader(f"📄 {result['filename']}")
                with st.expander("View Extracted Text"):
                    st.text_area("Text", result["text"], height=300, key=f"text_{result['filename']}")
            else:
                st.subheader(f"❌ {result['filename']}")
                st.error(f"Could not process file. Error: {result['error']}")
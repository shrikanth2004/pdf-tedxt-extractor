import streamlit as st
import time
import concurrent.futures
from extractor import extract_text_from_bytes

st.set_page_config(
    page_title="Parallel PDF Extractor",
    page_icon="🚀",
    layout="centered"
)

st.title("🚀 Parallel PDF Text Extractor")

st.markdown("""
This app uses parallel processing to extract text from multiple PDF files quickly. 
Upload your files below to get started.
""")

uploaded_files = st.file_uploader(
    "Drag and drop your PDF files here",
    type="pdf",
    accept_multiple_files=True
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
                    st.text_area("Text", result["text"], height=300, key=f"text_area_{result['filename']}")
            else:
                st.subheader(f"❌ {result['filename']}")
                st.error(f"Could not process file. Error: {result['error']}")

import streamlit as st
import re
import fitz  # PyMuPDF
 
# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text
 
# Function to extract fields from text
def extract_fields(text):
    # Sample regex patterns (you may need to fine-tune them based on your PDF structure)
    problem = re.search(r'Problem[:\-]\s*(.*)', text, re.IGNORECASE)
    reporter = re.search(r'Reported by[:\-]\s*(.*)', text, re.IGNORECASE)
    department = re.search(r'Department[:\-]\s*(.*)', text, re.IGNORECASE)
    date = re.search(r'Date[:\-]\s*(.*)', text, re.IGNORECASE)
    affected = re.search(r'Affected (?:Items|Component|Software)[s]*[:\-]\s*(.*)', text, re.IGNORECASE)
 
    return {
        "problem": problem.group(1).strip() if problem else "N/A",
        "reporter": reporter.group(1).strip() if reporter else "N/A",
        "department": department.group(1).strip() if department else "N/A",
        "date": date.group(1).strip() if date else "N/A",
        "affected": affected.group(1).strip() if affected else "N/A"
    }
 
# Streamlit app UI
st.title("Change Request Summarizer")
st.write("Upload a PDF file containing a change request to get a summary.")
 
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
 
if uploaded_file:
    with st.spinner("Extracting and summarizing..."):
        text = extract_text_from_pdf(uploaded_file)
        fields = extract_fields(text)
 
        summary = (
            f"This change request is due to **{fields['problem']}**, "
            f"reported by **{fields['reporter']}** from **{fields['department']}** on **{fields['date']}**. "
            f"It affects **{fields['affected']}**."
        )
 
        st.subheader("Summary")
        st.markdown(summary)
 
        # Optional: show extracted text for debugging
        with st.expander("Show extracted text"):
            st.text_area("Extracted Text", text, height=300)

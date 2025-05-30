
import streamlit as st
import fitz  # PyMuPDF
import re

def extract_info(text):
    # Define regex patterns to extract relevant information
    problem_pattern = re.compile(r'Problem:\s*(.*)')
    reporter_pattern = re.compile(r'Reporter:\s*(.*)')
    department_pattern = re.compile(r'Department:\s*(.*)')
    date_pattern = re.compile(r'Date:\s*(.*)')
    affected_pattern = re.compile(r'Affected Component, Items, Software\(s\):\s*(.*)')

    # Extract information using regex
    problem = re.search(problem_pattern, text).group(1) if re.search(problem_pattern, text) else "N/A"
    reporter = re.search(reporter_pattern, text).group(1) if re.search(reporter_pattern, text) else "N/A"
    department = re.search(department_pattern, text).group(1) if re.search(department_pattern, text) else "N/A"
    date = re.search(date_pattern, text).group(1) if re.search(date_pattern, text) else "N/A"
    affected = re.search(affected_pattern, text).group(1) if re.search(affected_pattern, text) else "N/A"

    return problem, reporter, department, date, affected

def summarize_change_request(problem, reporter, department, date, affected):
    return f"This change request is due to {problem}, reported by {reporter} from {department} on {date}. It affects {affected}."

def main():
    st.title("Change Request Summarizer")

    uploaded_file = st.file_uploader("Upload a PDF file containing the change request", type="pdf")

    if uploaded_file is not None:
        # Read the PDF file
        pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = ""
        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)
            text += page.get_text()

        # Extract information from the text
        problem, reporter, department, date, affected = extract_info(text)

        # Summarize the change request
        summary = summarize_change_request(problem, reporter, department, date, affected)

        # Display the summary
        st.write(summary)

if __name__ == "__main__":
    main()

Got it, just the Python code for the Streamlit app. Here it is:

Python

import streamlit as st
import PyPDF2
import io
import google.generativeai as genai
import os

# Configure Google Generative AI with your API key
# It's highly recommended to set your API key as an environment variable
# e#g., os.environ["GOOGLE_API_KEY"] = "YOUR_API_KEY"
# For Streamlit Cloud, set this as a 'secret' named GOOGLE_API_KEY
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

def extract_text_from_pdf(uploaded_file):
    """
    Extracts text from an uploaded PDF file.
    """
    if uploaded_file is not None:
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() if page.extract_text() else "" # Handle potentially empty pages
            return text
        except Exception as e:
            st.error(f"Error reading PDF: {e}")
            return None
    return None

def summarize_change_request(text_content):
    """
    Summarizes the change request using a generative AI model.
    """
    if not text_content or text_content.strip() == "":
        return "No substantial text content to summarize."

    # Define the prompt for the AI model
    prompt = f"""
    Analyze the following change request text and extract the key information to fit the following format:

    "This change request is due to [Problem], reported by [Reporter] from [Department] on [Date]. It affects [Affected Component, Items, Software(s)]."

    If a piece of information is not explicitly found in the text, use "N/A" for that specific field.
    Ensure the output strictly adheres to the requested format.

    Change Request Text:
    ---
    {text_content}
    ---

    Extracted Summary:
    """

    try:
        model = genai.GenerativeModel('gemini-pro') # Or 'gemini-1.5-flash' for faster, cheaper inference
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        st.error(f"Error generating summary: {e}")
        return "Could not generate summary. Please check your API key and try again."

# Set Streamlit page configuration
st.set_page_config(
    page_title="Change Request Summarizer",
    layout="centered",
    initial_sidebar_state="auto"
)

# --- Streamlit UI ---
st.title("📄 Change Request Summarizer")
st.markdown("Upload your change request PDF, and I'll summarize it for you using AI!")

# File uploader widget
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file is not None:
    st.success("PDF file uploaded successfully!")

    # Expandable section for extracted text preview
    with st.expander("Preview Extracted Text"):
        with st.spinner("Extracting text from PDF..."):
            pdf_text = extract_text_from_pdf(uploaded_file)

        if pdf_text:
            st.write(pdf_text[:1000] + "..." if len(pdf_text) > 1000 else pdf_text)
            if len(pdf_text) > 1000:
                st.info(f"Showing first 1000 characters. Total characters: {len(pdf_text)}")
        else:
            st.warning("Could not extract text from the PDF. The file might be scanned or corrupted.")

    if pdf_text and pdf_text.strip() != "":
        # Button to trigger summarization
        if st.button("Summarize Change Request", help="Click to analyze the PDF content and generate the summary."):
            with st.spinner("Summarizing change request using AI... This may take a moment."):
                summary = summarize_change_request(pdf_text)
                st.subheader("Summarized Change Request:")
                st.info(summary)
    elif uploaded_file is not None:
        st.warning("The uploaded PDF appears to have no readable text content.")
else:
    st.info("Please upload a PDF file to get started.")

st.markdown("""
---
### How it works:
1.  **Upload your PDF:** Select your change request document from your local machine.
2.  **Text Extraction:** The app uses `PyPDF2` to read the PDF and extract all text.
3.  **AI Summarization:** Google's Generative AI model (`gemini-pro`) then processes the extracted text.
4.  **Structured Output:** The AI is prompted to format the summary precisely, identifying the problem, reporter, department, date, and affected components.
""")

st.markdown(
    """
    <style>
    .stApp {
        background-color: #1a1a1a; /* Dark background */
        color: white;
    }
    .stTextInput>div>div>input {
        color: white;
    }
    .stTextArea>div>div>textarea {
        color: white;
    }
    .stButton>button {
        background-color: #4CAF50; /* Green button */
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stFileUploader>div>button {
        background-color: #2196F3; /* Blue upload button */
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
    }
    .stFileUploader>div>button:hover {
        background-color: #0b7dda;
    }
    .stCode {
        background-color: #333333;
        color: #f8f8f2;
        border-radius: 5px;
        padding: 10px;
    }
    .stInfo {
        background-color: #2e86de; /* A nice blue for info boxes */
        color: white;
        border-radius: 8px;
        padding: 15px;
        font-size: 1.1em;
    }
    .stWarning {
        background-color: #f39c12; /* Orange for warnings */
        color: white;
        border-radius: 8px;
        padding: 15px;
    }
    .stSuccess {
        background-color: #28a745; /* Green for success */
        color: white;
        border-radius: 8px;
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
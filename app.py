import streamlit as st
from google import genai
from pypdf import PdfReader

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

st.title("📄 Chat with your PDF")

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file:
    reader = PdfReader(uploaded_file)
    full_text = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
    st.success(f"PDF loaded! ({len(reader.pages)} pages)")

    question = st.text_input("Your question:")
    if question:
        with st.spinner("Thinking..."):
            prompt = f"Based on this document:\n\n{full_text[:15000]}\n\nAnswer this question: {question}"
            response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt
            )
        st.write("**Answer:**", response.text)
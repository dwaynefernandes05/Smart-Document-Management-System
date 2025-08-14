import streamlit as st
import os
from smartdocument import DocumentManager

st.set_page_config(page_title="📄 Smart Document Q&A", layout="wide")
st.title("📄 Smart Document System")
st.write("Upload documents to analyze, summarize, compare, and perform more tasks.")

dm = DocumentManager()

# ---- Dropdown Menu ----
mode = st.selectbox(
    "Select Action",
    [
        "📄 Upload & Ask Questions",
        "📝 Summarize Document",
        "🔍 Compare Documents",
        "🔑 Extract Keywords",
        "😊 Sentiment Analysis",
        "🌍 Translate Document"
    ]
)

# ---- Upload & Ask Questions ----
if mode == "📄 Upload & Ask Questions":
    uploaded_file = st.file_uploader("Upload a document", type=["pdf", "txt", "docx", "csv", "md", "xlsx"])
    if uploaded_file:
        os.makedirs("uploads", exist_ok=True)
        save_path = os.path.join("uploads", uploaded_file.name)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"✅ Saved file: {save_path}")
        st.success(dm.load_documents(save_path))

    question = st.text_input("Enter your question")
    if st.button("Get Answer") and question:
        answer = dm.ask_question(question)
        st.markdown(f"**Answer:** {answer}")

# ---- Summarize Document ----
elif mode == "📝 Summarize Document":
    uploaded_file = st.file_uploader("Upload a PDF,TXT or DOCX file for summarization", type=["pdf", "txt", "docx"])
    if uploaded_file:
        os.makedirs("uploads", exist_ok=True)
        save_path = os.path.join("uploads", uploaded_file.name)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(dm.load_documents(save_path))

        if st.button("Summarize"):
            summary = dm.ask_question("Summarize the document in detail.")
            st.markdown(f"**Summary:** {summary}")

# ---- Compare Documents ----
elif mode == "🔍 Compare Documents":
    if "dm1" not in st.session_state:
        st.session_state.dm1 = DocumentManager()
    if "dm2" not in st.session_state:
        st.session_state.dm2 = DocumentManager()

    file1 = st.file_uploader("Upload First Document", type=["pdf", "txt", "docx"], key="file1")
    if file1:
        path1 = os.path.join("uploads", file1.name)
        os.makedirs("uploads", exist_ok=True)
        with open(path1, "wb") as f:
            f.write(file1.getbuffer())
        result1 = st.session_state.dm1.load_documents(path1)
        st.success(f"✅ Loaded {file1.name}")
        if result1:
            st.info(result1)

    file2 = st.file_uploader("Upload Second Document", type=["pdf", "txt", "docx"], key="file2")
    if file2:
        path2 = os.path.join("uploads", file2.name)
        os.makedirs("uploads", exist_ok=True)
        with open(path2, "wb") as f:
            f.write(file2.getbuffer())
        result2 = st.session_state.dm2.load_documents(path2)
        st.success(f"✅ Loaded {file2.name}")
        if result2:
            st.info(result2)

    if st.button("Compare"):
        if getattr(st.session_state.dm1, "vector_store", None) and getattr(st.session_state.dm2, "vector_store", None):
            answer1 = st.session_state.dm1.ask_question("Summarize the document in detail.")
            answer2 = st.session_state.dm2.ask_question("Summarize the document in detail.")
            comparison_result = st.session_state.dm1.ask_question(
                f"Document 1 Summary: {answer1}\nDocument 2 Summary: {answer2}\nNow compare them in detail."
            )
            st.markdown(f"**Comparison:** {comparison_result}")
        else:
            st.error("❌ Please upload and load both documents before comparing.")

# ---- Extract Keywords ----
elif mode == "🔑 Extract Keywords":
    uploaded_file = st.file_uploader("Upload a PDF,TXT or DOCX file", type=["pdf", "txt", "docx"])
    if uploaded_file:
        os.makedirs("uploads", exist_ok=True)
        save_path = os.path.join("uploads", uploaded_file.name)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(dm.load_documents(save_path))

        if st.button("Extract Keywords"):
            keywords = dm.extract_keywords()
            st.markdown(f"**Keywords:** {keywords}")

# ---- Sentiment Analysis ----
elif mode == "😊 Sentiment Analysis":
    uploaded_file = st.file_uploader("Upload a PDF,TXT or DOCX file", type=["pdf", "txt", "docx"])
    if uploaded_file:
        os.makedirs("uploads", exist_ok=True)
        save_path = os.path.join("uploads", uploaded_file.name)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(dm.load_documents(save_path))

        if st.button("Analyze Sentiment"):
            sentiment = dm.sentiment_analysis()
            st.markdown(f"**Sentiment:** {sentiment}")

# ---- Translate Document ----
elif mode == "🌍 Translate Document":
    uploaded_file = st.file_uploader("Upload a PDF,TXT or DOCX file", type=["pdf", "txt", "docx"])
    if uploaded_file:
        os.makedirs("uploads", exist_ok=True)
        save_path = os.path.join("uploads", uploaded_file.name)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(dm.load_documents(save_path))

        target_language = st.text_input("Enter target language (e.g., French, Hindi, Spanish)")
        if st.button("Translate") and target_language:
            translation = dm.translate_text(target_language)
            st.markdown(f"**Translated Text ({target_language}):** {translation}")

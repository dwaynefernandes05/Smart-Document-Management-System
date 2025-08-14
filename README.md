# 📄 Smart Document System

---

A Streamlit-based AI-powered application that allows users to upload documents (PDF, TXT, MD, XLSX) and perform advanced analysis using **RAG (Retrieval-Augmented Generation)** with **Ollama LLaMA 3** and **Hugging Face embeddings**.

---

## 🚀 Features

- **Ask Questions** – Query your documents in natural language.
- **Summarization** – Generate detailed summaries of your documents.
- **Document Comparison** – Compare two documents and highlight key differences.
- **Keyword Extraction** – Identify the most important terms in your document.
- **Sentiment Analysis** – Detect the overall sentiment of the content.
- **Translation** – Translate document text into a target language of your choice.

---

## 🛠️ Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **LLM**: [Ollama](https://ollama.ai/) with `llama3:8b` model
- **Embeddings**: Hugging Face `sentence-transformers/all-MiniLM-L6-v2`
- **Vector Store**: FAISS
- **Document Parsing**: LangChain document loaders (PDF, TXT, MD, XLSX)

---

## 📂 Supported File Types

- PDF (`.pdf`)
- Text (`.txt`)
- Docx (`.docx`)
- Markdown (`.md`)
- Excel (`.xlsx`)
- Csv (`.csv`)

---

## 📦 Installation

### 1️⃣ Clone the repository
```bash
git clone https://github.com/yourusername/smart-document-system.git
cd smart-document-system
```

### 2️⃣ Create a virtual environment and activate it
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Install and run Ollama
- **Download Ollama:** https://ollama.ai/download
- **Pull the model:**
```bash
ollama pull llama3:8b

#OR

ollama pull mistra:7b
```

---

### ▶️ Usage
**Run the Streamlit app:**
```bash
streamlit run streamlit_app.py
```

**Upload a document and:**

- Ask questions

- Summarize it

- Compare with another document

- Extract keywords

- Analyze sentiment

- Translate to another language

---

### 📌 Example

**Question:**
"What is the main theme of this document?"

**Answer:**
"The document primarily discusses sustainable development practices in urban areas."

---

### 🤝 Contributing

Pull requests are welcome! If you have suggestions for new features or improvements, please open an issue.
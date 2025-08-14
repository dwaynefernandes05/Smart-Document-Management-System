from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM  # or from langchain_ollama import OllamaLLM if using the new package
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader, CSVLoader, UnstructuredMarkdownLoader, UnstructuredExcelLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA


class DocumentManager:
    def __init__(self):
        # Embeddings model (still HuggingFace, runs locally)
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.vector_store = None

        # LLaMA 3 via Ollama
        self.llm = OllamaLLM(model="mistral:7b")
        # You can change model name to any Ollama model you have pulled

    def load_documents(self, file_path):
        """Loads and processes the documents"""
        # Load specific type of documents
        if file_path.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        elif file_path.endswith(".txt"):
            loader = TextLoader(file_path, encoding="utf-8")
        elif file_path.endswith(".docx"):
            loader = Docx2txtLoader(file_path)
        elif file_path.endswith(".csv"):
            loader = CSVLoader(file_path)
        elif file_path.endswith(".md"):
            loader = UnstructuredMarkdownLoader(file_path)
        elif file_path.endswith(".xlsx") or file_path.endswith(".xls"):
            loader = UnstructuredExcelLoader(file_path)
        else:
            return f"❌ Unsupported file type: {file_path}"

        # Load and split
        documents = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        texts = splitter.split_documents(documents)

        # Create or update vector store
        if self.vector_store is None:
            self.vector_store = FAISS.from_documents(texts, self.embeddings)
        else:
            self.vector_store.add_documents(texts)

        return f"Document {file_path} loaded successfully!"

    def ask_question(self, question):
        """Ask a question about loaded documents"""
        if self.vector_store is None:
            return "No documents loaded yet!"

        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            retriever=self.vector_store.as_retriever()
        )
        return qa_chain.run(question)

    def summarise_document(self, file_path):
        """Generates summary for the document"""
        self.load_documents(file_path)

        summary_prompt = """
        Please provide a concise summary of the document, including:
        1. Main topics covered
        2. Key points
        3. Important conclusions
        """

        return self.ask_question(summary_prompt)

    def compare_documents(self, file1_path, file2_path):
        """Compares two documents"""
        self.load_documents(file1_path)
        doc1_summary = self.summarise_document(file1_path)

        self.load_documents(file2_path)
        doc2_summary = self.summarise_document(file2_path)

        compare_prompt = f"""
        Compare these documents:
        Document 1: {doc1_summary}
        Document 2: {doc2_summary}

        Please highlight:
        1. Common themes
        2. Key differences
        3. Unique points in each document
        """
        return self.ask_question(compare_prompt)

    def extract_keywords(self):         #extract key words from the document
        if self.vector_store is None:
            return "No documents loaded yet!"
        
        docs = self.vector_store.similarity_search("",k=2)
        full_text = " ".join([doc.page_content for doc in docs])

        prompt = f"Extract the top 10 most important keywords from the following text:\n\n{full_text}"
        return self.llm.invoke(prompt)
    
    def sentiment_analysis(self):         #performs sentiment analysis of the document
        if self.vector_store is None:
            return "No documents loaded yet!"
        
        docs = self.vector_store.similarity_search("",k=2)
        full_text = " ".join([doc.page_content for doc in docs])

        prompt = f"Analyze the overall sentiment of the following text and explain why:\n\n{full_text}"
        return self.llm.invoke(prompt)
    
    def translate_text(self,target_language):         #translates text in the document
        if self.vector_store is None:
            return "No documents loaded yet!"
        
        docs = self.vector_store.similarity_search("",k=2)
        full_text = " ".join([doc.page_content for doc in docs])

        prompt = f"Translate the following text to {target_language}:\n\n{full_text}"
        return self.llm.invoke(prompt)
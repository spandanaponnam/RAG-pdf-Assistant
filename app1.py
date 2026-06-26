import os
import tempfile
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import (
    GoogleGenerativeAIEmbeddings,
    ChatGoogleGenerativeAI
)
from langchain_qdrant import QdrantVectorStore
from langchain_classic.chains import RetrievalQA
# API Key
os.environ["GOOGLE_API_KEY"] = "YOUR_API_KEY"

# Gemini Embeddings
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001"
)
# Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)
st.title("📄 Chat With Your PDF")
uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)
if uploaded_file:
    # Save PDF temporarily
    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    ) as tmp_file:
        tmp_file.write(uploaded_file.read())
        pdf_path = tmp_file.name
    # Load PDF
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()
    print(pages[0].page_content)
    # Split
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(pages)
    st.success(f"Loaded {len(chunks)} chunks")
    # Store in Qdrant
    if "vector_store" not in st.session_state:
        st.session_state.vector_store = QdrantVectorStore.from_documents(
            documents=chunks,
            embedding=embeddings,
            url="http://localhost:6333",
            collection_name="user_pdf"
        )
    vector_store = st.session_state.vector_store
    retriever = vector_store.as_retriever(
        search_kwargs={"k": 2}
    )
    # QA Chain
    from langchain_core.prompts import PromptTemplate
    prompt = PromptTemplate(
        template="""
    Answer the question using the PDF context.
    If the user asks for a summary or description, summarize the PDF content.
    Context:
    {context}
    Question:
    {question}
    Answer:
    """,
        input_variables=["context", "question"]
    )
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt}
    )
    question = st.text_input(
        "Ask a question about the PDF"
    )
    if question:
        with st.spinner("Thinking..."):
            answer = qa_chain.invoke(
                {"query": question}
            )
        st.subheader("Answer")
        st.write(answer["result"])
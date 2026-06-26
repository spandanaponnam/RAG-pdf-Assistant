# 📄 RAG PDF Assistant

A simple AI-powered PDF chatbot that lets you upload a PDF and ask questions about its content.

This project uses **Retrieval-Augmented Generation (RAG)** to search the uploaded document and provide answers using Generative AI.

## 🚀 Features

- Upload PDF documents
- Extract text from PDF files
- Split documents into smaller chunks
- Create embeddings for document search
- Store vectors using Qdrant
- Ask questions about your PDF
- Generate answers using Google Gemini AI

## 🛠️ Tech Stack

- Python
- Streamlit
- LangChain
- Google Gemini API
- Qdrant Vector Database
- PyPDF Loader

## ⚙️ How It Works

1. User uploads a PDF
2. PDF text is extracted
3. Text is divided into smaller chunks
4. Chunks are converted into embeddings
5. Embeddings are stored in Qdrant
6. User asks a question
7. Relevant information is retrieved and Gemini generates the answer

## 📂 Project Structure

RAG-pdf-Assistant/
│
├── app1.py
├── requirements.txt
└── README.md


## ▶️ Run Locally

Clone the repository:

git clone https://github.com/spandanaponnam/RAG-pdf-Assistant.git

Go to project folder:

cd RAG-pdf-Assistant

Create virtual environment:

python -m venv venv

Activate environment (Windows):

venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Run the application:

streamlit run app1.py


## 💬 Example Questions

- Summarize this PDF
- Explain this document
- What are the main points?
- What skills are mentioned?


## 🔮 Future Improvements

- Support multiple PDFs
- Add chat history
- Improve response speed
- Deploy online
- Add user authentication


## 👨‍💻 Author

Created as a Gen AI project to explore PDF question answering using RAG, LangChain, Gemini, and Qdrant.

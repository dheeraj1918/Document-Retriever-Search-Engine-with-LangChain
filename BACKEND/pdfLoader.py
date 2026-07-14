from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from generateEmbeddings import generate_embedding
import pypdf
def pdf_loader(file_path):
    loader=PyPDFLoader(file_path)
    pdf_data=loader.load()
    text_splitter=RecursiveCharacterTextSplitter(chunk_size=400,chunk_overlap=20)
    documents=text_splitter.split_documents(pdf_data)
    return documents
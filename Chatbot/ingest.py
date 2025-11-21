from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import DirectoryLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


data = "Data/"
DB_FAISS_PATH = "vectorstores/db_faiss"

def create_vector_db():
    loader = DirectoryLoader(data, glob="*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()
    text_splitter=RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    text=text_splitter.split_documents(documents)

    embedding = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2', 
    model_kwargs = {'device':'cpu'})

    db = FAISS.from_documents(text, embedding)
    db.save_local(DB_FAISS_PATH)

if __name__ == '__main__':
    create_vector_db()

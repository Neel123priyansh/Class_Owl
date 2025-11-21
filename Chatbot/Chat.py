import os
import pathlib as Path
import logging
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import DirectoryLoader
from langchain_pinecone import PineconeVectorStore
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceBgeEmbeddings 
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
import os
from langchain_openai import OpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

PINE_CONE_API_KEY = 'pcsk_tvsrw_9SjMZqygLV7gYC7HZwFJsUf1u4jf6XMZfTELxdJQXXU2dpDRAcAWcd8e9NieQLp'
LLAMA_API_KEY = 'LA-d096dc5331c1440b9caebe7a16ba2e7e8515e963a9fa496fa45a293a81b43fd1'

def load_pdf_data(data):
    loader = DirectoryLoader(data, glob="*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()

    return documents

extracted_data = load_pdf_data(data='Data/')

def text_split(extracted_data):
    text_splitter=RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
    text_chunks=text_splitter.split_documents(extracted_data)
    return text_chunks
text_chunks=text_split(extracted_data)
# print("The length of text chunks", len(text_chunks))

def download_hugging_face_embedding():
    embedding = HuggingFaceBgeEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    return embedding 

embeddings = download_hugging_face_embedding()

pc = Pinecone(api_key=PINE_CONE_API_KEY)
index_name = "medchat-1"

os.environ["PINECONE_API_KEY"] = PINE_CONE_API_KEY

docsearch = PineconeVectorStore.from_documents(
    documents=text_chunks, index_name=index_name, embedding=embeddings,
)


retriever = docsearch.as_retriever(search_type='similarity', search_kwargs={"k":3})
retriever_docs = retriever.invoke("What is acne?")

llm = OpenAI(temperature=0.4, max_tokens=500)

system_prompt=(
    "You are an assistant for question-answering task."
    "Use the following pieces of retrieved context to answer"
    "the question. If you don't know the answer, say that you"
    "don't know. Use three senstences maximum to keep the "
    "answer concise."
    "\n\n"
    "{context}"
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),

    ]
)

question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

response = rag_chain.invoke({"input" : "What is Acne?"})
print(response["answer"])
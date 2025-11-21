import os
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import DirectoryLoader
from langchain_pinecone import PineconeVectorStore
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.llms import HuggingFacePipeline
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
import pinecone

# API Keys
PINE_CONE_API_KEY = 'pcsk_tvsrw_9SjMZqygLV7gYC7HZwFJsUf1u4jf6XMZfTELxdJQXXU2dpDRAcAWcd8e9NieQLp'

# Load PDF Data
def load_pdf_data(data):
    loader = DirectoryLoader(data, glob="*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()
    return documents

extracted_data = load_pdf_data(data='Data/')

# Split Text into Chunks
def text_split(extracted_data):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
    text_chunks = text_splitter.split_documents(extracted_data)
    return text_chunks

text_chunks = text_split(extracted_data)

# Load HuggingFace Embeddings
def download_hugging_face_embedding():
    embedding = HuggingFaceBgeEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    return embedding

embeddings = download_hugging_face_embedding()

# Initialize Pinecone Vector Store
pc = Pinecone(api_key=PINE_CONE_API_KEY)

index_name = "medchat-2"

# pc.create_index(
#     name=index_name,
#     dimension=384, # Replace with your model dimensions
#     metric="cosine", # Replace with your model metric
#     spec=ServerlessSpec(
#         cloud="aws",
#         region="us-east-1"
#     ) 
# )

os.environ["PINECONE_API_KEY"] = PINE_CONE_API_KEY


docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings,
)

# print(docsearch)

# # Create Retriever
retriever = docsearch.as_retriever(search_type='similarity', search_kwargs={"k": 3})

# Load Llama Model (HuggingFace)
def load_llama_model():
    model_name = "tiiuae/falcon-7b-instruct"  # Replace with your model
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        device_map="auto",  # Automatically places model on GPU if available
        torch_dtype="auto",  # Optimizes precision
    )
    generation_pipeline = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_length=512,
        temperature=0.7,
        top_p=0.9,
    )
    llm = HuggingFacePipeline(pipeline=generation_pipeline)
    return llm

llm = load_llama_model()

# Define System Prompt
system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you "
    "don't know. Use three sentences maximum to keep " 
    "the answer concise."
    "\n\n"
    "{context}"
)

# Create Prompt Template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

# Create Chains
question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

# Ask Question
response = rag_chain.invoke({"input": "What is Acne?"})
print(response["answer"])

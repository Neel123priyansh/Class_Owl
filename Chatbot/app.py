from flask import Flask, request, jsonify, render_template
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import CTransformers
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

app = Flask(__name__)

DB_FAISS_PATH = 'D:\\Orton\\Chatbot\\vectorstores\\db_faiss'

custom_prompt_template = """Use the following pieces of information to answer the user's question.
If you don't know the answer, just say that you don't know — don't make up an answer.

Context: {context}
Question: {question}

Helpful answer:
"""

def set_custom_prompt():
    return PromptTemplate(template=custom_prompt_template, input_variables=["context", "question"])

def load_llm():
    return CTransformers(
        model="TheBloke/Llama-2-7B-Chat-GGML",
        model_type="llama",
        max_new_tokens=512,
        temperature=0.7
    )

def qa_bot():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    db = FAISS.load_local(DB_FAISS_PATH, embeddings, allow_dangerous_deserialization=True)
    llm = load_llm()
    prompt = set_custom_prompt()

    # Build new chain structure
    doc_chain = create_stuff_documents_chain(llm, prompt)
    retrieval_chain = create_retrieval_chain(db.as_retriever(search_kwargs={"k": 2}), doc_chain)

    return retrieval_chain

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def handle_query():
    data = request.json
    query = data.get('query', '')

    if not query:
        return jsonify({'error': 'No query provided'}), 400

    qa_system = qa_bot()
    response = qa_system.invoke({"input": query})

    return jsonify({
        "answer": response["answer"],
        "context": [doc.page_content for doc in response["context"]],
    })

if __name__ == '__main__':
    app.run(debug=True)

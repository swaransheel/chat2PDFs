import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

st.markdown(
    """
    <style>
    .user-message {
        text-align: right;
        padding: 15px;
        margin: 5px;
        background-color: #e9fff3;
        border-radius: 10px;
        color: #000000; 
    }
    .assistant-message {
        text-align: left; 
        padding: 15px;
        margin: 5px;
        background-color: #fffde7;
        border-radius: 10px;
        color: #795548;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")
    return vector_store

def get_conversational_chain():
    prompt_template = """
    You are a knowledgeable assistant tasked with providing accurate and detailed answers based on the context provided. Please adhere to the following guidelines when formulating your response:

    1. **Clarity**: Ensure your answer is clear and easy to understand, using simple language where possible.
    2. **Detail**: Provide a comprehensive answer that includes all relevant information from the context.
    3. **Relevance**: Stick to the context provided. If the answer is not found within the context, state explicitly that the information is not available. Do not make assumptions or guesses.

    **Response Format:**
    - Use bold for major points.
    - Use bullet points or numbered lists for clarity.
    - Clearly separate different sections.

    **Context:**
    {context}

    **Question:**
    {question}

    **Response:**
    """
    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    
    return chain

def format_response(message):
    """
    Format the AI's response to enhance readability and presentation.
    """
    formatted_response = message.replace("\n", "<br>")
    
    lines = formatted_response.splitlines()
    formatted_lines = []
    for line in lines:
        if line.strip().startswith("- "):
            formatted_lines.append(f"<li>{line[2:]}</li>")
        else:
            formatted_lines.append(line)
    
    formatted_response = "<ul>" + "".join(formatted_lines) + "</ul>"
    
    formatted_response = formatted_response.replace("**", "<strong>").replace("__", "<strong>")
    formatted_response = formatted_response.replace("*", "<em>").replace("_", "<em>")
    
    formatted_response = formatted_response.replace("<ul></ul>", "")
    formatted_response = ' '.join(formatted_response.split())

    return formatted_response

def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    
    try:
        new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    except Exception as e:
        st.error(f"Error loading vector store: {e}")
        return

    docs = new_db.similarity_search(user_question)

    if not docs:
        st.warning("No relevant documents found.")
        return

    chain = get_conversational_chain()
    
    response = chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)
    
    answer = response.get("output_text", "Answer not found.")
    st.session_state.chat_history.append(("Assistant", answer))
    st.session_state.chat_history.append(("User", user_question))
    
    
    
def main():
    st.header("Smart PDF Assistant: Ask Questions, Get Answers!")
    st.write("This is a conversational AI assistant that can answer questions about a PDF document.")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    with st.form(key='question_form'):
        user_question = st.text_input("Ask Anything About the Content of Your PDFs")
        submit_button = st.form_submit_button(label='Submit')

    if submit_button and user_question:
        with st.spinner("Thinking..."):
            user_input(user_question)
        st.rerun() 

    for role, message in reversed(st.session_state.chat_history):
        if role == "Assistant":
            formatted_response = format_response(message)
            st.markdown(f"<div class='assistant-message'>{formatted_response}</div>", unsafe_allow_html=True)
            
        else:
            
            st.markdown(f"<div class='user-message'>{message}</div>", unsafe_allow_html=True)

    with st.sidebar:
        st.title("Upload & Manage PDFs")
        pdf_docs = st.file_uploader("Drag & Drop or Browse PDF Files, then Click Submit", accept_multiple_files=True)
        if st.button("Start Analysis"):
            with st.spinner("Analyzing your PDFs..."):
                raw_text = get_pdf_text(pdf_docs)
                if raw_text.strip(): 
                    text_chunks = get_text_chunks(raw_text)
                    vectorstore = get_vector_store(text_chunks)
                    st.success("Done")
                else:
                    st.error("No text extracted from the PDF files.")
    st.write("---")
    if st.button("Clear Conversation"):
        st.session_state.chat_history = [] 
        st.rerun()  
if __name__ == "__main__":
    main()
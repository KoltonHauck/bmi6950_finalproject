import os
import streamlit as st

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFDirectoryLoader

from langchain_openai import ChatOpenAI

### helper functions to retrieving patient options and knowledge bases options ###
def get_patient_list(patient_path="files/patients/"):
    return os.listdir(patient_path)
def get_knowledge_base_list(kb_path="files/knowledge_bases/"):
    return os.listdir(kb_path)
def get_file_list(kb_path="files/knowledge_bases/", kb_selection="cardiovascular"):
    if kb_selection:
        return os.listdir(kb_path + kb_selection)
    else:
        return "no knowledge base selected"
    
### retriever related functions ###
def get_retrievers(patient_selection, knowledge_base_selections):
    retrievers = []

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=64)

    embeddings = HuggingFaceEmbeddings(
        model_name="thenlper/gte-large",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )

    if patient_selection:
        patient_loader = PyPDFDirectoryLoader(f"files/patients/{patient_selection}/")
        documents = patient_loader.load()
        texts = text_splitter.split_documents(documents)
        pat_db = FAISS.from_documents(texts, embeddings)
        retrievers.append({
            "name": "Patient Chart",
            "description": "Good for answering questions about patient-specific data",
            "retriever": pat_db.as_retriever()
        })
    if knowledge_base_selections:
        kb_loaders = [PyPDFDirectoryLoader(f"files/knowledge_bases/{kb}/") for kb in knowledge_base_selections]
        documents_s = [kb_loader.load() for kb_loader in kb_loaders]
        texts_s = [text_splitter.split_documents(document) for document in documents_s]
        texts = [text for _ in texts_s for text in _]
        kb_db = FAISS.from_documents(texts, embeddings)
        retrievers.append({
            "name": "Knowledge Base",
            "description": "Cardiovascular guidelines",
            "retriever": kb_db.as_retriever()
        })

    if len(retrievers) == 0:
        return None
    
    return retrievers
def set_retriever_session_state(patient_selection, knowledge_base_selections):
    if "retriever" not in st.session_state:
        st.session_state["retrievers"] = get_retrievers(patient_selection, knowledge_base_selections)
    else:
        st.session_state["retrievers"] = get_retrievers(patient_selection, knowledge_base_selections)

### get the chat model ###
def get_llm(model_selected, openai_api_key):
    client = ChatOpenAI(model_name=model_selected,
                        temperature=1.0,
                        openai_api_key=openai_api_key)
    
    return client

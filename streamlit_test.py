import os
import streamlit as st

#from app_utils import *

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFDirectoryLoader, PyPDFLoader
from langchain.chains import MultiRetrievalQAChain

from langchain_openai import ChatOpenAI

from langchain.callbacks.base import BaseCallbackHandler
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

from langchain.schema import ChatMessage
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
def get_retrievers(patient_selection, kb, file_selection):
    update_info("retrieving retrievers...")
    retrievers = []

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=64)

    embeddings = HuggingFaceEmbeddings(
        model_name="thenlper/gte-large",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )

    ### patient was selected ###
    if patient_selection:
        update_info(f"getting {patient_selection} retrievers from files/patients/{patient_selection}/")
        patient_loader = PyPDFDirectoryLoader(f"files/patients/{patient_selection}/")
        documents = patient_loader.load()
        texts = text_splitter.split_documents(documents)
        pat_db = FAISS.from_documents(texts, embeddings)
        retrievers.append({
            "name": "Patient Chart",
            "description": "Good for answering questions about patient-specific data",
            "retriever": pat_db.as_retriever()
        })
        update_info("patient retriever loaded")

    ### whole knowledge base ###
    if kb and not file_selection:
        update_info(f"getting {kb} retrievers from files/knowledge_bases/{kb}/*")
        kb_loader = PyPDFDirectoryLoader(f"files/knowledge_bases/{kb}/")
        documents = kb_loader.load()
        texts = text_splitter.split_documents(documents)
        kb_db = FAISS.from_documents(texts, embeddings)
        retrievers.append({
            "name": f"{kb} knowledge base",
            "description": f"{kb} guidelines",
            "retriever": kb_db.as_retriever()
        })
        update_info(f"{kb} retriever loaded")
    ### specific files from knowledge base ###
    elif kb and file_selection:
        update_info(f"getting {kb} retrievers from files/knowledge_bases/{kb}/{file_selection}")
        kb_files_loaders = [PyPDFLoader(f"files/knowledge_bases/{kb}/{file}") for file in file_selection]
        documents_s = [kb_loader.load() for kb_loader in kb_files_loaders]
        texts_s = [text_splitter.split_documents(document) for document in documents_s]
        texts = [text for _ in texts_s for text in _]
        kb_db = FAISS.from_documents(texts, embeddings)
        retrievers.append({
            "name": f"{kb} knowledge base",
            "description": f"{kb} guidelines",
            "retriever": kb_db.as_retriever()
        })
        update_info(f"{kb} retriever loaded")

    if len(retrievers) == 0:
        return None
    
    return retrievers
def set_retriever_session_state(patient_selection, kb, file_selection):
    if "retriever" not in st.session_state:
        st.session_state["retrievers"] = get_retrievers(patient_selection, kb, file_selection)
    else:
        st.session_state["retrievers"] = get_retrievers(patient_selection, kb, file_selection)

### get the chat model ###
def get_llm(model_selected, openai_api_key):
    stream_handler = StreamHandler(st.empty())
    client = ChatOpenAI(model_name=model_selected,
                        temperature=0.5,
                        openai_api_key=openai_api_key,
                        streaming=False,
                        callbacks=[stream_handler])
    
    return client

info = st.info("INFO: <- Open side bar to enter credentials <-".upper())

### update info text box ###
def update_info(new_info):
    info.info("INFO: " + new_info.upper())

### class to handle streaming chat output to streamlit app
class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)

### get init messages ###
def get_init_messages():
    return ChatMessage(role="assistant", content="How can I help you?")

### clear button function to clear messages ###
def initialize_messages():
    st.session_state["messages"] = [get_init_messages()]

### sidebar ###
with st.sidebar:
    ### openai api key ###
    openai_api_key = st.text_input("OPENAI_API_KEY", type="password")
    if not (openai_api_key.startswith("sk-") and len(openai_api_key)==51):
        st.warning("Please enter your credentials!", icon="⚠")
    else:
        update_info("key entered, proceed to prompting!")
        st.success("Proceed to entering your prompt message!", icon="👉")

    st.divider()

    ### model and parameter selection ###
    st.subheader("Model Selection")
    model_selected = st.sidebar.selectbox("Choose a Model:", ["gpt-3.5-turbo", "gpt-4-turbo-preview"])

    st.divider()

    ### RAG sources selections ###
    st.subheader("VDB Selections")
    patient_selection = st.selectbox("Select patient:", [None] + get_patient_list())

    knowledge_base_selection = st.selectbox("Select knowledge base:", [None] + get_knowledge_base_list())

    file_selection = st.multiselect(
        "Select files to load",
        get_file_list(),
        disabled = not knowledge_base_selection
    )

    #knowledge_base_selection = st.multiselect(
    #    "Select knowledge bases",
    #    get_knowledge_base_list()
    #)

    #st.button("Create VDB", on_click=set_retriever_session_state()) #patient_selection, knowledge_base_selection))
    if st.button("Create VDB"):
        st.session_state["info"] = "test"
        update_info("creating vdb...")
        set_retriever_session_state(patient_selection, knowledge_base_selection, file_selection)
        update_info("created vdb")

    st.divider()

    ### clear chat history button ###
    st.button("Clear Chat History", on_click=initialize_messages)

### init initial messages ###
if "messages" not in st.session_state:
    st.session_state["messages"] = [get_init_messages()]

### write messages ###
for msg in st.session_state.messages:
    st.chat_message(msg.role).write(msg.content)

### chat input ###
if prompt := st.chat_input():
    st.session_state.messages.append(ChatMessage(role="user", content=prompt))
    st.chat_message("user").write(prompt)

    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    with st.chat_message("assistant"):
        llm = get_llm(openai_api_key=openai_api_key, model_selected=model_selected)

        with st.spinner():
            if st.session_state.get("retrievers", None):
                update_info("prompting multiretrievalqachain")
                qa = MultiRetrievalQAChain.from_retrievers(
                    llm=llm,
                    retriever_infos=st.session_state.retrievers,
                    callbacks=[]
                )
                
                response = qa.invoke(st.session_state.messages)
                st.session_state.messages.append(ChatMessage(role="assistant", content=response["result"]))

                #st.rerun()
                #stream = response["result"]
            else:
                update_info("prompting base model")
                response = llm.invoke(st.session_state.messages)
                stream = response.content
                st.session_state.messages.append(ChatMessage(role="assistant", content=response.content))

        st.rerun()

        #update_info(" ".join([f"{message.role}: {message.content}//" for message in st.session_state.messages]))
        #st.session_state.messages.append(ChatMessage(role="assistant", content=stream))

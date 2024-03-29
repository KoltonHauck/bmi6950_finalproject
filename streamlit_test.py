import os
import streamlit as st

from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFDirectoryLoader, PyPDFLoader, TextLoader
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
    st.toast("retrieving retrievers...")
    retrievers = []

    text_splitter = CharacterTextSplitter() #RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=64)

    embeddings = HuggingFaceEmbeddings(
        model_name="thenlper/gte-large",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )

    ### patient was selected ###
    if patient_selection:
        st.toast(f"getting {patient_selection} retrievers from files/patients/{patient_selection}/")
        patient_loader = PyPDFDirectoryLoader(f"files/patients/{patient_selection}/")
        documents = patient_loader.load()
        texts = text_splitter.split_documents(documents)
        pat_db = FAISS.from_documents(texts, embeddings)
        retrievers.append({
            "name": "Patient Chart",
            "description": "Good for answering questions about patient-specific data",
            "retriever": pat_db.as_retriever()
        })
        st.toast("patient retriever loaded")

    ### whole knowledge base ###
    if kb and not file_selection:
        st.toast(f"getting {kb} retrievers from files/knowledge_bases/{kb}/*")
        kb_loader = PyPDFDirectoryLoader(f"files/knowledge_bases/{kb}/")
        documents = kb_loader.load()
        texts = text_splitter.split_documents(documents)
        kb_db = FAISS.from_documents(texts, embeddings)
        retrievers.append({
            "name": f"{kb} knowledge base",
            "description": f"{kb} guidelines",
            "retriever": kb_db.as_retriever()
        })
        st.toast(f"{kb} retriever loaded")
    ### specific files from knowledge base ###
    elif kb and file_selection:
        st.toast(f"getting {kb} retrievers from files/knowledge_bases/{kb}/{file_selection}")
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
        st.toast(f"{kb} retriever loaded")

    if len(retrievers) == 0:
        return None
    
    return retrievers

@st.cache_resource
def get_huggingface_embeddings():
    embeddings = HuggingFaceEmbeddings(
        model_name="thenlper/gte-large",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )
    return embeddings

### function to get kb retriever for vdb ###
@st.cache_resource
def get_kb_retriever(kb, file_selection):
    text_splitter = CharacterTextSplitter() #RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=64)

    #embeddings = HuggingFaceEmbeddings(
    #    model_name="thenlper/gte-large",
    #    model_kwargs={"device": "cpu"},
    #    encode_kwargs={"normalize_embeddings": True}
    #)

        ### whole knowledge base ###
    if kb and not file_selection:
        #st.toast(f"getting {kb} retrievers from files/knowledge_bases/{kb}/*")
        kb_loader = PyPDFDirectoryLoader(f"files/knowledge_bases/{kb}/")
        documents = kb_loader.load()
        texts = text_splitter.split_documents(documents)
        kb_db = FAISS.from_documents(texts, get_huggingface_embeddings())
        return {
            "name": f"{kb} knowledge base",
            "description": f"{kb} guidelines",
            "retriever": kb_db.as_retriever()
        }
    ### specific files from knowledge base ###
    elif kb and file_selection:
        #st.toast(f"getting {kb} retrievers from files/knowledge_bases/{kb}/{file_selection}")
        kb_files_loaders = [PyPDFLoader(f"files/knowledge_bases/{kb}/{file}") for file in file_selection]
        documents_s = [kb_loader.load() for kb_loader in kb_files_loaders]
        texts_s = [text_splitter.split_documents(document) for document in documents_s]
        texts = [text for _ in texts_s for text in _]

        kb_db = FAISS.from_documents(texts, get_huggingface_embeddings())
        return {
            "name": f"{kb} knowledge base",
            "description": f"{kb} guidelines",
            "retriever": kb_db.as_retriever()
        }

### function to get the patient retriever for vdb ###
@st.cache_resource
def get_patient_retriever(patient_selection):
    text_splitter = CharacterTextSplitter() #RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=64) f

    #embeddings = HuggingFaceEmbeddings(
    #    model_name="thenlper/gte-large",
    #    model_kwargs={"device": "cpu"},
    #    encode_kwargs={"normalize_embeddings": True}
    #)

    #st.toast(f"getting {patient_selection} retrievers from files/patients/{patient_selection}/")
    patient_loader = PyPDFDirectoryLoader(f"files/patients/{patient_selection}/")
    documents = patient_loader.load()
    texts = text_splitter.split_documents(documents)
    pat_db = FAISS.from_documents(texts, get_huggingface_embeddings())
    return {
        "name": "Patient Chart",
        "description": "Good for answering questions about patient-specific data",
        "retriever": pat_db.as_retriever()
    }

def set_retriever_session_state(patient_selection, kb, file_selection):
    #if "retrievers" in st.session_state:
    #    st.toast("del old retrievers")
    #    del st.session_state.retrievers
    #st.session_state["retrievers"] = get_retrievers(patient_selection, kb, file_selection)

    retrievers = []
    if patient_selection:
        retrievers.append(get_patient_retriever(patient_selection))
        st.toast("patient retriever loaded")
    if kb:
        retrievers.append(get_kb_retriever(kb, file_selection))
        st.toast(f"{kb} retriever loaded")

    if not kb and not patient_selection:
        retrievers = None

    st.session_state["retrievers"] = retrievers

### get the chat model ###
def get_llm(model_selected):
    stream_handler = StreamHandler(st.empty())
    client = ChatOpenAI(model_name=model_selected,
                        temperature=0.5,
                        openai_api_key=os.environ.get("OPENAI_API_KEY"),
                        streaming=False,
                        callbacks=[stream_handler])
    
    return client

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
        os.environ["OPENAI_API_KEY"] = openai_api_key
        st.success("Proceed to entering your prompt message!", icon="👉")

    st.divider()

    ### model and parameter selection ###
    st.subheader("Model Selection")
    model_selected = st.sidebar.selectbox("Choose a Model:", ["gpt-3.5-turbo", "gpt-4-turbo-preview"])

    st.divider()

    ### RAG sources selections ###
    st.subheader("VDB Selections")
    patient_selection = st.selectbox("Select patient:", [None] + get_patient_list())

    ### General KB selection ###
    knowledge_base_selection = st.selectbox("Select knowledge base:", [None] + get_knowledge_base_list())

    ### Specific file selection ###
    file_selection = st.multiselect(
        "Select files to load",
        get_file_list(),
        disabled = not knowledge_base_selection
    )

    #st.button("Create VDB", on_click=set_retriever_session_state()) #patient_selection, knowledge_base_selection))
    if st.button("Create VDB"):
        st.session_state["info"] = "test"
        st.toast("creating vdb...")
        set_retriever_session_state(patient_selection, knowledge_base_selection, file_selection)
        st.toast("created vdb")

    st.divider()

    ### clear chat history button ###
    st.button("Clear Chat History", on_click=initialize_messages)

### init initial messages ###
if "messages" not in st.session_state:
    st.session_state["messages"] = [get_init_messages()]

### write messages ###
for msg in st.session_state.messages:
    st.chat_message(msg.role).write(msg.content)

### suggestion to enter api key
if not openai_api_key:
    st.toast("<- Open side bar to enter credentials <-")

### chat input ###
if prompt := st.chat_input(disabled= not openai_api_key):
    st.session_state.messages.append(ChatMessage(role="user", content=prompt))
    st.chat_message("user").write(prompt)

    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    with st.chat_message("assistant"):
        #llm = get_llm(openai_api_key=openai_api_key, model_selected=model_selected)

        with st.spinner():
            if st.session_state.get("retrievers", None):
                st.toast("prompting multiretrievalqachain")
                qa = MultiRetrievalQAChain.from_retrievers(
                    llm=get_llm(model_selected=model_selected),
                    retriever_infos=st.session_state["retrievers"])
                
                response = qa.invoke(st.session_state.messages)
                st.session_state.messages.append(ChatMessage(role="assistant", content=response["result"]))

            else:
                st.toast("prompting base model")
                response = get_llm(model_selected=model_selected).invoke(st.session_state.messages)
                stream = response.content
                st.session_state.messages.append(ChatMessage(role="assistant", content=response.content))

        st.rerun()

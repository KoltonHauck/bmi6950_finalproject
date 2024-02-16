# https://docs.streamlit.io/knowledge-base/tutorials/build-conversational-apps

import streamlit as st

# langchain
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate
)
from langchain.chains import ConversationalRetrievalChain
from langchain.chains import MultiRetrievalQAChain

# streaming
from langchain_community.callbacks import StreamlitCallbackHandler

# RAG
from langchain_community.document_loaders import PyPDFDirectoryLoader # or use Unstructured - UnstructuredPDFLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# os
import os

# convert st messages list to langchain message type
def st_messages_to_lc_messages(st_messages):
    lc_messages = []
    for message in st_messages:
        if message["role"] == "user":
            lc_messages.append(
                HumanMessage(content=message["content"])
            )
        elif message["role"] == "assistant":
            lc_messages.append(
                AIMessage(content=message["content"])
            )
        elif message["role"] == "system":
            lc_messages.append(
                SystemMessage(content=message["content"])
            )

    return lc_messages

# get openai chat client
def get_llm():
    client = ChatOpenAI(model_name=model_selected,
                        temperature=1.0,
                        openai_api_key=openai_api_key)
    
    return client

# load faiss db from pdf dir
def get_vdb_from_pdfs():
    loader = PyPDFDirectoryLoader("files/pdf/")
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=64)
    texts = text_splitter.split_documents(docs)

    embeddings = HuggingFaceEmbeddings(
        model_name="thenlper/gte-large",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )

    db = FAISS.from_documents(texts, embeddings)

    return db.as_retriever(search_type="similarity", search_kwargs={"k":2})

def initialize_messages():
    st.session_state.messages = [{"role": "assistant", "content": "How may I help you?"}]

def get_vdb():
    st.text(f"entering get_vdb\npatient sel: {patient_selection}\nkb sel: {knowledge_base_selections}")
    ### loaders ###
    loaders = []
    # patient list
    if patient_selection:
        st.text("entering patient sel")
        #patient_path = os.path.join("files/patient/", patient_selection)
        patient_path = f"files/patients/{patient_selection}/"
        st.text(f"patient path: {patient_path}")
        loaders.append(PyPDFDirectoryLoader(patient_path))
    # knowledge bases
    if knowledge_base_selections:
        st.text("entering kb sel")
        #kb_paths = [os.path.join("files/knowledge_bases/", kb) for kb in knowledge_base_selections]
        kb_paths = [f"files/knowledge_bases/{kb}" for kb in knowledge_base_selections]
        st.text(f"kb path: {kb_paths}")
        loaders += [PyPDFDirectoryLoader(kb_path) for kb_path in kb_paths]

    st.text(f"loaders length: {len(loaders)}")
    st.text(loaders)
    # if no loaders
    if len(loaders) == 0:
        st.text("\treturning None")
        return None

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=64)
    embeddings = HuggingFaceEmbeddings(
        model_name="thenlper/gte-large",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )

    st.text("test 1")
    index = VectorstoreIndexCreator(
        vectorstore_cls=FAISS,
        embedding=embeddings,
        text_splitter=text_splitter
    ).from_loaders(loaders)

    return index #.as_retriever(search_type="similarity", search_kwargs={"k":2})

def get_retrievers():
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
            "name": "Patient Chart",
            "description": "Good for answering questions about patient-specific data",
            "retriever": kb_db.as_retriever()
        })

    st.text(len(retrievers))
    st.text(patient_selection)
    st.text(knowledge_base_selections)

    if len(retrievers) == 0:
        return None
    
    return retrievers

def set_retriever_session_state():
    if "retriever" not in st.session_state:
        st.session_state["retrievers"] = get_retrievers()
    else:
        st.session_state["retrievers"] = get_retrievers()

def get_patient_list(patient_path="files/patients/"):
    return os.listdir(patient_path)

def get_knowledge_base_list(kb_path="files/knowledge_bases/"):
    return os.listdir(kb_path)

st.title("ChatGPT-like clone")


if "messages" not in st.session_state:
    initialize_messages() 

with st.sidebar:
    ### openai api key ###
    openai_api_key = st.text_input("OPENAI_API_KEY", type="password")
    if not (openai_api_key.startswith("sk-") and len(openai_api_key)==51):
        st.warning("Please enter your credentials!", icon="⚠")
    else:
        st.success("Proceed to entering your prompt message!", icon="👉")

    st.divider()

    ### model and parameter selection ###
    st.subheader("Model Selection")
    model_selected = st.sidebar.selectbox("Choose a Model:", ["gpt-3.5-turbo", "gpt-4-turbo-preview"])

    st.divider()

    ### RAG sources selections
    st.subheader("VDB Selection")
    patient_selection = st.selectbox("Select a patient:", [None] + get_patient_list())

    knowledge_base_selections = st.multiselect(
        "Select your knowledge bases",
        get_knowledge_base_list()
    )

    st.button("Confirm Selections", on_click=set_retriever_session_state)

    st.divider()

    ### clear chat history button ###
    st.button("Clear Chat History", on_click=initialize_messages())

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        #chat_window.markdown(message["content"])

if prompt := st.chat_input("What is up?", disabled=not openai_api_key):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

if st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant"):
        #with st.spinner("Thinking..."):
        #    response = generate_response()

        #if not openai_api_key.startswith('sk-'):
        #    st.warning('Please enter your OpenAI API key!', icon='⚠')

        #qa = ConversationalRetrievalChain.from_llm(get_client(), get_vdb_from_pdfs())
        #stream = qa({"question": prompt, "chat_history": st.session_state.messages[:-1]})

        llm = get_llm()
        if st.session_state.retriever:
            qa = MultiRetrievalQAChain(
                llm=llm,
                retriever_infos=st.session_state.retriever
            )
            response = qa.invoke(st_messages_to_lc_messages(st.session_state.messages))
            stream = response["result"]
        else:
            response = llm.invoke(st_messages_to_lc_messages(st.session_state.messages))
            stream = response.content
        
        st.write(stream)
        st.session_state.messages.append({"role": "assistant", "content": stream})

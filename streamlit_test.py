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

# streaming
from langchain_community.callbacks import StreamlitCallbackHandler

# RAG
from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

st.title("ChatGPT-like clone")

openai_api_key = st.sidebar.text_input('OpenAI API Key', type='password')

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
def get_client():
    client = ChatOpenAI(model_name="gpt-3.5-turbo",
                        temperature=1.0,
                        openai_api_key=openai_api_key,)
    
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

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if not openai_api_key.startswith('sk-'):
            st.warning('Please enter your OpenAI API key!', icon='⚠')

        qa = ConversationalRetrievalChain.from_llm(get_client(), get_vdb_from_pdfs())
        stream = qa({"question": prompt, "chat_history": st.session_state.messages[:-1]})

        #stream = get_client()(
        #    model=st.session_state["openai_model"],
        #    messages = st_messages_to_lc_messages(st.session_state.messages),
        #)    
        
        st.write(stream.content)

        st.session_state.messages.append({"role": "assistant", "content": stream.content})

from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import ChatMessage
from langchain_openai import ChatOpenAI
import streamlit as st

from app_utils import *

st.session_state["info"] = "Open side bar to enter credentials <-"
info = st.info(st.session_state["info"])

### update info text box ###
def update_info(new_info):
    info.info(new_info)

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
        set_retriever_session_state(patient_selection, knowledge_base_selection)
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
        stream_handler = StreamHandler(st.empty())
        llm = ChatOpenAI(openai_api_key=openai_api_key, streaming=True, callbacks=[stream_handler])
        response = llm.invoke(st.session_state.messages)
        st.session_state.messages.append(ChatMessage(role="assistant", content=response.content))
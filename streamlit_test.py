# https://docs.streamlit.io/knowledge-base/tutorials/build-conversational-apps

import streamlit as st
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate
)

from langchain.schema import HumanMessage, SystemMessage, AIMessage

st.title("ChatGPT-like clone")

openai_api_key = st.sidebar.text_input('OpenAI API Key', type='password')

def st_messages_to_lc_messages(st_messages):
    lc_messages = []
    for message in st_messages:
        try:
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
        except:
            st.write(f"Current message failed: {message}")
            st.write(f"message history: {st_messages}")
    return lc_messages


def get_client():
    client = ChatOpenAI(model_name="gpt-3.5-turbo",
                        temperature=1.0,
                        openai_api_key=openai_api_key)
    
    return client


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

        #stream = get_client().chat.completions.create(
        #stream = get_client()(
        #    model=st.session_state["openai_model"],
        #    messages=[
        #        {"role": m["role"], "content": m["content"]}
        #        for m in st.session_state.messages
        #    ],
        #    stream=True,
        #)

        stream = get_client()(
            model=st.session_state["openai_model"],
            messages = st_messages_to_lc_messages(st.session_state.messages[:-1]),
            stream=True
        )    
        
        try:
            response = st.write_stream(stream.content)
        except:
            response = st.write(stream.content)

    st.write(f"response....{response}")
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.write("----- Message History -----")
    st.write(st.session_state.messages)

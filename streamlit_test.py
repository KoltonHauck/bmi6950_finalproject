# https://docs.streamlit.io/knowledge-base/tutorials/build-conversational-apps

import streamlit as st
from langchain.chat_models import ChatOpenAI

st.title("ChatGPT-like clone")

openai_api_key = st.sidebar.text_input('OpenAI API Key', type='password')

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

        client = get_client()

        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
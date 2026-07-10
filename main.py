import streamlit as st
from chatbot import Groq

llm=Groq()

if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])




if prompt :=st.chat_input("Say something.."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    msg=llm.Create_prompt(prompt, st.session_state.messages)
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"): 
        response=st.write_stream(llm.model.stream(msg))
    st.session_state.messages.append({"role": "assistant", "content": response})

    


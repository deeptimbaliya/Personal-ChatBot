import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

st.set_page_config(page_title="LangChain Chatbot", page_icon="💬")
st.title("💬 LangChain + Groq Chatbot")

# --- Sidebar settings ---
with st.sidebar:
    api_key = st.text_input("Groq API Key", type="password")
    model = st.selectbox(
        "Model",
        ["llama3-8b-8192", "llama3-70b-8192"],
        index=0,
    )
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7)
    system_prompt = st.text_area(
        "System prompt (optional)",
        value="You are a helpful assistant.",
    )
    if st.button("Clear chat"):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []  # list of dicts: {"role": "user"/"assistant", "content": str}

# --- Render chat history ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Handle new input ---
prompt = st.chat_input("Type your message...")

if prompt:
    if not api_key:
        st.error("Please enter your groq API key in the sidebar.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Build LangChain message list from history
    lc_messages = [SystemMessage(content=system_prompt)]
    for m in st.session_state.messages:
        if m["role"] == "user":
            lc_messages.append(HumanMessage(content=m["content"]))
        else:
            lc_messages.append(AIMessage(content=m["content"]))

    llm = ChatGroq(
        model="openai/gpt-oss-20b",
        groq_api_key=api_key,
        temperature=temperature,
        streaming=True,
    )

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        for chunk in llm.stream(lc_messages):
            full_response += chunk.content
            placeholder.markdown(full_response + "▌")
        placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
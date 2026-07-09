from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage,AIMessage
import os
import getpass

store={}

llm=ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.9,
    max_tokens=None,
    reasoning_format="parsed",
    max_retries=2,
    timeout=None
)

store["history"] = []

while True:

    user_input=input("Write your Massage:\n")

    if user_input.lower() in ["exit","bye",]:
        break
    prompt= ChatPromptTemplate([
        ("system","you are a personal Assistant and helpful chatbot."),
        MessagesPlaceholder(variable_name="history"),
        ("user","{input}")
    ])
    history = store["history"] 

    msg=prompt.invoke({"input":user_input,"history":history})

    result=llm.invoke(msg)

    print(result.content)


    history.append(HumanMessage(content=user_input))
    history.append(AIMessage(content=result.content))

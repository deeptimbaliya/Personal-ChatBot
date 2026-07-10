from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

class Groq():
    def __init__(self):
        self.model=ChatGroq(
            model="openai/gpt-oss-20b",
            temperature=0.9,
            max_tokens=None,
            reasoning_format="parsed",
            max_retries=2,
            timeout=None
        )
        self.prompt= ChatPromptTemplate([
            ("system","you are a personal Assistant and helpful chatbot."),
            MessagesPlaceholder(variable_name="history"),
            ("user","{input}")
        ])


    def Create_prompt(self,user_input, history) :
        return self.prompt.invoke({"input":user_input,"history":history})

        




from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
load_dotenv()
GROQ_MODEL = os.getenv("GROQ_MODEL")
def get_chat_title(user_query):
    llm = ChatGroq(model=GROQ_MODEL,temperature = 0)
    title_prompt_template = ("You are a helpful chat assistant that provides short, clear and catchy title. \n\n"
                             "Task:\n- Read the given user query.\n- Create a concise title (max 7 words).\n"
                       "- The title should summarize the intent of the query.\n"
                       "- Avoid unnecessary words, punctuation, or filler.\n"
                       "- Keep it professional and easy to understand.\n\n"
                       "User Query:\n{user_query}\n\n"
                       "Output:\nTitle:")
    # title_prompt = PromptTemplate(title_prompt_template).format(user_query = user_query)
    title_prompt = PromptTemplate(
        input_variables=["user_query"],
        template=title_prompt_template
    ).format(user_query=user_query)
    title = llm.invoke(title_prompt).content
    return title
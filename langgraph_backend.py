from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph.message import add_messages
from dotenv import load_dotenv 
from langgraph.checkpoint.memory import InMemorySaver

# llm 
load_dotenv()
llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-flash")

# State
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

# Task
def chat_node(state: ChatState):

    messages = state['messages']

    response = llm.invoke(messages)

    return {'messages' : [response]}

# Graph
checkpointer = InMemorySaver()
graph = StateGraph(ChatState)

graph.add_node('chat_node',chat_node)

graph.add_edge(START,'chat_node')
graph.add_edge('chat_node',END)

chatbot = graph.compile(checkpointer=checkpointer)



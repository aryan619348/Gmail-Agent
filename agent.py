import os
from dotenv import load_dotenv
load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")

from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent
from langchain.chains.conversation.memory import ConversationBufferWindowMemory

from calendar_functions import tools

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

memory = ConversationBufferWindowMemory(
    memory_key='chat_history',
    k=1,
    return_messages=True
)
llm = ChatOpenAI(temperature=0,model_name='gpt-3.5-turbo')
conversational_agent = initialize_agent(
    agent='chat-conversational-react-description',
    tools=tools,
    llm=llm,
    verbose=True,
    max_iterations=3,
    early_stopping_method='generate',
    memory=memory,
    handle_parsing_errors=True
)

print(conversational_agent.run("Create a new mmeting called trial at tajmahal for the pupose of trial from 10am to 12pm on december 30th"))
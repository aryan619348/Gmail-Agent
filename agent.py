import os
from dotenv import load_dotenv
load_dotenv()
# for deployment
OPENAI_API_KEY=os.environ["OPENAI_API_KEY"]

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.prompts import MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage
from langchain.tools.render import format_tool_to_openai_function
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.agents import AgentExecutor


from tools import tools

# llm = ChatOpenAI(model="gpt-4-0613", temperature=0)
llm = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0)
MEMORY_KEY = "chat_history"
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You're a calendar assistant. For any calendar or events related questiosn first find the todays date and then figure out the dates to use based on the result.",
        ),
        MessagesPlaceholder(variable_name=MEMORY_KEY),
        ("user", "{input}"),
        ("Answer the question if possible using the history and use the tools after that only"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

chat_history = []
llm_with_tools = llm.bind(functions=[format_tool_to_openai_function(t) for t in tools])

agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_to_openai_function_messages(
            x["intermediate_steps"]
        ),
        "chat_history": lambda x: x["chat_history"],
    }
    | prompt
    | llm_with_tools
    | OpenAIFunctionsAgentOutputParser()
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

def my_agent(question):
    result = agent_executor.invoke({"input": question, "chat_history": chat_history})
    chat_history.extend(
        [
            HumanMessage(content=question),
            AIMessage(content=result["output"]),
        ]
    )
    return result

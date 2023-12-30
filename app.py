import gradio as gr
from agent import conversational_agent

def chatbot(message,history):
    response=conversational_agent(message)
    answer =response['output']
    return answer

gr.ChatInterface(
    chatbot,
    chatbot=gr.Chatbot(height=300),
    textbox=gr.Textbox(placeholder="Ask me a yes or no question", container=False, scale=7),
    title="Google Calendar Agent",
    description="Converse with your google calendar!!",
    theme="soft",
    retry_btn=None,
    undo_btn="Delete Previous",
    clear_btn="Clear",
).launch()
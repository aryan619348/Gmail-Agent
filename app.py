import gradio as gr
from agent import conversational_agent
from calendar_functions import create_service
import os.path

from ingest_credentials import save_copy

def chatbot(message,history,uploaded_file):
    if not os.path.exists("token.json"):
        print("path == ", uploaded_file)
        save_copy(uploaded_file[0])
    response=conversational_agent(message)
    answer =response['output']
    return answer

    

gr.ChatInterface(
    chatbot,
    chatbot=gr.Chatbot(height=300),
    textbox=gr.Textbox(placeholder="Ask me a question for your calendar", container=False, scale=7),
    title="Google Calendar Agent",
    description="Converse with your google calendar!!",
    theme="soft",
    retry_btn=None,
    undo_btn="Delete Previous",
    clear_btn="Clear",
    additional_inputs=[
                            gr.File(file_types=["json"], file_count="multiple")
                        ],

).launch()
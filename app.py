import gradio as gr

from agent import my_agent
import os.path

from ingest_credentials import save_copy

from voice_bot import voice_bot
def chatbot(message,history,uploaded_file):
    if uploaded_file:
        if not os.path.exists("token.json"):
            save_copy(uploaded_file[0])
        response=my_agent(message)
        answer =response['output']
        return answer
    else:
        answer = "Please add the credentials.json before proceeding in the additional inputs section"
        return answer

    

chatbot=gr.ChatInterface(
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

)
demo = gr.Blocks()
with demo:
    gr.TabbedInterface([chatbot,voice_bot],["Chatbot","Voice-Enabled Bot"])

demo.launch()


import gradio as gr
from voice_bot import voice_bot
from chat_bot import chat_bot
demo = gr.Blocks()
with demo:
    gr.TabbedInterface([chat_bot,voice_bot],["Chatbot","Voice-Enabled Bot"])

demo.launch(server_port=8000)

import requests
import gradio as gr
import os
from dotenv import load_dotenv
load_dotenv()
# token = os.getenv("HUGGINGFACE_KEY")

token=os.environ.get("HUGGINGFACE_KEY")
from agent import my_agent
from ingest_credentials import save_copy


API_URL = "https://api-inference.huggingface.co/models/openai/whisper-tiny"
headers = {"Authorization": "Bearer {token}"}

def query(audio_file,uploaded_file):
    if uploaded_file:
        if not os.path.exists("token.json"):
            save_copy(uploaded_file[0])
        with open(audio_file, "rb") as f:
            data = f.read()
        response = requests.post(API_URL, headers=headers, data=data)
        question = response.json()['text']
        response=my_agent(question)
        answer =response['output']
        return answer
    else:
        answer = "Please add the credentials.json before proceeding in the additional inputs section"
        return answer



voice_bot = gr.Interface(
    fn=query,
    inputs=[
        gr.Audio(sources=["microphone"],type="filepath"),
        gr.File(file_types=["json"], file_count="multiple")
    ],
    outputs="text",
    title="Google Calendar Agent",
    description="Converse with your google calendar!!",
)




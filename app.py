import streamlit as st
from lyzr_automata.ai_models.openai import OpenAIModel
from lyzr_automata import Agent,Task
from lyzr_automata.pipelines.linear_sync_pipeline import LinearSyncPipeline
from PIL import Image
from dotenv import load_dotenv
import os

load_dotenv()
api = os.getenv("OPENAI_API_KEY")

st.set_page_config(
    page_title="Lyzr Error Resolver",
    layout="centered",  # or "wide"
    initial_sidebar_state="auto",
    page_icon="lyzr-logo-cut.png",
)

st.markdown(
    """
    <style>
    .app-header { visibility: hidden; }
    .css-18e3th9 { padding-top: 0; padding-bottom: 0; }
    .css-1d391kg { padding-top: 1rem; padding-right: 1rem; padding-bottom: 1rem; padding-left: 1rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

image = Image.open("lyzr-logo.png")
st.image(image, width=150)

# App title and introduction
st.title("Lyzr Error Resolver🕸️")
st.markdown("### Welcome to the Lyzr Error Resolver!")
st.markdown("Upload Your Code and Error.This App fix your errors!!!")

open_ai_text_completion_model = OpenAIModel(
    api_key=api,
    parameters={
        "model": "gpt-4-turbo-preview",
        "temperature": 0.2,
        "max_tokens": 1500,
    },
)

system = st.text_area("Enter Code: ", height=300)
tech = st.text_input("Enter error: ")

bug_fixing_agent = Agent(
    role="Bug Fixing expert",
    prompt_persona=f"You are a Software developer and You are an expert at bug fixing"
)

bug_fixing_task = Task(
    name="Bug Fixing Task",
    model=open_ai_text_completion_model,
    agent=bug_fixing_agent,
    log_output=True,
    instructions=f"""I am getting the error {tech} from the following snippet of code: {system}. How can I fix it?
    """
)


if st.button("Resolve"):
    output = LinearSyncPipeline(
        name="Bug Fixing Pipeline",
        completion_message="Bug Fixed!!",
        tasks=[
            bug_fixing_task
        ],
    ).run()

    st.markdown(output[0]['task_output'])

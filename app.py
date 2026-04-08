import gradio as gr
from inference import run_model

def run(symptoms):
    return run_model(symptoms)

iface = gr.Interface(
    fn=run,
    inputs=gr.Textbox(label="Enter symptoms"),
    outputs="text",
    title="AI Medical Triage System",
    description="Describe your symptoms"
)

iface.launch(server_name="0.0.0.0", server_port=7860)
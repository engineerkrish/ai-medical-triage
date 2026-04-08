import gradio as gr
from fastapi import FastAPI
from pydantic import BaseModel
from inference import run_model

# ------------------- FASTAPI -------------------

app = FastAPI()

class Input(BaseModel):
    symptoms: str

# ✅ Required for OpenEnv
@app.post("/reset")
def reset():
    return {"message": "Environment reset successful"}

# ✅ Required for OpenEnv
@app.post("/step")
def step(input: Input):
    output = run_model(input.symptoms)
    return {"output": output}


# ------------------- GRADIO -------------------

def run(symptoms):
    return run_model(symptoms)

iface = gr.Interface(
    fn=run,
    inputs=gr.Textbox(label="Enter symptoms"),
    outputs="text",
    title="AI Medical Triage System",
    description="Describe your symptoms"
)

# Mount Gradio inside FastAPI
app = gr.mount_gradio_app(app, iface, path="/")
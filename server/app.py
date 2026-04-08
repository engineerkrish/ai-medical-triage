from fastapi import FastAPI
import gradio as gr

app = FastAPI()

@app.get("/")
def main():
    return {"message": "AI Medical Triage running"}

@app.post("/reset")
def reset():
    return {"message": "Environment reset successful"}

@app.post("/step")
def step(input: dict):
    return {"output": "processed"}

# Gradio
def run(symptoms):
    return "Diagnosis result"

iface = gr.Interface(
    fn=run,
    inputs="text",
    outputs="text"
)

app = gr.mount_gradio_app(app, iface, path="/")
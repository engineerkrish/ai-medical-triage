from fastapi import FastAPI
import gradio as gr

# 👉 Your existing imports (keep if needed)
# from env.models import run_model
# from pydantic import BaseModel

app = FastAPI()

# -------------------------------
# REQUIRED ROOT ENDPOINT (IMPORTANT)
# -------------------------------
@app.get("/")
def main():
    return {"message": "AI Medical Triage running"}

# -------------------------------
# RESET ENDPOINT
# -------------------------------
@app.post("/reset")
def reset():
    return {"message": "Environment reset successful"}

# -------------------------------
# STEP ENDPOINT
# -------------------------------
@app.post("/step")
def step(input: dict):
    symptoms = input.get("symptoms", "")
    output = run(symptoms)
    return {"output": output}

# -------------------------------
# MODEL FUNCTION (KEEP YOUR LOGIC)
# -------------------------------
def run(symptoms):
    # 👉 Replace with your actual model call
    return f"Processed symptoms: {symptoms}"

# -------------------------------
# GRADIO UI
# -------------------------------
iface = gr.Interface(
    fn=run,
    inputs=gr.Textbox(label="Enter symptoms"),
    outputs="text",
    title="AI Medical Triage System",
    description="Describe your symptoms"
)

# -------------------------------
# MOUNT GRADIO INTO FASTAPI
# -------------------------------
app = gr.mount_gradio_app(app, iface, path="/")
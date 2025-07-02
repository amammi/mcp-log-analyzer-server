import os
import gradio as gr

from agent import LogAnalyzerAgentWrapper

def call_log_analyzer_agent(provider, model, container_name, log_level):
    wrapper = LogAnalyzerAgentWrapper()
    if provider == "openai" and os.getenv("OPENAI_API_KEY", "") == "":
        message = "Attenzione: chiave OpenAI mancante nel file .env, per favore inserire una chiave valida e poi proseguire."
        raise gr.Error(message=message)
    model = model.strip()
    container_name = container_name.strip()
    yield wrapper.analyze(provider, model, container_name, log_level)



provider = gr.Radio(choices=["ollama", "openai"], label="Seleziona il provider del LLM da utilizzare",value="openai")
model = gr.Textbox(label="Inserisci il nome di un LLM valido da utilizzare a seconda del provider scelto", value="gpt-4.1-mini")
log_level = gr.Radio(choices=['INFO', 'DEBUG', "ERROR"], label="Seleziona il log level da analizzare")
container_name = gr.Textbox(label="Inserisci il nome del container dal quale estrarre i log da analizzare")

demo = gr.Interface(fn=call_log_analyzer_agent, inputs=[provider, model, container_name, log_level], outputs=["textbox"], title="Docker Logs Analyzer for FastAPI app", flagging_mode='never')


demo.launch()
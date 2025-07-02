import os
import asyncio
from autogen_agentchat.ui import Console
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.ollama import OllamaChatCompletionClient
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.tools.mcp import McpWorkbench
from autogen_ext.tools.mcp._config import SseServerParams
from fastmcp import Client
from dotenv import load_dotenv

import click

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop=loop)

class LogAnalyzerAgentWrapper:
    def __init__(self):
        load_dotenv()
        self.mcp_base_url = os.getenv("MCP_BASE_URL")
        self.mcp_server_params = SseServerParams(url=self.mcp_base_url)
    
    def analyze(self, provider: str, model: str, container_name: str, log_level_choice: str):
        return loop.run_until_complete(self._analyze(provider, model, container_name, log_level_choice))
    
    def __get_model_client(self, provider: str, model: str):
        match provider:
            case 'ollama':
                model_client = OllamaChatCompletionClient(host=os.getenv("CUSTOM_MODEL_BASE_URL"), model=model)
                
            case 'openai':
                model_client = OpenAIChatCompletionClient(model=model, api_key=os.getenv("OPENAI_API_KEY", ""), temperature=0.3)
                
            case _:
                raise ValueError("Provider non valido.")
        
        return model_client
    
    async def _analyze(self, provider: str, model: str, container_name: str, log_level_choice: str):

        async with Client(self.mcp_base_url) as mcp_client:
        
            async with McpWorkbench(self.mcp_server_params) as wb:

                try:
                    system_message = (await mcp_client.get_prompt("assistant_system_message")).messages[0].content.text
                except Exception as e:
                    print("Errore tecnico nel recupero del system message dell'assistente. Per favore riprovare.")
                    print(str(e))
                    return
                
                assistant = AssistantAgent(
                    "log_analyzer",
                    model_client=self.__get_model_client(provider, model),
                    workbench=wb,
                    system_message=system_message,
                    reflect_on_tool_use=True,
                    model_client_stream=True,
                )
                try:
                    task = (await mcp_client.get_prompt("resume_analyze_logs", {"container_name": container_name, "level": log_level_choice})).messages[0].content.text
                except Exception as e:
                    print("Errore tecnico nel recupero del task. Per favore riprovare.")
                    print(str(e))
                    return
                
                return (await assistant.run(task=task)).messages[-1].content


async def main(provider: str = "ollama", model: str = "qwen3:latest"):
    mcp_base_url = os.getenv("MCP_BASE_URL")
    async with Client(mcp_base_url) as mcp_client:

        mcp_server_params = SseServerParams(url=mcp_base_url)
        async with McpWorkbench(mcp_server_params) as wb:
            match provider:
                case 'ollama':
                    model_client = OllamaChatCompletionClient(host=os.getenv("CUSTOM_MODEL_BASE_URL"), model=model)
                    
                case 'openai':
                    model_client = OpenAIChatCompletionClient(model=model, api_key=os.getenv("OPENAI_API_KEY", ""))
                    
                case _:
                    raise ValueError("Provider non valido.")

            try:
                system_message = (await mcp_client.get_prompt("assistant_system_message")).messages[0].content.text
            except Exception as e:
                print("Errore tecnico nel recupero del system message dell'assistente. Per favore riprovare.")
                print(str(e))
                return
            
            assistant = AssistantAgent(
                "log_analyzer",
                model_client=model_client,
                workbench=wb,
                system_message=system_message,
                reflect_on_tool_use=True,
                model_client_stream=True,
            )
            container_name = input("Inserisci il nome del container che vuoi analizzare: ")
            log_level_choice = input("""Inserisci il codice del log level da analizzare: 
1) INFO
2) DEBUG
3) ERROR
Scelta: """)
            match log_level_choice.strip():
                case "1":
                    log_level_choice = "INFO"
                case "2":
                    log_level_choice = "DEBUG"
                case "3":
                    log_level_choice = "ERROR"
                case _:
                    print("Errore nella scelta del log level. Riavviare e riprovare inserendo una delle opzioni disponibili.")
                    return 
            try:
                task = (await mcp_client.get_prompt("resume_analyze_logs", {"container_name": container_name, "level": log_level_choice})).messages[0].content.text
            except Exception as e:
                print("Errore tecnico nel recupero del task. Per favore riprovare.")
                print(str(e))
                return
            await Console(assistant.run_stream(task=task))
            

@click.command()
@click.option("--provider", "-p", type=str, help="Specifica che tipo di provider usare per gli LLM. Disponibili \"ollama\" e \"openai\"", default="ollama")
@click.option("--model", "-m", type=str, help="indicare il modello ollama/openai che si intende utilizzare", default="qwen3:latest")
def runner(provider: str, model: str):
    asyncio.run(main(provider=provider, model=model))

if __name__ == '__main__':
    try:
        runner()
    except Exception as e:
        print(str(e))
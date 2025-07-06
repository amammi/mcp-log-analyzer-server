import os
import asyncio

from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.ollama import OllamaChatCompletionClient
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.models.anthropic import AnthropicChatCompletionClient
from autogen_ext.tools.mcp import McpWorkbench
from autogen_ext.tools.mcp._config import SseServerParams
from fastmcp import Client
from dotenv import load_dotenv


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop=loop)


class LogAnalyzerAgentWrapper:
    def __init__(self, mcp_base_url: str = None):
        load_dotenv()
        self.mcp_base_url: str = os.getenv("MCP_BASE_URL") if mcp_base_url is None else mcp_base_url
        self.mcp_server_params = SseServerParams(url=self.mcp_base_url)
    
    def analyze(self, provider: str, model: str, container_name: str, log_level_choice: str, api_key: str = None, base_url: str = None) -> str:
        return loop.run_until_complete(self._analyze(provider, model, container_name, log_level_choice, api_key, base_url))
    
    def __get_model_client(self, provider: str, model: str, api_key: str = None, base_url: str = None):
        base_url = base_url or os.getenv("CUSTOM_MODEL_BASE_URL")
        match provider:
            case 'ollama':
                model_client = OllamaChatCompletionClient(host=base_url if base_url is None else base_url, model=model)

            case 'anthropic':
                model_client = AnthropicChatCompletionClient(model=model, api_key=api_key, temperature=0.3)
                
            case 'openai':
                model_client = OpenAIChatCompletionClient(model=model, api_key=api_key, temperature=0.3)
                
            case _:
                raise ValueError("Provider non valido.")
        
        return model_client
    
    async def _analyze(self, provider: str, model: str, container_name: str, log_level_choice: str, api_key: str = None, base_url: str = None) -> str:

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
                    model_client=self.__get_model_client(provider, model, api_key, base_url),
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
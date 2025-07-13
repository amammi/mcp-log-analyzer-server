import os
import asyncio
import logging

from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.ollama import OllamaChatCompletionClient
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.models.anthropic import AnthropicChatCompletionClient
from autogen_ext.tools.mcp import McpWorkbench
from autogen_ext.tools.mcp._config import SseServerParams
from fastmcp import Client

from client_webapp.models import McpServerConfig

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop=loop)
logger = logging.getLogger(__name__)


class LogAnalyzerAgentWrapper:
    def __init__(self, mcp_servers: list[McpServerConfig] = None):
        self.workbenches: list[McpWorkbench] = []
        for server in mcp_servers:
            match server.connection_type:
                case "sse":
                    params = SseServerParams(url=f"{server.base_url}/sse")
                case _:
                    raise ValueError(f"Unknown server type {server.connection_type}")

            self.workbenches.append(McpWorkbench(server_params=params))
    
    def analyze(self, provider: str, model: str, container_name: str, log_level_choice: str, api_key: str = None, base_url: str = None) -> str:
        return loop.run_until_complete(self._analyze(provider, model, container_name, log_level_choice, api_key, base_url))
    
    def __get_model_client(self, provider: str, model: str, api_key: str = None, base_url: str = None):
        base_url = base_url or os.getenv("CUSTOM_MODEL_BASE_URL")
        match provider:
            case 'ollama':
                model_client = OllamaChatCompletionClient(host=base_url, api_key=api_key, model=model, temperature=0.0, model_info={'function_calling': True, 'family': 'unknown', 'json_output': True, 'vision': False, 'structured_output': True })

            case 'anthropic':
                model_client = AnthropicChatCompletionClient(model=model, api_key=api_key, temperature=0.0)
                
            case 'openai':
                model_client = OpenAIChatCompletionClient(model=model, api_key=api_key, temperature=0.0)
                
            case _:
                raise ValueError("Provider non valido.")
        
        return model_client
    
    async def _analyze(self, provider: str, model: str, container_name: str, log_level_choice: str, api_key: str = None, base_url: str = None) -> str | None:

        server_params = self.workbenches[0].server_params
        print(server_params.url)
        async with Client(server_params.url) as mcp_client :

            try:
                system_message = (await mcp_client.get_prompt("assistant_system_message")).messages[0].content.text
            except Exception as e:
                msg = "Errore tecnico nel recupero del system message dell'assistente. Per favore riprovare."
                logger.error(msg)
                raise RuntimeError(msg) from e

            assistant = AssistantAgent(
                "log_analyzer",
                model_client=self.__get_model_client(provider, model, api_key, base_url),
                workbench=self.workbenches,
                max_tool_iterations=20,
                system_message=system_message,
                reflect_on_tool_use=True,
                model_client_stream=True,
            )

            try:
                task = (await mcp_client.get_prompt("resume_analyze_logs", {"container_name": container_name, "level": log_level_choice})).messages[0].content.text
            except Exception as e:
                msg = "Errore tecnico nel recupero del task. Per favore riprovare."
                logger.error(msg)
                raise RuntimeError(msg) from e

            return (await assistant.run(task=task)).messages[-1].content
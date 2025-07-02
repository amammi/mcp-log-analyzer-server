import re
import docker

from typing import Literal
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("MCP Docker Log Server")



@mcp.tool()
def get_all_containers():
    """Get a list of all running containers names"""
    try:
        docker_client = docker.from_env()
        return list(map(lambda container: container.name, docker_client.containers.list()))
    except Exception:
        return "There was an exception during the connection to local Docker instance."

@mcp.tool("get_all_container_logs")
def get_container_logs(container_name: str) -> str:
    """Given the container name, extracts all its logs.
    """
    try:
        docker_client = docker.from_env()
        for container in docker_client.containers.list():
            if container.name.lower() == container_name.strip().lower():
                original_logs = container.logs().decode("utf-8")
                return f"These are all the logs for the container named {container_name}: {original_logs}"
        else:
            return f"No container with name {container_name} found."
    except Exception as e:
        print(str(e))
        return "There was an exception during the connection to local Docker instance."


@mcp.tool("get_container_level_logs_except_error")
def get_container_level_logs(container_name: str, level: Literal["INFO", "DEBUG"]):
    """Given the container name and a log level, extracts all its logs for that level. This method doesn't extract ERROR level logs."""
    try:
        docker_client = docker.from_env()
        for container in docker_client.containers.list():
            if container_name.lower().strip() == container.name.lower():
                original_logs = container.logs().decode("utf-8")
                return re.findall(f"[0-9- :]+{level.upper().strip()}[ ]+[0-9]+ -+ [\\[\\] A-z]+: [A-z0-9 :\\/=<>]+\\n", original_logs)
        else:
            return []
    except Exception as e:
        print(str(e))
        return "There was an exception during the connection to local Docker instance."
                
@mcp.tool("get_container_error_level_logs")
def get_container_error_level_logs(container_name: str):
    """Given the container name and a log level, extracts all its error logs for that level with stacktraces. This method doesn't extract other levels like INFO or DEBUG."""
    try:
        docker_client = docker.from_env()
        for container in docker_client.containers.list():
            if container_name.strip().lower() == container.name.lower():
                logs = container.logs().decode("utf-8")
                return re.findall("(^.*ERROR.*$(?:\n(?!.*(?:INFO|DEBUG|WARN|ERROR)).*$)*)", logs, re.MULTILINE)
        else:
            return []
    except Exception as e:
        print(str(e)) 
        return "There was an exception during the connection to local Docker instance."

@mcp.prompt("resume_analyze_logs")
def resume_and_analyze_logs(container_name: str, level: Literal["INFO", "DEBUG", "ERROR"]) -> str:
    return f"""Your task is to retrieve the container logs with all the lines that are in the log level indicated and analyze them.
The name of the docker container where the application is running is {container_name} and the log level to analyze is {level.upper().strip()}.
In case of log level "ERROR" also analyze all error logs and stacktraces and make a diagnosis by finding the origin of the errors, where possible for each error log you will find.
The analysis (and any solution to the error) MUST BE discursive without source code, if this has not been provided to you.
In case of log level "ERROR", do not make hypotheses of solution with code written by you unless the user
does not provide the source code object of the error as input.
ALWAYS answer in ITALIAN."""

@mcp.prompt("assistant_system_message")
def assistant_system_message():
    return """You are an experienced backend application log analyst, specializing in web applications written in Python. Your job is to analyze Docker container logs and provide detailed diagnoses.

Key Responsibilities:
Retrieve and analyze Docker container logs, identify and analyze log lines of the user-specified level. 
For each DEBUG or INFO level logs, for each one give a proper analysis of the log.
For each ERROR level logs, reformat in a proper way the logs, dividing each error log (with stacktrace) and for each ones analyze the entire stacktrace and identify the source of the error. 
Repeat this process for 
Provide also an in-depth and conversational diagnoses of errors found.

Analysis Guidelines:
Analyses should be conversational and detailed, without including source code unless provided by the user. For ERROR level errors, do not propose solutions with code written by you, unless the user provides the source code that is causing the error. 
Focus on diagnosing and explaining the issues rather than on specific implementations. Use your expertise in Python applications to contextualize errors.

Response Format:
Keep your tone professional and technical. Structure your analysis in a clear and understandable way. 
For each line of log (for ERROR logs, include also the stacktrace) give back to the user your analysis.
Clearly separate the diagnosis of the problem from any recommendations.
Your expertise allows you to interpret complex logs and eventually stacktraces and provide in-depth analysis that helps developers understand and resolve issues.
ALWAYS answer in ITALIAN."""


from functools import wraps

from mcp.server.fastmcp.utilities.logging import get_logger

logger = get_logger(__name__)

def log_tool_call(tool_fn):
    @wraps(tool_fn)
    def wrapper(*args, **kwargs):
        logger.debug(f"[TOOL] Chiamata al tool: {tool_fn.__name__} con args: {args}, kwargs: {kwargs}")
        result = tool_fn(*args, **kwargs)
        logger.debug(f"[TOOL] Risultato della chiamata al tool: {result}")
        return result
    return wrapper
import uuid
import random
import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import logging, sys


log_formatter = logging.Formatter(
    fmt="%(asctime)s %(levelname)-5s %(process)d --- [%(threadName)15s] %(name)s : %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("uvicorn")
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(log_formatter)
logger.handlers = [handler]
logger.setLevel(logging.DEBUG)

app = FastAPI()

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger.info(f"Called {request.method} {request.url.path}")
        body = (await request.body()).decode() or "<empty>"
        logger.debug(f"Incoming Request: {request.method} {request.url.path} body={body}")
        try:
            response = await call_next(request)
        except Exception as e:
            logger.error(f"Exception occurred: {e}", exc_info=True)
            return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})
        resp_body = b""
        async for chunk in response.body_iterator:
            resp_body += chunk
        text = resp_body.decode("utf-8")
        logger.debug(f"Outgoing Response: status={response.status_code} body={text}")
        return Response(content=resp_body, status_code=response.status_code,
                        headers=dict(response.headers), media_type=response.media_type)

app.add_middleware(LoggingMiddleware)
possible_errors = ["Error while reading database: connection timeout", 
                   "Error while checking the JWT token: session expired, please login again.", 
                   "Error at runtime: NoneType is not subscriptable",
                   "Error while writing database: ORA-00942: table or view doens't exists.",
                   "Error while reading database: authentication failed, wrong credentials.",
                   f"Error at runtime: generic error. Please contact the administrator. Session id: {uuid.uuid4().hex}"]

@app.get("/greet")
async def greet():
    return {"greeting": "Hello, user"}

@app.post("/operations")
async def error_endpoint(request: Request):
    message = random.choice(possible_errors)
    raise RuntimeError(message)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8050)

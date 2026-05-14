from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import PlainTextResponse
from agent.retail_agent import run_agent

app = FastAPI(
    title="Retail AI Assistant API",
    description="Agentic AI Retail Assistant using Groq + Tool Calling",
    version="1.0.0"
)

class QueryRequest(BaseModel):
    query: str


@app.get("/")
def home():
    return {
        "message": "Retail AI Assistant API is running"
    }

@app.post("/chat")
def chat(request: QueryRequest):

    response = run_agent(request.query)

    return PlainTextResponse(content=response)

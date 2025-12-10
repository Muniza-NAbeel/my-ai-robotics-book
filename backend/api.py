from fastapi import FastAPI
from pydantic import BaseModel
from my_agent import agent, Runner  # aapke agent ko import karo

app = FastAPI()

class QueryRequest(BaseModel):
    question: str

@app.post("/ask")
async def ask_question(request: QueryRequest):
    result = Runner.run_sync(agent, input=request.question)
    return {"answer": result.final_output}

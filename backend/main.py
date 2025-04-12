from fastapi import FastAPI
from database import SupabaseVectorDB
from advisor import RelocationAdvisor

app = FastAPI()
advisor = RelocationAdvisor()

@app.post("/chat")
async def chat(user_id: str, message: str):
    db = SupabaseVectorDB()
    response = advisor.generate_response(message)
    db.store_memory(user_id, response.embedding, response.text, {})
    return {"response": response.text}
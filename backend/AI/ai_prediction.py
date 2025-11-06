import os
import httpx
from dotenv import load_dotenv
import json

load_dotenv()

API_KEY = os.getenv("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")
Base_url = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

system_prompt = {
    "priority" : "You are an AI that classifies task priority as Low, Medium, or High. Consider title and the description for prediction.",

    "due_date": "You are an AI that predicts a reasonable due date (in YYYY-MM-DD format) for a given task. Consider title and the description for prediction.",

    "category": "You are an AI that classifies tasks into categories (Work, Study, Personal, Health, etc.). Consider title and the description for prediction.",

    "subtasks": "You are an AI that breaks down a task description into smaller subtasks. display with serialize nnumbers include small information about the subtask also. "
}

async def ai_predict(task : str, s_prompt:str) -> str:
    """Send a prompt to Openrouter API and return the AI response"""
    if s_prompt not in system_prompt:
        raise ValueError("Invalid prompt type")
    
    body={
    "model": "mistralai/mistral-small-24b-instruct-2501:free",
    "messages": [
        {"role" : "system", "content":system_prompt[s_prompt]},
        {"role" : "user","content" : task}
    ]
    }

    async with httpx.AsyncClient() as Client:
        response = await Client.post(Base_url, headers=headers, json = body)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()
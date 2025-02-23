from fastapi import FastAPI
from pydantic import BaseModel
import os
import groq
import dotenv

dotenv.load_dotenv()

app = FastAPI()

groq_client = groq.Client(api_key=os.getenv("GROQ_API_KEY"))

class PromptInput(BaseModel):
    prompt: str  # Ensure prompt is always a string

@app.post("/sales-recommendations")
async def sales_recommendations(input_data: PromptInput):
    sys_prompt = "Read the instructions and content carefully, then generate 10 unique and creative sales recommendations for increasing revenue."

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": input_data.prompt},  # Ensure this is a string
        ],
        max_tokens=10000
    )

    recommendations = response.choices[0].message.content
    return {"sales_recommendations": recommendations.split("\n")}

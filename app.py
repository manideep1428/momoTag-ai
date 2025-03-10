from fastapi import FastAPI
from pydantic import BaseModel
import os
import groq
import dotenv
from fastapi.middleware.cors import CORSMiddleware

dotenv.load_dotenv()

app = FastAPI()

groq_client = groq.Client(api_key=os.getenv("GROQ_API_KEY"))

class PromptInput(BaseModel):
    prompt: str  # Ensure prompt is always a string

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all headers
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}    

@app.post("/sales-recommendations")
async def sales_recommendations(input_data: PromptInput):
    sys_prompt = "Read the instructions and content carefully, then generate 10 unique and creative sales recommendations for increasing revenue."

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": input_data.prompt},
        ],
        max_tokens=10000
    )

    recommendations = response.choices[0].message.content.split("\n")  # Ensure list format
    return {"sales_recommendations": recommendations}  # Keep response consistent

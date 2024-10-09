from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from execute_trained_model import get_finetuned_bert_sentiment

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Load environment variables from .env file
load_dotenv()


class SentimentRequest(BaseModel):
    email: str

class UpdateMessage(BaseModel):
    email: str
    emotion: str


client = OpenAI()

@app.post("/sentiment/")
async def get_sentiment(request: SentimentRequest):
    return {"sentiment": get_finetuned_bert_sentiment(request.email)}


@app.post("/rephrase/")
async def update_message(request: UpdateMessage):
    TASK = "You are an email message processor. Given an email message and an emotion, you will update the email according to the emotion."

    prompt = f"Email: {request.email}\nEmotion: {request.emotion}"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": TASK},
            {"role": "user", "content": prompt}
        ]
    )
    return {"recipe": response.choices[0].message.content.strip()}

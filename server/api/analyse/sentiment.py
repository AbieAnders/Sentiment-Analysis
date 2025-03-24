from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from gtts import gTTS # type: ignore
import os
from transformers import pipeline
sentiment_analyzer = pipeline("sentiment-analysis")

router = APIRouter()

class Article(BaseModel):
    date: str
    title: str
    body: str
    url: str
    image: str
    source: str
    text: str

class SentimentRequest(BaseModel):
    articles: list[Article]

def hf_sentiment_transformer(text):
    truncated_text = text[:512] #sadly have to truncate to fit token limits
    try:
        result = sentiment_analyzer(truncated_text)[0]
        return {"text": text, "sentiment": result["label"], "score": result["score"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def generate_tts(text, sentiment_label):
    if not text:
        return None
    try:
        tts = gTTS(text=text, lang="hi", slow=False)
        filename = f"{sentiment_label}_speech.mp3"
        tts.save(filename)
        return filename
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating {sentiment_label} TTS: {e}")

@router.get('/download/{filename}')
async def download_file(filename: str):
    filepath = os.path.join(os.getcwd(), filename)
    if os.path.isfile(filepath):
        return FileResponse(filepath, filename=filename)
    else:
        raise HTTPException(status_code=404, detail="File not found")

@router.post('/sentiment_rpt')
async def generate_sentiment(request: SentimentRequest):
    try:
        analysis_results = [hf_sentiment_transformer(article.text) for article in request.articles]
        positive_texts = [res for res in analysis_results if res['sentiment'] == 'POSITIVE']
        negative_texts = [res for res in analysis_results if res['sentiment'] == 'NEGATIVE']

        most_positive = max(positive_texts, key=lambda x: x['score'], default=None)
        most_negative = max(negative_texts, key=lambda x: x['score'], default=None)

        positive_file = generate_tts(most_positive['text'], "most_positive") if most_positive else None
        negative_file = generate_tts(most_negative['text'], "most_negative") if most_negative else None

        return {
            "analysis": analysis_results,
            "most_positive": most_positive,
            "most_negative": most_negative,
            "positive_audio": f"/api/download/{positive_file}" if positive_file else None,
            "negative_audio": f"/api/download/{negative_file}" if negative_file else None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

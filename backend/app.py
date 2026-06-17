from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv
import base64
from typing import Optional
import uvicorn

load_dotenv()

app = FastAPI(title="Osaka Expat Helper API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class TranslationResponse(BaseModel):
    original_text: str
    english_translation: str
    summary: str
    key_actions: Optional[str] = None
    deadline: Optional[str] = None

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/translate", response_model=TranslationResponse)
async def translate_document(file: UploadFile = File(...)):
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        image_data = await file.read()
        base64_image = base64.b64encode(image_data).decode('utf-8')
        
        prompt = """
        Analyze this image of a Japanese official document and provide:
        1. The original Japanese text
        2. Full English translation
        3. A clear summary
        4. Key actions required
        5. Important deadlines
        
        Format:
        ORIGINAL_TEXT: [text]
        ENGLISH_TRANSLATION: [text]
        SUMMARY: [text]
        KEY_ACTIONS: [text]
        DEADLINE: [text]
        """
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert translator for expats in Japan."},
                {"role": "user", "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]}
            ],
            max_tokens=1000,
            temperature=0.3
        )
        
        result_text = response.choices[0].message.content
        lines = result_text.split('\n')
        parsed_data = {
            'original_text': '',
            'english_translation': '',
            'summary': '',
            'key_actions': '',
            'deadline': 'Not specified'
        }
        
        for line in lines:
            line = line.strip()
            if line.startswith('ORIGINAL_TEXT:'):
                parsed_data['original_text'] = line.replace('ORIGINAL_TEXT:', '').strip()
            elif line.startswith('ENGLISH_TRANSLATION:'):
                parsed_data['english_translation'] = line.replace('ENGLISH_TRANSLATION:', '').strip()
            elif line.startswith('SUMMARY:'):
                parsed_data['summary'] = line.replace('SUMMARY:', '').strip()
            elif line.startswith('KEY_ACTIONS:'):
                parsed_data['key_actions'] = line.replace('KEY_ACTIONS:', '').strip()
            elif line.startswith('DEADLINE:'):
                parsed_data['deadline'] = line.replace('DEADLINE:', '').strip()
        
        return TranslationResponse(**parsed_data)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
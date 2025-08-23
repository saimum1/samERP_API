
from datetime import datetime
from bson import ObjectId
from fastapi import HTTPException, status
from app.schemas import generativeAISchema
from app.core.generativeAIModel import GeminiService

async def create_generative_article(request: generativeAISchema.ArticleRequest):
    print("data for generative ai",request)
    try:
        gemini_service=GeminiService()
        if not request.topic and not request.prompt:
            raise HTTPException(status_code=400, detail="Either 'topic' or 'prompt' must be provided")
        if request.topic:
            result = gemini_service.generate_article(
                topic=request.topic,
                format_instructions=request.format_instructions,
                word_count=request.word_count
            )
        else:
            result = gemini_service.generate_content(
                prompt=request.prompt
            )
        
        return {"generated_content": result}
    
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except RuntimeError as re:
        raise HTTPException(status_code=500, detail=str(re))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    

async def analyze_leads(request: generativeAISchema.LeadAnalysisRequest):
    print("data for lead analysis", request)
    try:
        gemini_service = GeminiService()
        if not request.chats:
            raise HTTPException(status_code=400, detail="'chats' field must be provided")

        result = gemini_service.generate_lead_analysis(request.chats)
        return {"generated_content": result}

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except RuntimeError as re:
        raise HTTPException(status_code=500, detail=str(re))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

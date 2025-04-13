from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
from backend.ml.summarizer import process_and_summarize

router = APIRouter()

@router.post("/genai-tools/summarize")
async def summarize_content(
    text: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    vibe: str = Form("professional"),
    tone: str = Form("informative"),
    theme: str = Form("education")
):
    # Ensure that at least one of the inputs (text or file) is provided
    if not text and not file:
        raise HTTPException(status_code=400, detail="Please provide either text or a file.")

    try:
        # Pass all necessary arguments to process_and_summarize
        summary = await process_and_summarize(text, file, vibe, tone, theme)
        return JSONResponse(content={"summary": summary})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

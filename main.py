import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List
from ml_engine import predictor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Tag Service API",
    description="мл присвоение тегов",
    version="1.0.0"
)

class AssignTagsRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=4096, description="Текст сообщения")

class AssignTagsResponse(BaseModel):
    data: List[str] = Field(..., max_items=10, description="Присвоенные теги")

class HealthResponse(BaseModel):
    status: str

@app.get("/health", response_model=HealthResponse, tags=["system"])
async def health_check():
    """Проверка доступности сервиса."""
    return {"status": "ok"}

@app.post("/api/v1/tags/assign", response_model=AssignTagsResponse, tags=["tags"])
async def assign_tags(request: AssignTagsRequest):
    """Присваивает теги входящему сообщению."""
    if len(request.message.strip().split()) < 2:
        return {"data": ["прочее"]}
        
    try:
        result = predictor.process_message(request.message)
        logger.info(f"Запрос обработан. Выданы теги: {result['tags']}")
        
        return {"data": result["tags"]}
        
    except Exception as e:
        logger.error(f"Внутренняя ошибка ML-движка: {e}")
        raise HTTPException(status_code=500, detail="internal_error")
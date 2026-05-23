from fastapi import APIRouter, HTTPException, Body
from typing import Dict

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/")
async def chat_endpoint(message: str = Body(..., embed=True)) -> Dict[str, str]:
    """
    Эндпоинт для обработки чат-запросов.
    Валидирует входное сообщение и возвращает ответ.
    """
    if not message:
        raise HTTPException(status_code=400, detail="Сообщение не может быть пустым")
    if len(message) > 1000:
        raise HTTPException(status_code=400, detail="Сообщение слишком длинное (макс. 1000 символов)")
    
    # Обращение к бизнес-логике
    from services.business_logic import process_chat_message
    try:
        response = await process_chat_message(message)
        return response
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.exception(f"Ошибка обработки сообщения: {str(e)}")
        raise HTTPException(status_code=503, detail="Внутренняя ошибка сервиса")
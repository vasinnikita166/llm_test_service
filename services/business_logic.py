import logging
from typing import Dict, Any
from llm.llm_module import generate_response
from cache.ttl_cache import cache

logger = logging.getLogger(__name__)

@cache(ttl=300) # Кешировать ответы на 5 минут
async def process_chat_message(message: str) -> Dict[str, Any]:
    """
    Основная бизнес-логика обработки чат-сообщения.
    Вызывает другие компоненты и возвращает ответ.
    """
    logger.info(f"Начата обработка сообщения: {message[:50]}")
    try:
        # Генерация промпта и вызов LLM
        response_text = await generate_response(message)
        
        # Пост-обработка ответа
        cleaned_response = post_process_response(response_text)
        
        if not cleaned_response:
            raise ValueError("После пост-обработки ответ оказался пустым")
        
        logger.info("Сообщение успешно обработано")
        return {"response": cleaned_response}
    
    except Exception as e:
        logger.error(f"Ошибка в бизнес-логике: {str(e)}")
        raise

def post_process_response(response: str) -> str:
    """
    Пост-обработка ответа от LLM.
    Удаляет лишние пробелы, проверяет на пустоту.
    """
    cleaned = response.strip()
    # Дополнительные шаги пост-обработки можно добавить здесь
    return cleaned
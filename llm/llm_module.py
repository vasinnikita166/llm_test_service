import logging
import httpx
import asyncio
from typing import Optional
from .prompt_builder import build_prompt

logger = logging.getLogger(__name__)

# Конфигурация для вызова LLM
LLM_API_URL = "https://api.example.com/v1/generate" # Заглушка
LLM_API_KEY = "your-api-key" # Заглушка
TIMEOUT_SECONDS = 30
MAX_RETRIES = 3

async def generate_response(user_message: str) -> str:
    """
    Модуль вызова LLM с ретраями, таймаутом и fallback.
    """
    prompt = await build_prompt(user_message)
    logger.info("Сформирован промпт для LLM")
    
    # Fallback ответ
    fallback_response = "Извините, сейчас я не могу ответить. Попробуйте позже."
    
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            logger.info(f"Попытка {attempt} вызова LLM API")
            async with httpx.AsyncClient(timeout=TIMEOUT_SECONDS) as client:
                response = await client.post(
                    LLM_API_URL,
                    headers={"Authorization": f"Bearer {LLM_API_KEY}"},
                    json={"prompt": prompt, "max_tokens": 150}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    text = data.get("text", fallback_response)
                    logger.info("Успешно получен ответ от LLM API")
                    return text
                elif 500 <= response.status_code < 600:
                    # Ошибки сервера, возможно временные
                    logger.warning(f"Временная ошибка LLM API: {response.status_code}")
                    if attempt < MAX_RETRIES:
                        await asyncio.sleep(2 ** attempt) # Экспоненциальная задержка
                        continue
                else:
                    # Ошибки клиента (4xx) - не повторяем
                    logger.error(f"Ошибка LLM API: {response.status_code}, {response.text}")
                    break
                    
        except httpx.TimeoutException:
            logger.warning(f"Таймаут при вызове LLM API (попытка {attempt})")
            if attempt < MAX_RETRIES:
                await asyncio.sleep(2 ** attempt)
                continue
        except httpx.RequestError as e:
            logger.error(f"Ошибка соединения с LLM API: {e}")
            if attempt < MAX_RETRIES:
                await asyncio.sleep(2 ** attempt)
                continue
        except Exception as e:
            logger.exception(f"Неожиданная ошибка при вызове LLM: {e}")
            break
    
    logger.warning("Все попытки вызова LLM исчерпаны, возвращаем fallback")
    return fallback_response
from typing import Dict, Any

SYSTEM_PROMPT = "Ты — полезный ассистент. Ответь кратко."

async def build_prompt(user_message: str) -> str:
    """
    Формирует промпт для LLM из системного промпта и пользовательского запроса.
    """
    prompt = f"{SYSTEM_PROMPT}\n\nПользователь: {user_message}\nАссистент:"
    return prompt
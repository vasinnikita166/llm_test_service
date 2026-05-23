import logging
import time
import random

logger = logging.getLogger(__name__)

# Simulating LLM API call with retry logic, timeout and fallback

def call_llm(prompt: str, max_retries: int = 3, timeout: float = 10.0) -> str:
    """
    Call the LLM with retry logic, timeout simulation and fallback mechanism.
    In a real implementation, this would call an actual LLM API.
    """
    logger.info(f"Calling LLM with prompt: {prompt[:100]}...")
    
    last_exception = None
    
    for attempt in range(max_retries):
        try:
            # Simulate network timeout
            if random.random() < 0.3 and attempt < max_retries - 1:  # 30% chance of timeout, but not on last attempt
                raise TimeoutError(f"LLM API request timed out (attempt {attempt + 1}/{max_retries})")
            
            # Simulate other transient errors (5xx)
            if random.random() < 0.2 and attempt < max_retries - 1:  # 20% chance of server error
                error_code = random.choice([500, 502, 503, 504])
                raise Exception(f"LLM API returned error {error_code} (attempt {attempt + 1}/{max_retries})")
            
            # Simulate successful response after delay
            time.sleep(random.uniform(0.1, 1.0))
            
            # Simple rule-based response generation to simulate LLM
            user_text = prompt.split('Пользователь:')[-1].split('Ассистент:')[0].strip()
            
            # Very basic NLP to generate different responses
            if any(word in user_text.lower() for word in ['привет', 'здравствуй', 'добрый', 'hello', 'hi']):
                responses = [
                    "Здравствуйте! Как я могу вам помочь?",
                    "Приветствую! Готов помочь с любыми вопросами.",
                    "Добрый день! Чем могу быть полезен?"
                ]
            elif any(word in user_text.lower() for word in ['спасибо', 'благодарю', 'thank']):
                responses = [
                    "Пожалуйста! Рад был помочь.",
                    "Всегда пожалуйста! Обращайтесь снова.",
                    "Не за что! Я всегда здесь, чтобы помогать."
                ]
            elif '?' in user_text or any(word in user_text.lower() for word in ['как', 'что', 'где', 'когда', 'почему', 'зачем', 'кто', 'который']):
                responses = [
                    "Это интересный вопрос. По моему мнению, это зависит от контекста.",
                    "Хороший вопрос! Ответ может быть неоднозначным, но я постараюсь помочь.",
                    "Я понимаю ваш вопрос. Давайте рассмотрим это с разных сторон."
                ]
            else:
                responses = [
                    "Я понял ваше сообщение. Могу ли я чем-то помочь?",
                    "Спасибо за сообщение. Готов ответить на любые ваши вопросы.",
                    "Интересно. Расскажите, пожалуйста, больше о том, что вас интересует."
                ]
            
            response = random.choice(responses)
            logger.info(f"LLM call succeeded on attempt {attempt + 1}")
            return response
            
        except (TimeoutError, Exception) as e:
            last_exception = e
            logger.warning(f"LLM call failed on attempt {attempt + 1}: {str(e)}")
            
            if attempt < max_retries - 1:
                # Exponential backoff with jitter
                sleep_time = (2 ** attempt) * 0.1 + random.uniform(0, 0.1)
                logger.info(f"Retrying in {sleep_time:.2f} seconds...")
                time.sleep(sleep_time)
    
    # If all retries failed, return fallback response
    logger.error(f"All retry attempts failed. Using fallback response.")
    return "Извините, в данный момент я не могу обработать ваш запрос. Пожалуйста, попробуйте позже."
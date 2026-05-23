import time
import threading
from typing import Any, Callable, Dict

# Простой кеш с TTL, использующий словарь
_cache: Dict[str, Any] = {}
_cache_lock = threading.Lock()


def cache(ttl: int = 300):
    """
    Декоратор для кеширования результата функции с TTL (в секундах).
    Использует простой словарь.
    """
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> Any:
            # Создаем ключ из аргументов функции
            key = str((args, sorted(kwargs.items())))
            
            with _cache_lock:
                current_time = time.time()
                if key in _cache:
                    cached_result, timestamp = _cache[key]
                    if current_time - timestamp < ttl:
                        return cached_result
                    else:
                        # Удаляем устаревший кеш
                        del _cache[key]
            
            # Выполняем функцию и кешируем результат
            result = func(*args, **kwargs)
            
            with _cache_lock:
                _cache[key] = (result, current_time)
            
            return result
        return wrapper
    return decorator
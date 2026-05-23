import logging
from typing import Optional
from llm.prompt_builder import build_prompt
from llm.llm_client import call_llm
from llm.post_processor import process_response
from cache.ttl_cache import cache

logger = logging.getLogger(__name__)

def process_chat(user_message: str) -> str:
    """
    Main business logic function that orchestrates the chat processing pipeline.
    """
    try:
        logger.info("Starting chat processing pipeline")
        
        # Check cache first
        cache_key = f"chat:{user_message.strip()}",
        cached_response = cache.get(cache_key)
        if cached_response:
            logger.info("Cache hit - returning cached response")
            return cached_response
        
        # Build prompt
        prompt = build_prompt(user_message)
        logger.debug(f"Built prompt: {prompt[:200]}...")
        
        # Call LLM
        raw_response = call_llm(prompt)
        logger.debug(f"Raw LLM response: {raw_response[:200]}...")
        
        # Post-process response
        processed_response = process_response(raw_response)
        logger.debug(f"Processed response: {processed_response[:200]}...")
        
        # Validate response
        if not processed_response or len(processed_response.strip()) == 0:
            logger.error("LLM returned empty response after post-processing")
            raise Exception("Empty response from LLM")
        
        # Cache the response
        cache.set(cache_key, processed_response)
        
        logger.info("Chat processing completed successfully")
        return processed_response
        
    except Exception as e:
        logger.error(f"Error in chat processing pipeline: {str(e)}")
        raise e
import logging
import re

logger = logging.getLogger(__name__)

def process_response(response: str) -> str:
    """
    Post-process the LLM response to clean it up and ensure quality.
    """
    if not response:
        return response
    
    try:
        logger.debug(f"Processing response: {response[:200]}...")
        
        # Remove extra whitespace
        processed = re.sub(r'\s+', ' ', response.strip())
        
        # Fix common punctuation spacing issues
        processed = re.sub(r'\s+([,.!?;:])', r'\1', processed)
        
        # Ensure proper spacing after sentence endings
        processed = re.sub(r'([.!?])(\w)', r'\1 \2', processed)
        
        # Remove any leading/trailing quotes if they're not properly paired
        if processed.startswith(('"', '"')) and not processed.endswith(('"', '"')):
            processed = processed[1:]
        if processed.endswith(('"', '"')) and not processed.startswith(('"', '"')):
            processed = processed[:-1]
        
        logger.debug(f"Processed response: {processed[:200]}...")
        return processed
        
    except Exception as e:
        logger.error(f"Error in post-processing response: {str(e)}")
        # Return original response if processing fails
        return response
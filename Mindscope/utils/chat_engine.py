from .openai_client import generate_chat_response
from .fallback_responses import get_fallback_response
import logging
import requests




logger = logging.getLogger(__name__)

def generate_intelligent_response(user_message, history_messages=None):
    """
    Hybrid approach: Try multiple methods in order
    """
    # 1. First try Hugging Face API (your existing setup)
    try:
        hf_response = generate_chat_response(user_message, history_messages)
        if hf_response and hf_response != "This is an AI response to your message":
            return hf_response
    except Exception as e:
        logger.warning(f"Hugging Face API failed: {e}")
    
    # 2. Try simple API call without authentication
    try:
        response = requests.post(
            "https://api-inference.huggingface.co/models/microsoft/DialoGPT-small",
            json={
                "inputs": f"User: {user_message}\nAssistant:",
                "parameters": {"max_length": 150, "temperature": 0.7}
            },
           
           timeout = 5
        )



        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                generated_text = result[0].get('generated_text', '')
                if 'Assistant:' in generated_text:
                    return generated_text.split('Assistant:')[-1].strip()
                return generated_text.replace(f"User: {user_message}\nAssistant:", "").strip()
    except Exception as e:
        logger.warning(f"Simple API call failed: {e}")
    
    # 3. Final fallback to improved keyword system
    return get_fallback_response(user_message)
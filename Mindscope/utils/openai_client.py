import os
import logging
from django.conf import settings

# Try to import requests, with fallback if not available
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    logging.warning("Requests library not installed. Using fallback responses only.")

from .fallback_responses import get_fallback_response

logger = logging.getLogger(__name__)

def generate_chat_response(user_message, history_messages=None):
    """
    Generate AI response using Hugging Face Inference API with fallback
    """
    # If requests is not available, use fallback immediately
    if not REQUESTS_AVAILABLE:
        return get_fallback_response(user_message)
    
    # Try Hugging Face API first
    hf_response = try_hugging_face_api(user_message, history_messages)
    if hf_response:
        return hf_response
    
    # Fallback to local responses if API fails
    return get_fallback_response(user_message)

def try_hugging_face_api(user_message, history_messages):
    """
    Try to get response from Hugging Face API
    """
    API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-large"
    api_key = os.getenv("HUGGINGFACE_API_KEY")
    
    if not api_key:
        logger.warning("HUGGINGFACE_API_KEY not found in environment variables")
        return None
    
    headers = {"Authorization": f"Bearer {api_key}"}
    
    # Build conversation context
    conversation_text = build_conversation_context(user_message, history_messages)
    
    payload = {
        "inputs": conversation_text,
        "parameters": {
            "max_length": 150,
            "temperature": 0.7,
            "do_sample": True,
            "top_p": 0.9,
            "repetition_penalty": 1.1
        }
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=15)
        response.raise_for_status()
        
        result = response.json()
        if isinstance(result, list) and len(result) > 0:
            generated_text = result[0].get('generated_text', '')
            # Extract only the assistant's response
            if 'assistant:' in generated_text:
                return generated_text.split('assistant:')[-1].strip()
            return generated_text.strip()
        else:
            logger.warning("Unexpected response format from Hugging Face API")
            return None
            
    except requests.exceptions.Timeout:
        logger.warning("Hugging Face API timeout")
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Hugging Face API error: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error in Hugging Face API call: {e}")
        return None

def build_conversation_context(user_message, history_messages):
    """
    Build proper conversation context for the model
    """
    conversation = ""
    
    # Add system prompt (helps guide the AI's personality)
    conversation += "System: You are a supportive, empathetic mental health assistant. Be kind, understanding, and provide helpful suggestions. Don't give medical advice.\n"
    
    # Add conversation history
    if history_messages:
        for msg in history_messages:
            if msg['role'] == 'user':
                conversation += f"user: {msg['content']}\n"
            elif msg['role'] == 'assistant':
                conversation += f"assistant: {msg['content']}\n"
    
    # Add current message
    conversation += f"user: {user_message}\n"
    conversation += "assistant:"
    
    return conversation
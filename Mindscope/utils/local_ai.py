# Mindscope/utils/local_ai.py
from transformers import pipeline
import torch
import logging

logger = logging.getLogger(__name__)

class LocalAIChat:
    def __init__(self):
        self.chatbot = None
        try:
            # Use a small, fast model
            self.chatbot = pipeline(
                "text-generation",
                model="microsoft/DialoGPT-small",
                device=-1  # Use CPU (no GPU needed)
            )
            logger.info("Local AI model loaded successfully")
        except Exception as e:
            logger.warning(f"Could not load local model: {e}")
    
    def generate_response(self, user_message):
        if not self.chatbot:
            return None
        
        try:
            # Create prompt
            prompt = f"User: {user_message}\nAssistant:"
            
            # Generate response
            response = self.chatbot(
                prompt,
                max_length=150,
                temperature=0.7,
                do_sample=True,
                num_return_sequences=1
            )
            
            # Extract just the assistant's part
            full_text = response[0]['generated_text']
            if 'Assistant:' in full_text:
                return full_text.split('Assistant:')[-1].strip()
            return full_text.replace(prompt, '').strip()
            
        except Exception as e:
            logger.error(f"Local AI error: {e}")
            return None

# Global instance
local_ai = LocalAIChat()

def get_local_ai_response(user_message):
    return local_ai.generate_response(user_message)
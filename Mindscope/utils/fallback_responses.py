import re

FALLBACK_RESPONSES = {
    "greeting": "Hello! 👋 I'm here to provide emotional support and guidance. How are you feeling today?",
    "how_are_you": "I'm here and ready to listen! I'm an AI designed to provide mental health support. How can I help you today?",
    "name": "I'm your mental health support assistant! You can call me MindHelper. 😊",
    "help": "I'm here to listen and provide emotional support. You can share how you're feeling, ask for coping strategies, or discuss anything that's on your mind. What would you like to talk about?",
    "thanks": "You're very welcome! I'm glad I could help. Remember I'm here whenever you need someone to talk to. 💙",
    "goodbye": "Take care of yourself! Remember to practice self-care and reach out if you need more support. I'll be here when you return. 🌟",
    
    # ADD THIS NEW RESPONSE:
    "exercise": "Great question! Here are some helpful exercises:\n\n• **Deep Breathing**: 4-7-8 technique (inhale 4s, hold 7s, exhale 8s)\n• **Walking**: 15-20 minute brisk walk\n• **Yoga**: Child's pose or gentle stretches\n• **Progressive Muscle Relaxation**: Tense and release each muscle group\n• **Mindful Movement**: Gentle stretching with focus on breath",
    
    "anxious": "I understand feeling anxious can be really difficult. 😔 Try taking some deep breaths - inhale for 4 seconds, hold for 4, exhale for 6. Would you like to talk about what's making you feel this way?",
    "sleep": "Trouble sleeping can be so challenging. 😴 Establishing a regular bedtime routine, limiting screen time before bed, and creating a comfortable sleep environment can help. Would you like more specific suggestions?",
    "stress": "Stress management is so important for wellbeing. 🧘‍♀️ Try breaking tasks into smaller steps, taking short breaks, or practicing mindfulness. What's causing you stress right now?",
    "lonely": "Feeling lonely can be really tough. 💔 Reaching out to friends, joining community activities, or even volunteering can help create connections. Would you like to explore ways to feel more connected?",
    "work": "Work stress is common. 💼 Setting boundaries, prioritizing tasks, and taking regular breaks can help manage this. What aspect of work is most challenging for you?",
    "relationship": "Relationship issues can be complex. 💑 Clear communication and setting healthy boundaries are often helpful. Would you like to talk more about your specific situation?",
    "sad": "I'm sorry you're feeling sad. 😔 Remember that it's okay to feel this way. Sometimes talking about it, writing in a journal, or doing something you enjoy can help.",
    "angry": "Feeling angry is a natural emotion. 😠 Taking a walk, deep breathing, or counting to ten can help manage intense feelings. Would you like to talk about what's making you feel this way?",
    "overwhelm": "When feeling overwhelmed, try breaking things down into smaller steps. 📝 Focus on one thing at a time and remember to take breaks. What's feeling overwhelming right now?",
    
    "default": "Thank you for sharing. I'm here to listen and support you. How has your day been going? 💭"
}

def get_fallback_response(user_message):
    if not user_message or not isinstance(user_message, str):
        return FALLBACK_RESPONSES["default"]
    
    user_message = user_message.lower().strip()
    
    # Remove punctuation for better matching
    clean_message = re.sub(r'[^\w\s]', '', user_message)
    
    # === ADD THIS CHECK FOR EXERCISE ===
    if any(word in clean_message for word in ["exercise", "workout", "physical", "fitness", "yoga", "stretch"]):
        return FALLBACK_RESPONSES["exercise"]
    # ===================================
    
    # Check for quick topic button values first (exact matches)
    if "i'm having trouble sleeping" in user_message:
        return FALLBACK_RESPONSES["sleep"]
    elif "i'm feeling anxious" in user_message:
        return FALLBACK_RESPONSES["anxious"]
    elif "i need help with stress management" in user_message:
        return FALLBACK_RESPONSES["stress"]
    elif "i'm feeling lonely" in user_message:
        return FALLBACK_RESPONSES["lonely"]
    elif "i have work stress" in user_message:
        return FALLBACK_RESPONSES["work"]
    elif "i have a relationship issue" in user_message:
        return FALLBACK_RESPONSES["relationship"]
    
    # Greetings
    if any(word in clean_message for word in ["hi", "hello", "hey", "hola", "greetings", "good morning", "good afternoon"]):
        return FALLBACK_RESPONSES["greeting"]
    
    # How are you
    elif any(phrase in user_message for phrase in ["how are you", "how do you do", "how's it going"]):
        return FALLBACK_RESPONSES["how_are_you"]
    
    # Name questions
    elif any(phrase in user_message for phrase in ["who are you", "whats your name", "what is your name"]):
        return FALLBACK_RESPONSES["name"]
    
    # Help
    elif any(word in clean_message for word in ["help", "what can you do", "how do you work", "what should i do"]):
        return FALLBACK_RESPONSES["help"]
    
    # Thanks
    elif any(word in clean_message for word in ["thank", "thanks", "appreciate", "grateful"]):
        return FALLBACK_RESPONSES["thanks"]
    
    # Goodbye
    elif any(word in clean_message for word in ["bye", "goodbye", "see you", "talk later"]):
        return FALLBACK_RESPONSES["goodbye"]
    
    # Emotional states
    elif any(word in clean_message for word in ["anxious", "worry", "nervous", "panic", "anxiety"]):
        return FALLBACK_RESPONSES["anxious"]
    elif any(word in clean_message for word in ["sleep", "tired", "insomnia", "awake", "cant sleep", "can't sleep"]):
        return FALLBACK_RESPONSES["sleep"]
    elif any(word in clean_message for word in ["stress", "stressed", "overwhelm", "pressure", "stressing"]):
        return FALLBACK_RESPONSES["stress"]
    elif any(word in clean_message for word in ["lonely", "alone", "isolated", "isolation", "no friends"]):
        return FALLBACK_RESPONSES["lonely"]
    elif any(word in clean_message for word in ["work", "job", "career", "boss", "colleague", "office"]):
        return FALLBACK_RESPONSES["work"]
    elif any(word in clean_message for word in ["relationship", "partner", "friend", "family", "boyfriend", "girlfriend", "husband", "wife"]):
        return FALLBACK_RESPONSES["relationship"]
    elif any(word in clean_message for word in ["sad", "depress", "unhappy", "miserable", "down", "blue"]):
        return FALLBACK_RESPONSES["sad"]
    elif any(word in clean_message for word in ["angry", "mad", "frustrat", "annoy", "furious", "irritated"]):
        return FALLBACK_RESPONSES["angry"]
    elif any(word in clean_message for word in ["overwhelm", "too much", "cant handle", "drowning"]):
        return FALLBACK_RESPONSES["overwhelm"]
    
    else:
        return FALLBACK_RESPONSES["default"]
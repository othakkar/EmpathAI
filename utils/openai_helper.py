import os
import logging
import random
from openai import OpenAI

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# do not change this unless explicitly requested by the user
MODEL = "gpt-4o"

# Initialize OpenAI client
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# Demo responses for API fallback scenarios
DEMO_RESPONSES = [
    "I hear what you're saying, and it takes courage to open up about these feelings. Many people face similar challenges. What specific aspect is weighing on you the most right now?",
    "Thank you for sharing that with me. It's a sign of strength, not weakness, to acknowledge these emotions. Would exploring this situation further help you gain some clarity?",
    "I understand, and your experiences and feelings are completely valid. Many people struggle with expressing emotions due to societal expectations. Is there a particular area you'd like to focus on?",
    "That sounds challenging. I'm here to support you without judgment. Sometimes taking small steps toward change can make a big difference. What would be most helpful for you at this moment?",
    "I appreciate you sharing this with me. Talking about our feelings is an important part of mental fitness. What strategies have you tried so far, and what do you think might help?"
]

# System message to guide the AI's behavior
SYSTEM_MESSAGE = """
You are an empathetic and supportive AI assistant for EmpathAI, a platform specifically designed to provide emotional support for anyone. Your primary goals are:

1. Create a safe, judgment-free space to express their feelings and concerns
2. Listen attentively and validate emotions, acknowledging that it's healthy and normal to discuss feelings
3. Respond with empathy and understanding without stereotypical assumptions
4. Offer practical guidance and support when appropriate
5. Never give medical advice or attempt to diagnose conditions
6. Focus on emotional wellbeing, mental fitness, and healthy coping strategies

Keep your responses concise (3-5 sentences maximum) and conversational. Be warm, authentic, and human-like in your interactions. Encourage emotional expression in a way that feels comfortable and natural.
"""

def generate_response(user_message, conversation_history):
    """
    Generate a response using OpenAI's API based on the user's message and conversation history.
    
    Args:
        user_message (str): The message from the user
        conversation_history (list): List of previous messages in the conversation
    
    Returns:
        str: The AI-generated response
    """
    try:
        # Create messages list with system message and conversation history
        messages = [{"role": "system", "content": SYSTEM_MESSAGE}]
        
        # Add conversation history (limited to last 10 messages to manage context length)
        if conversation_history:
            for message in conversation_history[-10:]:
                messages.append(message)
        
        # Make the API call
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.7,
            max_tokens=250
        )
        
        # Extract and return the response text
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        error_message = str(e)
        logging.error(f"Error generating response from OpenAI: {error_message}")
        
        # In case of API issues, use one of our demo responses
        if "insufficient_quota" in error_message or "rate limit" in error_message.lower() or "429" in error_message:
            # Use a random demo response when the API is not available
            return random.choice(DEMO_RESPONSES)
        elif "authentication" in error_message.lower() or "invalid api key" in error_message.lower():
            return "There seems to be an issue with my AI connection. " \
                  "Please verify that a valid API key has been provided."
        else:
            return "I'm having trouble connecting right now. Please try again in a moment."

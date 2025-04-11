import re

# List of crisis keywords and phrases to detect
CRISIS_KEYWORDS = [
    r"\bsuicide\b", r"\bkill myself\b", r"\bend my life\b", r"\bgive up\b", 
    r"\bno reason to live\b", r"\bwant to die\b", r"\bdon't want to be here\b",
    r"\bi can't take it\b", r"\bwant to end it all\b", r"\bharm myself\b",
    r"\bhurt myself\b", r"\bend it all\b", r"\bi'm done\b", r"\bno way out\b",
    r"\btired of living\b", r"\bbetter off dead\b", r"\bnobody would miss me\b",
    r"\bfeel worthless\b", r"\bcan't go on\b", r"\bwhat's the point\b", r"\bnothing matters\b",
    r"\bfeel trapped\b", r"\bnever getting better\b", r"\bcan't handle it anymore\b"
]

# Compile all patterns for faster matching
CRISIS_PATTERNS = [re.compile(pattern, re.IGNORECASE) for pattern in CRISIS_KEYWORDS]

# Crisis response message
CRISIS_RESPONSE = """
I'm concerned about what you've shared. Many people go through difficult times like this, and it takes real strength to express these feelings.

If you're having thoughts of harming yourself or feeling in crisis, please reach out to one of these resources:

• National Suicide Prevention Lifeline: 988 or 1-800-273-8255
• Crisis Text Line: Text HOME to 741741
• Veterans Crisis Line: 1-800-273-8255 (Press 1)
• Or go to your nearest emergency room

Reaching out isn't weakness – it's a sign of courage. Trained professionals are available 24/7 to provide support without judgment.

Would you like to talk more about what's going on? I'm here to listen, but please know I'm not a substitute for professional help during a crisis.
"""

def detect_crisis(message):
    """
    Detect if a message contains crisis keywords indicating potential self-harm or suicide risk.
    
    Args:
        message (str): The user's message
        
    Returns:
        tuple: (crisis_detected, response_message) where:
            - crisis_detected (bool): True if crisis keywords detected, False otherwise
            - response_message (str): Crisis response message if crisis detected, None otherwise
    """
    # Check if any crisis pattern matches the message
    for pattern in CRISIS_PATTERNS:
        if pattern.search(message):
            return True, CRISIS_RESPONSE
    
    return False, None

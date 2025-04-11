import os
import json
import logging
from flask import Flask, render_template, request, jsonify, session
from utils.openai_helper import generate_response
from utils.crisis_detector import detect_crisis

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev_secret_key")

# In-memory storage for chat history
conversation_history = {}

@app.route('/')
def index():
    """Render the main chat interface."""
    # Generate a unique session ID if not exists
    if 'session_id' not in session:
        session['session_id'] = os.urandom(16).hex()
    
    session_id = session['session_id']
    
    # Initialize conversation history for this session if not exists
    if session_id not in conversation_history:
        conversation_history[session_id] = []
    
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Process user messages and return AI responses."""
    try:
        data = request.json
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        session_id = session.get('session_id')
        if not session_id:
            return jsonify({'error': 'Session not found'}), 400
        
        # Initialize conversation history for this session if not exists
        if session_id not in conversation_history:
            conversation_history[session_id] = []
        
        # Add user message to history
        conversation_history[session_id].append({"role": "user", "content": user_message})
        
        # Check for crisis keywords
        crisis_detected, crisis_response = detect_crisis(user_message)
        
        if crisis_detected:
            # Add crisis response to history
            conversation_history[session_id].append({"role": "assistant", "content": crisis_response})
            return jsonify({'response': crisis_response, 'crisis_detected': True})
        
        # Generate AI response using OpenAI
        ai_response = generate_response(user_message, conversation_history[session_id])
        
        # Add AI response to history
        conversation_history[session_id].append({"role": "assistant", "content": ai_response})
        
        return jsonify({'response': ai_response, 'crisis_detected': False})
    
    except Exception as e:
        logging.error(f"Error processing chat: {str(e)}")
        return jsonify({'error': 'An error occurred while processing your message'}), 500

@app.route('/api/get_history', methods=['GET'])
def get_history():
    """Return the conversation history for the current session."""
    session_id = session.get('session_id')
    if not session_id or session_id not in conversation_history:
        return jsonify([])
    
    return jsonify(conversation_history[session_id])

@app.route('/api/preset_prompts', methods=['GET'])
def get_preset_prompts():
    """Return the list of preset prompts."""
    preset_prompts = [
        {"id": 1, "text": "I'm struggling with work stress lately.", "category": "work"},
        {"id": 2, "text": "How can I deal with pressure better?", "category": "coping"},
        {"id": 3, "text": "I'd like to talk about my relationship challenges.", "category": "relationships"},
        {"id": 4, "text": "I need help balancing my personal and professional life.", "category": "balance"},
        {"id": 5, "text": "I want to be a better partner but don't know how.", "category": "relationships"},
        {"id": 6, "text": "I'm not sure how to express my feelings.", "category": "expression"},
        {"id": 7, "text": "How can I improve my mental fitness?", "category": "wellness"}
    ]
    return jsonify(preset_prompts)

@app.route('/api/clear_history', methods=['POST'])
def clear_history():
    """Clear the conversation history for the current session."""
    session_id = session.get('session_id')
    if session_id and session_id in conversation_history:
        conversation_history[session_id] = []
    
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8501, debug=True)

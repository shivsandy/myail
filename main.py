
from flask import Flask, render_template, request, jsonify, session
import requests
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "your-secret-key-here"  # Change this to a secure secret key

# Perplexity API configuration
PERPLEXITY_API_URL = "https://api.perplexity.ai/chat/completions"
API_KEY = "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"

# Simple in-memory storage for chat history
chat_sessions = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        session_id = data.get('session_id', 'default')
        
        if session_id not in chat_sessions:
            chat_sessions[session_id] = []
        
        # Add user message to chat history
        chat_sessions[session_id].append({
            "role": "user", 
            "content": user_message,
            "timestamp": datetime.now().isoformat()
        })
        
        # Prepare API request
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        
        api_data = {
            "model": "sonar-pro",
            "messages": [{"role": msg["role"], "content": msg["content"]} 
                        for msg in chat_sessions[session_id]]
        }
        
        # Call Perplexity API
        response = requests.post(PERPLEXITY_API_URL, headers=headers, json=api_data)
        response.raise_for_status()
        
        bot_reply = response.json()['choices'][0]['message']['content']
        
        # Add bot response to chat history
        chat_sessions[session_id].append({
            "role": "assistant", 
            "content": bot_reply,
            "timestamp": datetime.now().isoformat()
        })
        
        return jsonify({
            "success": True,
            "response": bot_reply,
            "message_count": len(chat_sessions[session_id])
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/clear', methods=['POST'])
def clear_chat():
    try:
        data = request.get_json()
        session_id = data.get('session_id', 'default')
        
        if session_id in chat_sessions:
            chat_sessions[session_id] = []
        
        return jsonify({"success": True, "message": "Chat history cleared"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    session_id = request.args.get('session_id', 'default')
    history = chat_sessions.get(session_id, [])
    return jsonify({"history": history})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

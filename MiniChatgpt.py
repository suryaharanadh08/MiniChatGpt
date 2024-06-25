from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Load OpenAI API key from environment variable
openai.api_key ="YOUR OPEN API KEY"

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message")
    if user_message:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_message}
                ]
            )
            reply = response['choices'][0]['message']['content'].strip()
            return jsonify({"reply": reply})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"error": "No message provided"}), 400

@app.route('/')
def home():
    return '''
         <!DOCTYPE html>
        <html>
        <head>
            <title>MINI CHAT GPT</title>
            <style>
                body {
                    font-family: 'Arial', sans-serif;
                    background-color: #f4f4f9;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                }
                #chat-container {
                    background: white;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                    width: 80%;
                    max-width: 1000px;
                    display: flex;
                    flex-direction: column;
                    height: 80vh;
                }
                h1 {
                    margin-top: 0;
                    color: #333;
                    text-align: center;
                }
                #chat-history {
                    flex-grow: 1;
                    overflow-y: auto;
                    margin-bottom: 10px;
                    border: 1px solid #ddd;
                    padding: 10px;
                    border-radius: 4px;
                    background-color: #fafafa;
                }
                .message {
                    margin: 5px 0;
                    padding: 10px;
                    border-radius: 4px;
                    max-width: 75%;
                    position: relative;
                }
                .message .timestamp {
                    position: absolute;
                    bottom: -15px;
                    right: 10px;
                    font-size: 12px;
                    color: #999;
                }
                .user {
                    background-color: #007bff;
                    color: white;
                    text-align: right;
                    margin-left: auto;
                }
                .assistant {
                    background-color: #e2e3e5;
                    color: #333;
                }
                form {
                    display: flex;
                    margin-top: 10px;
                }
                input[type="text"] {
                    flex-grow: 1;
                    padding: 10px;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    font-size: 16px;
                }
                button {
                    padding: 10px 20px;
                    border: none;
                    background-color: #007bff;
                    color: white;
                    border-radius: 4px;
                    font-size: 16px;
                    cursor: pointer;
                    margin-left: 10px;
                }
                button:hover {
                    background-color: #0056b3;
                }
                #clear-btn {
                    margin-top: 10px;
                    background-color: #dc3545;
                }
                #clear-btn:hover {
                    background-color: #c82333;
                }
                #loading {
                    display: none;
                    text-align: center;
                    margin-top: 10px;
                }
            </style>
        </head>
        <body>
            <div id="chat-container">
                <h1>MINI CHAT GPT</h1>
                <div id="chat-history"></div>
                <form id="chatForm">
                    <input type="text" id="message" name="message" placeholder="Type your message..." required>
                    <button type="submit">Send</button>
                </form>
                <button id="clear-btn">Clear Chat</button>
                <div id="loading">Loading...</div>
            </div>
            <script>
                document.getElementById('chatForm').onsubmit = async function(event) {
                    event.preventDefault();
                    const message = document.getElementById('message').value;
                    document.getElementById('loading').style.display = 'block';
                    const response = await fetch('/chat', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ message })
                    });
                    const data = await response.json();
                    document.getElementById('loading').style.display = 'none';
                    addMessage('user', message);
                    if (data.reply) {
                        addMessage('assistant', data.reply);
                    } else {
                        addMessage('assistant', 'Error: ' + data.error);
                    }
                    document.getElementById('message').value = '';
                };

                document.getElementById('message').addEventListener('keypress', function(event) {
                    if (event.key === 'Enter') {
                        event.preventDefault();
                        document.getElementById('chatForm').dispatchEvent(new Event('submit'));
                    }
                });

                document.getElementById('clear-btn').onclick = function() {
                    document.getElementById('chat-history').innerHTML = '';
                };

                function addMessage(role, text) {
                    const chatHistory = document.getElementById('chat-history');
                    const messageElement = document.createElement('div');
                    messageElement.className = 'message ' + role;
                    messageElement.innerText = text;
                    const timestamp = document.createElement('div');
                    timestamp.className = 'timestamp';
                    timestamp.innerText = new Date().toLocaleTimeString();
                    messageElement.appendChild(timestamp);
                    chatHistory.appendChild(messageElement);
                    chatHistory.scrollTop = chatHistory.scrollHeight;
                }
            </script>
        </body>
        </html>
    '''

if __name__ == '__main__':
    app.run(debug=True)

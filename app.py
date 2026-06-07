# Flask App for the Local LLM Chatbot
# This file sets up a simple web server using Flask.
# It defines routes that the browser can call to send messages to the AI, clear the conversation, and get the conversation history.
# It uses the functions defined in ollama_client.py to handle the actual communication with the Ollama AI.
from flask import Flask, render_template, request, jsonify
from ollama_client import chat, clear_history, get_history

# Create the Flask app
# Think of this as "starting the restaurant"
app = Flask(__name__)

# ─────────────────────────────────────────
# ROUTE 1: The main page
# When you open http://localhost:5000 in your browser,
# Flask serves the chat UI (index.html)
# ─────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")


# ─────────────────────────────────────────
# ROUTE 2: Send a message to the AI
# When you hit Send in the browser, JavaScript
# calls this route with your message
# ─────────────────────────────────────────
@app.route("/chat", methods=["POST"])
def chat_route():
    # Get the data sent from the browser
    data = request.get_json()

    # Extract the message and model name
    user_message = data.get("message", "")
    model = data.get("model", "llama3.1")

    # Basic check — don't process empty messages
    if not user_message.strip():
        return jsonify({"error": "Empty message"}), 400

    # Send to ollama_client.py and get the AI's reply
    response = chat(user_message, model)

    # Send the reply back to the browser as JSON
    return jsonify({"response": response})


# ─────────────────────────────────────────
# ROUTE 3: Clear the conversation
# When you click "New Chat", this resets history
# ─────────────────────────────────────────
@app.route("/clear", methods=["POST"])
def clear_route():
    clear_history()
    return jsonify({"status": "History cleared"})


# ─────────────────────────────────────────
# ROUTE 4: Get full conversation history
# Optional — useful for debugging
# ─────────────────────────────────────────
@app.route("/history", methods=["GET"])
def history_route():
    return jsonify(get_history())


# ─────────────────────────────────────────
# Start the server
# debug=True means it auto-restarts when you save changes
# ─────────────────────────────────────────
if __name__ == "__main__":
    print("🚀 Local LLM Chatbot is running!")
    print("👉 Open your browser and go to: http://localhost:5000")
    app.run(debug=True)
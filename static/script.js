// ─────────────────────────────────────────
// This is the file that makes everything interactive.
// Without this, clicking Send would do nothing.
// This file is the bridge between what you see (the UI) and your Flask server.
// ─────────────────────────────────────────
// ─────────────────────────────────────────
// GRAB ALL THE HTML ELEMENTS WE NEED
// Think of these like variables pointing to
// specific parts of your chat page
// ─────────────────────────────────────────
const chatWindow = document.getElementById("chat-window");
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");
const modelSelect = document.getElementById("model-select");
const newChatBtn = document.getElementById("new-chat-btn");

// ─────────────────────────────────────────
// DARK / LIGHT MODE TOGGLE
// Adds or removes the "dark" class on body
// CSS variables automatically swap colors
// ─────────────────────────────────────────
function toggleTheme() {
    document.body.classList.toggle("dark");

    // Remember the user's preference in browser storage
    // So next time they open the app, theme is preserved
    const isDark = document.body.classList.contains("dark");
    localStorage.setItem("theme", isDark ? "dark" : "light");
}

// When page loads, check if user previously chose dark mode
function loadTheme() {
    const saved = localStorage.getItem("theme");
    if (saved === "dark") {
        document.body.classList.add("dark");
        // Also update the toggle switch position
        const toggle = document.getElementById("theme-toggle-input");
        if (toggle) toggle.checked = true;
    }
}

// ─────────────────────────────────────────
// ADD A MESSAGE BUBBLE TO THE CHAT WINDOW
// role = "user" → right side blue bubble
// role = "ai"   → left side dark bubble
// ─────────────────────────────────────────
function addMessage(content, role) {
    // Create the outer wrapper div
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message");
    messageDiv.classList.add(role === "user" ? "user-message" : "ai-message");

    // Create the bubble itself
    const bubble = document.createElement("div");
    bubble.classList.add("message-bubble");

    // If it's an AI message, render line breaks properly
    if (role === "ai") {
        bubble.innerHTML = formatMessage(content);
    } else {
        bubble.textContent = content;
    }

    // Put bubble inside wrapper, wrapper inside chat window
    messageDiv.appendChild(bubble);
    chatWindow.appendChild(messageDiv);

    // Auto-scroll to the latest message
    chatWindow.scrollTop = chatWindow.scrollHeight;

    return bubble;
}

// ─────────────────────────────────────────
// FORMAT AI MESSAGES
// Converts plain text to readable HTML
// Handles code blocks, bold, line breaks
// ─────────────────────────────────────────
function formatMessage(text) {
    // Convert **bold** to <strong>bold</strong>
    text = text.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");

    // Convert `code` to styled inline code
    text = text.replace(/`([^`]+)`/g, "<code style='background:rgba(79,70,229,0.1);padding:2px 6px;border-radius:4px;font-size:13px;'>$1</code>");

    // Convert line breaks to <br> tags
    text = text.replace(/\n/g, "<br>");

    return text;
}

// ─────────────────────────────────────────
// SHOW TYPING INDICATOR
// The 3 bouncing dots while AI is thinking
// ─────────────────────────────────────────
function showTypingIndicator() {
    const typingDiv = document.createElement("div");
    typingDiv.classList.add("message", "ai-message");
    typingDiv.id = "typing-indicator";

    typingDiv.innerHTML = `
        <div class="typing-indicator">
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        </div>
    `;

    chatWindow.appendChild(typingDiv);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

// ─────────────────────────────────────────
// REMOVE TYPING INDICATOR
// Called once AI response arrives
// ─────────────────────────────────────────
function removeTypingIndicator() {
    const indicator = document.getElementById("typing-indicator");
    if (indicator) indicator.remove();
}

// ─────────────────────────────────────────
// SEND MESSAGE — the main function
// This runs every time you click Send
// or press Enter
// ─────────────────────────────────────────
async function sendMessage() {
    // Get what the user typed and clean it up
    const message = userInput.value.trim();

    // Don't send if empty
    if (!message) return;

    // Get selected model from dropdown
    const model = modelSelect.value;

    // Show user's message as a bubble on the right
    addMessage(message, "user");

    // Clear the input box
    userInput.value = "";
    userInput.style.height = "auto";

    // Disable send button while waiting for AI
    // Prevents sending multiple messages at once
    sendBtn.disabled = true;
    sendBtn.textContent = "Sending...";

    // Show the typing dots
    showTypingIndicator();

    try {
        // ── Send message to Flask server ──
        // fetch() is like making a phone call to app.py
        // We send the message and model as JSON
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: message,
                model: model
            })
        });

        // Convert the response to JSON
        const data = await response.json();

        // Remove typing dots
        removeTypingIndicator();

        if (data.response) {
            // Show AI's reply as a bubble on the left
            addMessage(data.response, "ai");
        } else if (data.error) {
            addMessage("⚠️ Error: " + data.error, "ai");
        }

    } catch (error) {
        // Something went wrong (e.g. Flask not running)
        removeTypingIndicator();
        addMessage("⚠️ Could not reach the server. Is Flask running?", "ai");
    }

    // Re-enable send button
    sendBtn.disabled = false;
    sendBtn.textContent = "Send ➤";
}

// ─────────────────────────────────────────
// NEW CHAT — clears everything
// Calls Flask's /clear route and wipes UI
// ─────────────────────────────────────────
async function newChat() {
    // Tell Flask to clear conversation history
    await fetch("/clear", { method: "POST" });

    // Clear all messages from the chat window
    chatWindow.innerHTML = "";

    // Show fresh welcome message
    addMessage("👋 New chat started! How can I help you?", "ai");
}

// ─────────────────────────────────────────
// HANDLE ENTER KEY
// Enter = send message
// Shift + Enter = new line (don't send)
// ─────────────────────────────────────────
function handleKeyPress(event) {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault(); // Stop Enter from adding a new line
        sendMessage();
    }
}

// ─────────────────────────────────────────
// AUTO-RESIZE TEXTAREA
// Grows as you type more text
// ─────────────────────────────────────────
userInput.addEventListener("input", function () {
    this.style.height = "auto";
    this.style.height = Math.min(this.scrollHeight, 120) + "px";
});

// ─────────────────────────────────────────
// ADD THEME TOGGLE TO SIDEBAR
// Injects the toggle switch HTML into sidebar
// ─────────────────────────────────────────
function addThemeToggle() {
    const sidebar = document.querySelector(".sidebar");

    const toggleHTML = `
        <div class="theme-toggle">
            <span>🌙 Dark Mode</span>
            <label class="toggle-switch">
                <input type="checkbox" id="theme-toggle-input" onchange="toggleTheme()">
                <span class="toggle-slider"></span>
            </label>
        </div>
    `;

    // Insert before the privacy note
    const privacyNote = sidebar.querySelector(".privacy-note");
    privacyNote.insertAdjacentHTML("beforebegin", toggleHTML);
}

// ─────────────────────────────────────────
// RUN WHEN PAGE LOADS
// ─────────────────────────────────────────
window.onload = function () {
    loadTheme();      // Apply saved theme
    addThemeToggle(); // Add dark mode toggle to sidebar
    userInput.focus(); // Auto-focus the input box
};
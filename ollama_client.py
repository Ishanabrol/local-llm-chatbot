# What This File Does ?
# Connects to Ollama running on your laptop
# Sends your message to the AI
# Remembers the full conversation history (so the AI knows what was said before)
# Returns the AI's response back to your app
import ollama
import requests
from datetime import datetime

# ─────────────────────────────────────────
# CONVERSATION HISTORY
# Stores the full chat so AI remembers context
# ─────────────────────────────────────────
conversation_history = []


# ─────────────────────────────────────────
# FEATURE 1 — DATE & TIME
# Reads your system clock — no internet needed
# ─────────────────────────────────────────
def get_datetime():
    now = datetime.now()
    return now.strftime("Today is %A, %d %B %Y. The current time is %I:%M %p.")


# ─────────────────────────────────────────
# FEATURE 2 — WEATHER
# Uses Open-Meteo (free, no API key needed)
# We first convert city name to coordinates
# then fetch weather for those coordinates
# ─────────────────────────────────────────
def get_weather(city="Delhi"):
    try:
        # Step 1: Convert city name to latitude/longitude
        # Open-Meteo needs coordinates, not city names
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
        geo_response = requests.get(geo_url, timeout=5)
        geo_data = geo_response.json()

        # If city not found, return an error message
        if not geo_data.get("results"):
            return f"Sorry, I couldn't find weather data for '{city}'."

        # Extract coordinates from the response
        lat = geo_data["results"][0]["latitude"]
        lon = geo_data["results"][0]["longitude"]
        city_name = geo_data["results"][0]["name"]
        country = geo_data["results"][0].get("country", "")

        # Step 2: Fetch actual weather using coordinates
        weather_url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}"
            f"&current=temperature_2m,relative_humidity_2m,"
            f"wind_speed_10m,weather_code"
            f"&timezone=auto"
        )
        weather_response = requests.get(weather_url, timeout=5)
        weather_data = weather_response.json()

        # Extract the values we need
        current = weather_data["current"]
        temp = current["temperature_2m"]
        humidity = current["relative_humidity_2m"]
        wind = current["wind_speed_10m"]
        code = current["weather_code"]

        # Convert weather code to human readable condition
        condition = weather_code_to_text(code)

        return (
            f"Current weather in {city_name}, {country}:\n"
            f"Condition: {condition}\n"
            f"Temperature: {temp}°C\n"
            f"Humidity: {humidity}%\n"
            f"Wind Speed: {wind} km/h"
        )

    except Exception as e:
        return f"Sorry, I couldn't fetch weather data right now. Error: {str(e)}"


def weather_code_to_text(code):
    """
    Open-Meteo returns a number for weather condition.
    This converts it to plain English.
    """
    if code == 0:
        return "Clear sky ☀️"
    elif code in [1, 2, 3]:
        return "Partly cloudy ⛅"
    elif code in [45, 48]:
        return "Foggy 🌫️"
    elif code in [51, 53, 55]:
        return "Drizzle 🌦️"
    elif code in [61, 63, 65]:
        return "Rainy 🌧️"
    elif code in [71, 73, 75]:
        return "Snowy ❄️"
    elif code in [80, 81, 82]:
        return "Rain showers 🌨️"
    elif code in [95, 96, 99]:
        return "Thunderstorm ⛈️"
    else:
        return "Unknown condition"


# ─────────────────────────────────────────
# FEATURE 3 — WEB SEARCH
# Uses DuckDuckGo Instant Answer API
# Completely free, no signup, no API key
# Best for factual one-line answers
# ─────────────────────────────────────────
def web_search(query):
    try:
        # DuckDuckGo instant answer API
        url = f"https://api.duckduckgo.com/?q={query}&format=json&no_html=1"
        response = requests.get(url, timeout=5)
        data = response.json()

        # Try to get the best available answer
        # DuckDuckGo returns different fields depending on query type
        if data.get("AbstractText"):
            # Full summary paragraph (best result)
            return f"Web result: {data['AbstractText']} (Source: {data.get('AbstractSource', 'DuckDuckGo')})"

        elif data.get("Answer"):
            # Direct instant answer e.g. calculations, conversions
            return f"Web result: {data['Answer']}"

        elif data.get("RelatedTopics"):
            # Grab first related topic if no direct answer
            first = data["RelatedTopics"][0]
            if isinstance(first, dict) and first.get("Text"):
                return f"Web result: {first['Text']}"

        # Nothing useful found
        return "I searched the web but couldn't find a specific answer for that. Try rephrasing your question."

    except Exception as e:
        return f"Sorry, web search failed right now. Error: {str(e)}"


# ─────────────────────────────────────────
# DETECT WHAT KIND OF QUESTION WAS ASKED
# Looks for keywords to decide which
# real-time feature to trigger
# ─────────────────────────────────────────
def detect_intent(message):
    message_lower = message.lower()

    # Date/time keywords
    date_keywords = [
        "what time", "what's the time", "current time",
        "what date", "today's date", "what day", "day is it",
        "what is today", "current date"
    ]

    # Weather keywords
    weather_keywords = [
        "weather", "temperature", "humid", "rain",
        "sunny", "cloudy", "forecast", "wind", "hot", "cold"
    ]

    # Search keywords
    search_keywords = [
        "search", "look up", "find", "who is", "what is",
        "tell me about", "information about", "latest",
        "news about", "google"
    ]

    if any(k in message_lower for k in date_keywords):
        return "datetime"

    if any(k in message_lower for k in weather_keywords):
        return "weather"

    if any(k in message_lower for k in search_keywords):
        return "search"

    return "chat"  # Default — just chat normally


# ─────────────────────────────────────────
# EXTRACT CITY FROM WEATHER QUESTION
# e.g. "weather in Mumbai" → "Mumbai"
# ─────────────────────────────────────────
def extract_city(message):
    message_lower = message.lower()

    # Common patterns for city extraction
    patterns = ["weather in ", "temperature in ", "forecast for "]

    for pattern in patterns:
        if pattern in message_lower:
            # Get everything after the pattern
            city = message_lower.split(pattern)[-1]
            # Clean up punctuation and extra words
            city = city.split("?")[0].split(".")[0].strip()
            return city.title()  # Capitalize first letter

    # Default to Delhi if no city found
    return "Delhi"


# ─────────────────────────────────────────
# EXTRACT SEARCH QUERY
# e.g. "search for black holes" → "black holes"
# ─────────────────────────────────────────
def extract_search_query(message):
    message_lower = message.lower()

    remove_phrases = [
        "search for ", "look up ", "find ", "search ",
        "google ", "tell me about ", "information about ",
        "news about ", "what is ", "who is "
    ]

    for phrase in remove_phrases:
        if message_lower.startswith(phrase):
            return message[len(phrase):].strip()

    return message.strip()


# ─────────────────────────────────────────
# MAIN CHAT FUNCTION
# This is called by app.py every time
# you send a message
# ─────────────────────────────────────────
def chat(user_message, model="llama3.1"):

    # Step 1: Detect what kind of question this is
    intent = detect_intent(user_message)

    # Step 2: Fetch real-time data if needed
    real_time_context = ""

    if intent == "datetime":
        real_time_context = get_datetime()

    elif intent == "weather":
        city = extract_city(user_message)
        real_time_context = get_weather(city)

    elif intent == "search":
        query = extract_search_query(user_message)
        real_time_context = web_search(query)

    # Step 3: Build the message to send to Llama
    # If we have real-time data, prepend it as context
    # So Llama uses real data in its reply
    if real_time_context:
        full_message = (
            f"[Real-time data fetched for you]\n"
            f"{real_time_context}\n\n"
            f"Using the above real-time information, "
            f"please answer this question naturally: {user_message}"
        )
    else:
        full_message = user_message

    # Step 4: Add to conversation history
    conversation_history.append({
        "role": "user",
        "content": full_message
    })

    # Step 5: Send to Ollama and get response
    response = ollama.chat(
        model=model,
        messages=conversation_history
    )

    ai_message = response["message"]["content"]

    # Step 6: Save AI reply to history
    conversation_history.append({
        "role": "assistant",
        "content": ai_message
    })

    return ai_message


# ─────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────
def clear_history():
    global conversation_history
    conversation_history = []


def get_history():
    return conversation_history
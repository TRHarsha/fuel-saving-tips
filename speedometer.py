import streamlit as st
import time
import random
import os
import google.generativeai as genai

# Directly set the API key
api_key = 'AIzaSyCSblJhwW5i44o0-S_ltouuW4X8C2dSjXU'  # Replace with your actual API key

if not api_key:
    raise ValueError("API key not found. Please set the GOOGLE_API_KEY in the script.")

genai.configure(api_key=api_key)

# Function to load Gemini Pro model and get responses
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

# Set initial values
min_speed = 0
max_speed = 200
fuel_capacity = random.uniform(60, 70)
fuel_level = fuel_capacity
fuel_consumption_rate = 0.05  # Fuel consumption per update

# Create placeholders for speed and fuel level
speed_placeholder = st.empty()
fuel_placeholder = st.empty()
response_placeholder = st.empty()

# Function to simulate speed change
def get_new_speed(current_speed):
    change = random.uniform(-5, 5)
    new_speed = current_speed + change
    return max(min_speed, min(new_speed, max_speed))

# Initialize the current speed
current_speed = 0

# Simulate vehicle operation
while fuel_level > 0:
    # Update speed
    current_speed = get_new_speed(current_speed)
    
    # Update fuel level based on current speed
    fuel_consumed = (current_speed / max_speed) * fuel_consumption_rate
    fuel_level -= fuel_consumed
    fuel_level = max(0, fuel_level)  # Ensure fuel level doesn't go below 0

    # Display current speed and fuel level
    speed_placeholder.markdown(f"### Speed: {current_speed:.2f} Km/Hr")
    fuel_placeholder.markdown(f"### Fuel Level: {fuel_level:.2f} Litres")

    # Create input text
    input_text = f"I am driving the vehicle at {current_speed:.2f} Km/Hr and with {fuel_level:.2f} Litres. Suggest me one liner tips."
    response = get_gemini_response(input_text)

    # Display response
    response_placeholder.subheader("The Response is")
    for chunk in response:
        response_placeholder.write(chunk.text)

    # Pause for a short duration to simulate real-time update
    time.sleep(1)
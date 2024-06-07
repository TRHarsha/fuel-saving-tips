import streamlit as st
import time
import random
import google.generativeai as genai
import pyttsx3

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

# Function to simulate speed change
def get_new_speed(current_speed):
    change = random.uniform(-5, 5)
    new_speed = current_speed + change
    return max(min_speed, min(new_speed, max_speed))

# Set initial values
min_speed = 0
max_speed = 200
fuel_capacity = random.uniform(60, 70)
fuel_consumption_rate = 0.05  # Fuel consumption per update

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Initialize session state
if 'current_speed' not in st.session_state:
    st.session_state.current_speed = 0

if 'fuel_level' not in st.session_state:
    st.session_state.fuel_level = fuel_capacity

if 'running' not in st.session_state:
    st.session_state.running = False

# Create placeholders for speed and fuel level
speed_placeholder = st.empty()
fuel_placeholder = st.empty()
response_placeholder = st.empty()

# Buttons
if st.session_state.running:
    stop = st.button("Stop")
else:
    start = st.button("Start")

if not st.session_state.running and 'start' in locals() and start:
    st.session_state.running = True
    st.session_state.current_speed = 0
    st.session_state.fuel_level = fuel_capacity
    response_placeholder.empty()

if st.session_state.running and 'stop' in locals() and stop:
    st.session_state.running = False
    input_text = f"I am driving the vehicle at {st.session_state.current_speed:.2f} Km/Hr and with {st.session_state.fuel_level:.2f} Litres. Suggest me one line fuel saving tip."
    response = get_gemini_response(input_text)

    # Display response
    response_placeholder.subheader("The Response is")
    for chunk in response:
        response_text = chunk.text
        response_placeholder.write(response_text)

        # Convert response to speech
        engine.say(response_text)
        engine.runAndWait()

while st.session_state.running and st.session_state.fuel_level > 0:
    # Update speed
    st.session_state.current_speed = get_new_speed(st.session_state.current_speed)

    # Update fuel level based on current speed
    fuel_consumed = (st.session_state.current_speed / max_speed) * fuel_consumption_rate
    st.session_state.fuel_level -= fuel_consumed
    st.session_state.fuel_level = max(0, st.session_state.fuel_level)  # Ensure fuel level doesn't go below 0

    # Display current speed and fuel level
    speed_placeholder.markdown(f"### Speed: {st.session_state.current_speed:.2f} Km/Hr")
    fuel_placeholder.markdown(f"### Fuel Level: {st.session_state.fuel_level:.2f} Litres")

    # Pause for a short duration to simulate real-time update
    time.sleep(1)

    # Refresh the page
    st.experimental_rerun()

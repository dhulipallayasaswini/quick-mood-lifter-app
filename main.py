import streamlit as st
import requests
import os

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

def get_mood_lifter(age, mood, time_available):
    url = "https://api.together.xyz/v1/completions"
    prompt = f"""Suggest a quick micro-therapy exercise and a positive motivational quote.
User details:
- Age: {age}
- Mood: {mood}
- Time available: {time_available} minutes.
Suggest a simple relaxing micro-therapy exercise the user can do quickly.
List the Micro-therapy excercises in numbered list.This helps the user to clearly focus on action.
Make a distinction between the excercise and joke or quote by writing the joke or quote in Italics. 
Make the tone friendly, casual, and uplifting. 
Sometimes add a light joke or a positive motivational quote at the end in quotation marks."""
    
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "meta-llama/Llama-3-8b-chat-hf",
        "prompt": prompt,
        "max_tokens": 300,
        "temperature": 0.8,
        "top_p": 0.9
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        res_json = response.json()
        if "choices" in res_json and len(res_json["choices"]) > 0:
            return res_json["choices"][0]["text"].strip()
        else:
            return "No suggestion found. Please try again."
    except Exception as e:
        return f"Error: {e}"
st.set_page_config(page_title="Quick Mood Lifter", page_icon="🌈", layout="centered")
st.title("🌈 Quick Mood Lifter")

age = st.number_input("Enter your age:", min_value=5, max_value=100, step=1, value=5)
mood = st.selectbox("How are you feeling right now?", ["","Happy", "Sad", "Stressed", "Anxious", "Overwhelmed", "Tired", "Excited", "Bored", "Lonely", "Motivated"])
time_available = st.selectbox("How much time can you spend on yourself right now?", ["","2 minutes", "5 minutes", "10 minutes", "15 minutes", "20 minutes"])

if st.button("Get My Therapy Tip"):
    if age and mood and time_available:
        with st.spinner("Finding the perfect lift for you..."):
            output = get_mood_lifter(age, mood, time_available)
        st.success("Here’s your quick boost!")
        st.write(output)
    else:
        st.warning("Please fill out all fields.")

st.markdown("---")
st.caption("Powered by Together.ai LLM • Built with Streamlit • Hosted on Render")
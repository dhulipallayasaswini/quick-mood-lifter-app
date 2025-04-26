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

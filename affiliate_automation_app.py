import streamlit as st
import json
import csv
import random
from datetime import datetime, timedelta
import pandas as pd
import time
import re

# FastAPI integration
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.middleware.wsgi import WSGIMiddleware
from streamlit.web.server import Server

# ------------------ FASTAPI LIVE ENDPOINT ------------------ #
CONTENT_POOL = [
    {
        "platform": "Reddit",
        "title": "PSA: These resistance bands helped me lose 30lbs without a gym",
        "content": "I didn’t think bands would work. But now I’m down 30lbs in 4 months. Game changer. [affiliate link here]"
    },
    {
        "platform": "Pinterest",
        "title": "💪 These $15 Resistance Bands Replaced My Entire Gym!",
        "description": "Saved me $1200/year. Perfect for busy moms or small spaces. #homeworkout #fitness #affiliate"
    },
    {
        "platform": "TikTok",
        "script": "POV: You found the $15 resistance bands that replaced your gym ✨\n\n*Shows before/after*\n\nLink in bio! #fitness #musthave"
    }
]

api_app = FastAPI()

@api_app.get("/api/fetch_content")
def fetch_content():
    sample = random.sample(CONTENT_POOL, 2)
    return JSONResponse(content=sample)

# Attach FastAPI to Streamlit via ASGI
Server.get_current()._set_app_asgi_app(WSGIMiddleware(api_app))

# ------------------ STREAMLIT UI START ------------------ #
st.set_page_config(page_title="Affiliate Automation Hub", layout="wide")

st.title("🧠 Affiliate Automation with Built-In API")

if st.button("📡 Fetch Live Content from Endpoint"):
    try:
        import requests
        response = requests.get("http://localhost:8501/api/fetch_content")
        if response.status_code == 200:
            content = response.json()
            st.success("Fetched content from live endpoint:")
            for item in content:
                st.json(item)
        else:
            st.error("Failed to fetch data from the live endpoint.")
    except Exception as e:
        st.error(f"Error: {e}")

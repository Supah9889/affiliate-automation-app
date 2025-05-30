# === Imports ===
import streamlit as st
import requests

# === Function to Fetch From External FastAPI ===
def fetch_live_content():
    try:
        response = requests.get("https://FastAPIContent--seanhargain055.repl.co/api/fetch_content")
        if response.status_code == 200:
            return response.json()
        else:
            return [{"error": f"Status code: {response.status_code}"}]
    except Exception as e:
        return [{"error": f"API error: {e}"}]

# === Streamlit UI ===
st.set_page_config(page_title="Affiliate Automation Hub", layout="wide")
st.title("🧠 Affiliate Automation with Built-In API")

if st.button("🌐 Fetch Live API Content"):
    content = fetch_live_content()
    for item in content:
        st.json(item)

# You can build more features under here later

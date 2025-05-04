import streamlit as st
import uvicorn
from fastapi import FastAPI
import requests

#  Create a FastAPI app
app = FastAPI()

@app.get("/hello")
def get_hello():
    return {"message": "Hello, World!"}

def run_fastapi():
    uvicorn.run(app, host="0.0.0.0", port=8000)

import threading
api_thread = threading.Thread(target=run_fastapi)
api_thread.start()

st.title("FastAPI with Streamlit")
if st.button("Get Hello"):
    response = requests.get("http://localhost:8000/hello")
    if response.status_code == 200:
        st.success(response.json()["message"])
    else:
        st.error("Failed to get response from FastAPI")

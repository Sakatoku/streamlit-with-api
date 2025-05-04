import streamlit as st
# import uvicorn
# from fastapi import FastAPI
# import requests
import json

from streamlit_card import card
import inspect

# class OverrideComponentRequestHandler(st.web.server.component_request_handler.ComponentRequestHandler):

def new_component_request_handler_get(self, path: str) -> None:
    print("Custom handler for path:", path)
    if path == "api":
        # サンプルのJSONを出力する
        sample_response = {
            "message": "Hello from Streamlit!",
            "data": [1, 2, 3, 4, 5]
        }
        json_response = json.dumps(sample_response).encode("utf-8")
        self.write(json_response)
        self.set_status(200)
        self.set_header("Content-Type", "application/json")
        self.set_header("Cache-Control", "no-cache")
        if st.web.server.routes.allow_cross_origin_requests():
            self.set_header("Access-Control-Allow-Origin", "*")
    else:
        print("Calling original handler...")
        st.web.server.component_request_handler.ComponentRequestHandler.original_get(self, path)
    # elif "original_handler" in st.session_state:
    #     print("Calling original handler...")
    #     st.session_state.original_handler(self, path)
    # else:
    #     print("No original handler found.")
    #     print(st.session_state)

import fasteners
with fasteners.InterProcessLock("/tmp/lockfile"):
    print("Lock acquired")
    if st.web.server.component_request_handler.ComponentRequestHandler.get.__module__ == "streamlit.web.server.component_request_handler":
        st.web.server.component_request_handler.ComponentRequestHandler.original_get = st.web.server.component_request_handler.ComponentRequestHandler.get
        st.web.server.component_request_handler.ComponentRequestHandler.get = new_component_request_handler_get
        # st.session_state.original_handler = st.web.server.component_request_handler.ComponentRequestHandler.get
        print("Original handler saved")
    else:
        print("Original handler already saved")
    # st.web.server.component_request_handler.ComponentRequestHandler.get = new_component_request_handler_get

st.write(inspect.getfile(st.web.server.component_request_handler.ComponentRequestHandler.get))
st.write(st.web.server.component_request_handler.ComponentRequestHandler.get.__code__.co_filename)
st.write(st.web.server.component_request_handler.ComponentRequestHandler.get.__module__)
st.write(inspect.signature(st.web.server.component_request_handler.ComponentRequestHandler.get))

st.title("FastAPI with Streamlit")

hasClicked = card(
  title="Hello World!",
  text="Some description",
  image="http://placekitten.com/200/300",
  url="https://github.com/gamcoh/st-card"
)

st.write(st.session_state)

# import tornado.web
# _server_old_carete_app = st.web.server.Server._create_app
# def _server_new_create_app(self) -> tornado.web.Application:
#     print("Creating app...")
#     return _server_old_carete_app(self)
# st.web.server.Server._create_app = _server_new_create_app

st.write(st.web.server.component_request_handler.ComponentRequestHandler.get)

# #  Create a FastAPI app
# app = FastAPI()

# @app.get("/hello")
# def get_hello():
#     return {"message": "Hello, World!"}

# def run_fastapi():
#     uvicorn.run(app, host="0.0.0.0", port=8000)

# import threading
# api_thread = threading.Thread(target=run_fastapi)
# api_thread.start()

# st.title("FastAPI with Streamlit")
# if st.button("Get Hello"):
#     response = requests.get("http://localhost:8000/hello")
#     if response.status_code == 200:
#         st.success(response.json()["message"])
#     else:
#         st.error("Failed to get response from FastAPI")

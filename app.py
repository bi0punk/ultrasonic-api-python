from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import json
import socketio

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
sio = socketio.AsyncServer(cors_allowed_origins="*")

app.mount("/socket.io", socketio.ASGIApp(sio))

latest_data = {}

@app.post("/data")
async def receive_data(data: dict):
    global latest_data
    latest_data = data
    print("Received data:", data)  # Print data to console
    return {"message": "Data received successfully"}

@app.get("/", response_class=HTMLResponse)
async def show_data(request: Request):
    with open("index.html", "r") as file:
        html_content = file.read()
    return html_content

@app.get("/get_latest_data")
async def get_latest_data():
    return latest_data

@sio.event
async def connect(sid, environ):
    print(f"Connected: {sid}")

@sio.event
async def disconnect(sid):
    print(f"Disconnected: {sid}")

@sio.event
async def update_distance(sid, data):
    await sio.emit("update_distance", data)

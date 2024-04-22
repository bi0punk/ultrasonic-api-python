from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import json
import socketio

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
sio = socketio.AsyncServer(cors_allowed_origins="*")
app.mount("/socket.io", socketio.ASGIApp(sio))

# Estructura de datos compartida
latest_data = {"distance": 0}

# Decorador para registrar eventos de Socket.IO automáticamente
def register_event(event_name):
    def decorator(func):
        setattr(sio, event_name, func)
        return func
    return decorator

@register_event("connect")
async def connect(sid, environ):
    print(f"Connected: {sid}")

@register_event("disconnect")
async def disconnect(sid):
    print(f"Disconnected: {sid}")

@register_event("update_distance")
async def update_distance(sid, data):
    await sio.emit("update_distance", data)

@app.post("/data")
async def receive_data(data: dict):
    global latest_data
    latest_data = data
    print("Received data:", data)
    return {"message": "Data received successfully"}

@app.get("/", response_class=HTMLResponse)
async def show_data(request: Request):
    try:
        with open("index.html", "r") as file:
            html_content = file.read()
    except FileNotFoundError:
        return HTMLResponse(content="File not found", status_code=404)
    return HTMLResponse(content=html_content)

@app.get("/get_latest_data")
async def get_latest_data():
    distance = latest_data.get("distance", 0)
    return JSONResponse(content={"distance": distance})

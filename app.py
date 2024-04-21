from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import json
import socketio

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
sio = socketio.AsyncServer(cors_allowed_origins="*")

app.mount("/socket.io", socketio.ASGIApp(sio))

latest_data = {"progress": 0}  # Inicializamos el progreso a 0

@app.post("/data")
async def receive_data(data: dict):
    global latest_data
    latest_data = data
    print("Received data:", data)  # Imprimir datos en la consola
    return {"message": "Data received successfully"}

@app.get("/", response_class=HTMLResponse)
async def show_data(request: Request):
    with open("index.html", "r") as file:
        html_content = file.read()
    return html_content

@app.get("/get_latest_data")
async def get_latest_data():
    global latest_data
    progress = latest_data.get("distance", 0)  # Obtener el valor de distancia (progreso)
    progress_percent = min(progress, 100)  # Limitar el progreso a un máximo del 100%
    return JSONResponse(content={"progress": progress_percent})

@sio.event
async def connect(sid, environ):
    print(f"Connected: {sid}")

@sio.event
async def disconnect(sid):
    print(f"Disconnected: {sid}")

@sio.event
async def update_distance(sid, data):
    await sio.emit("update_distance", data)

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import json

app = FastAPI()

# Configuración para servir archivos estáticos (como CSS, JS, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Variable para almacenar el último dato recibido del Arduino
latest_data = {}

# Ruta para recibir los datos JSON del Arduino
@app.post("/data")
async def receive_data(data: dict):
    global latest_data
    latest_data = data
    return {"message": "Data received successfully"}

# Ruta para mostrar el valor más reciente en una página HTML
@app.get("/", response_class=HTMLResponse)
async def show_data(request: Request):
    with open("index.html", "r") as file:
        html_content = file.read()
    return html_content

# Ruta para obtener el último dato en formato JSON
@app.get("/get_latest_data")
async def get_latest_data():
    return latest_data

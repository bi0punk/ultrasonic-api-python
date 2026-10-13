import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

app = FastAPI()

# Orígenes permitidos por entorno (separados por coma). Default: solo localhost.
# Nota: con allow_credentials=False no se puede usar "*" si se usan credenciales.
_origins = [
    o.strip()
    for o in os.environ.get("CORS_ORIGINS", "http://localhost:8080").split(",")
    if o.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Variable para almacenar el último dato recibido del Arduino
latest_data: dict = {}


# Ruta para recibir los datos JSON del Arduino
@app.post("/data")
async def receive_data(data: dict):
    global latest_data
    latest_data = data
    return {"message": "Data received successfully"}


# Ruta para mostrar el valor más reciente en una página HTML
@app.get("/", response_class=HTMLResponse)
async def show_data():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Arduino Data</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-ywqiZw8pPvC3giC3PEpt3u5ZrO80iI0LQy8ZymzxI1ViTm8oV7fyQHiXs4D6vCBm" crossorigin="anonymous">
    </head>
    <body>
        <div class="container">
            <h1 class="mt-5">Arduino Data</h1>
            <div id="data-container" class="mt-3">
                <p id="data-value" class="lead"></p>
            </div>
        </div>
    </body>
    <script>
        // Función para actualizar el valor en la página
        function updateData() {
            fetch('/get_latest_data')
                .then(response => response.json())
                .then(data => {
                    const dataValue = document.getElementById('data-value');
                    dataValue.textContent = JSON.stringify(data);
                });
        }
        // Actualizar el valor cada 5 segundos
        setInterval(updateData, 1000);
        // Iniciar la actualización del valor al cargar la página
        updateData();
    </script>
    </html>
    """


# Ruta para obtener el último dato en formato JSON
@app.get("/get_latest_data")
async def get_latest_data():
    return latest_data

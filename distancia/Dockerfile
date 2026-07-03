# Usa la imagen base de Python
FROM python:3.10

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia los archivos de requerimientos al contenedor
COPY requirements.txt .

# Instala las dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el código al contenedor
COPY . .

# Define el comando por defecto para ejecutar tu aplicación
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]

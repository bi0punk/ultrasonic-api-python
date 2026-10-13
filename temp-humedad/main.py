import os
import shutil
import subprocess
import threading

from flask import Flask, jsonify, render_template, request
from gtts import gTTS

app = Flask(__name__)

sensor_data: list[dict] = []  # Lista para almacenar los datos recibidos
sensor_data_lock = threading.Lock()


def send_voice_notification(message):
    tts = gTTS(text=message, lang="en")
    tts.save("notification.mp3")
    mpg123 = shutil.which("mpg123")
    if mpg123 is None:
        print("mpg123 no está instalado; no se reproducirá la notificación.")
        return
    subprocess.run(
        [mpg123, "notification.mp3"]
    )  # Asegúrate de tener el reproductor mpg123 instalado


@app.route("/api", methods=["POST"])
def receive_sensor_data():
    data = request.get_json()
    temperature = data.get("temperature")
    humidity = data.get("humidity")

    # Verifica las condiciones de notificación
    if temperature < 15 or temperature > 30:
        send_voice_notification("Alerta de temperatura!")

    if humidity < 20 or humidity > 67:
        send_voice_notification("Alerta de humedad!")

    # Almacena los datos en la lista sensor_data
    with sensor_data_lock:
        sensor_data.append({"temperature": temperature, "humidity": humidity})
        sensor_data[:] = sensor_data[-1000:]

    return jsonify({"message": "Datos recibidos con éxito"})


@app.route("/data", methods=["GET"])
def get_sensor_data():
    with sensor_data_lock:
        return jsonify(sensor_data)


@app.route("/view", methods=["GET"])
def view_sensor_data():
    with sensor_data_lock:
        return render_template("data.html", sensor_data=sensor_data)


if __name__ == "__main__":
    app.run(host=os.environ.get("HOST", "0.0.0.0"), port=int(os.environ.get("PORT", 5000)))
